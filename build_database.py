#!/usr/bin/env python3
"""Build fjc.duckdb from the Federal Judicial Center's Integrated Database (IDB).

Sources (tab-delimited text inside zips, https://www.fjc.gov/research/idb):
    cv88on.zip     civil cases filed/terminated/pending, SY1988-present (updated quarterly)
    cr70to95.zip   criminal defendants FY1970-FY1995
    cr96on.zip     criminal defendants FY1996-present
    ap71to07.zip   appellate cases 1971-2007
    ap08on_0.zip   appellate cases 2008-present
(The bankruptcy extract is only available through the FJC's interactive tool.)

Usage:
    uv run python build_database.py            # download (if needed) + build
    uv run python build_database.py --tables civil criminal
    DATAPOND_MEMORY_LIMIT=4GB DATAPOND_THREADS=2 uv run python build_database.py
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path

import duckdb

from datapond_build import Checker, build_columns_table, ensure_metadata, export_dictionary
from datapond_build.fetch import download_file
from datapond_build.session import connect

BASE_URL = "https://www.fjc.gov/sites/default/files/idb/textfiles"
RAW_DIR = Path("data/raw")
DEFAULT_OUTPUT = "fjc.duckdb"

# table -> list of (zip name, member name)
SOURCES = {
    "civil": [("cv88on.zip", "cv88on.txt")],
    "criminal": [("cr70to95.zip", "cr70to95.txt"), ("cr96on.zip", "cr96on.txt")],
    "appellate": [("ap71to07.zip", "ap71to07.txt"), ("ap08on_0.zip", "ap08on.txt")],
}

TABLE_DESCRIPTIONS = {
    "civil": "Civil cases filed in U.S. district courts, statistical year 1988 to present: one row per case "
             "(parties, nature of suit, jurisdiction, filing/termination dates, disposition, judgment)",
    "criminal": "Criminal defendants in U.S. district courts, FY1970 to present: one row per defendant "
                "(filing offenses, disposition, sentence, dates)",
    "appellate": "Appeals filed in U.S. courts of appeals, 1971 to present: one row per appeal "
                 "(origin, nature of suit/offense, disposition, dates, judges)",
}

# IDB uses -8 for "not applicable / missing" in numeric fields and 01/01/1900 or blank in dates.
MISSING_NUMERIC = ("-8", "-9")
REJECTED: dict[str, tuple[int, int]] = {}
UNPARSEABLE_DATES: dict[tuple[str, str], tuple[int, int]] = {}  # (table, col) -> (invalid dates nulled, non-sentinel values)  # file -> (rows skipped as malformed, rows loaded)
DATE_SENTINELS = ("01/01/1900", "")

JOIN_HINTS = {
    "CIRCUIT": "Circuit number (0 = DC, 1-11); joins civil/criminal to appellate.DCIRC",
    "DISTRICT": "District code within circuit; joins to appellate.DDIST",
    "OFFICE": "Divisional office code; joins to appellate.DOFFICE",
    "DOCKET": "Docket number (district) or appeal number; joins to appellate.DDOCKET for district cases",
    "NOS": "Nature of suit code (civil) — see the codebook's NOS table",
    "TAPEYEAR": "Statistical year of the snapshot the row came from",
    "FISCALYR": "Fiscal year of the criminal record (1996+ file)", "fiscal_year": "Fiscal year: FISCALYR, or TAPEYEAR for the 1970-95 file",
}


def resolve_files(table: str) -> list[Path]:
    paths = []
    for zip_name, member in SOURCES[table]:
        zp = RAW_DIR / zip_name
        if not zp.exists():
            if not download_file(f"{BASE_URL}/{zip_name}", zp, desc=zip_name,
                                 headers={"User-Agent": "Mozilla/5.0 (datapond fjc-database build)"}):
                raise SystemExit(f"FATAL: could not download {zip_name}")
        txt = RAW_DIR / member
        if not txt.exists():
            print(f"  extracting {member} from {zip_name}")
            try:
                with zipfile.ZipFile(zp) as zf:
                    zf.extract(member, RAW_DIR)
            except NotImplementedError:  # Deflate64 (cr70to95.zip); Info-ZIP handles it
                subprocess.run(["unzip", "-o", "-q", str(zp), member, "-d", str(RAW_DIR)], check=True)
        # The IDB text files are UTF-8 with a few stray single bytes (0x9B etc.)
        # in party names; iconv -c drops the invalid bytes so DuckDB can read them.
        clean = txt.with_suffix(".clean.txt")
        if not clean.exists() or clean.stat().st_size == 0:
            print(f"  cleaning {member} (dropping invalid UTF-8 bytes)")
            with open(clean, "wb") as out:
                subprocess.run(["iconv", "-f", "UTF-8", "-t", "UTF-8", "-c", str(txt)], stdout=out, check=True)
        paths.append(clean)
    return paths


def header_of(path: Path) -> list[str]:
    with open(path, encoding="latin-1") as fh:
        return fh.readline().rstrip("\r\n").split("\t")


def looks_like_date(col: str) -> bool:
    return bool(re.search(r"DATE|DAT$|DKTDATE|FDATEUSE|TDATEUSE|LOADDATE|DATEUSE|DKTDT|TRANSDAT", col))


def load_table(con, table: str, files: list[Path]) -> int:
    """Load every source file as VARCHAR (union by name), then apply typed casts."""
    con.execute(f"DROP TABLE IF EXISTS {table}")
    parts = []
    for i, path in enumerate(files):
        stage = f"_stage_{table}_{i}"
        con.execute(f"DROP TABLE IF EXISTS {stage}")
        con.execute(f"""
            CREATE TABLE {stage} AS
            SELECT *, '{path.name.replace('.clean', '')}' AS source_file
            FROM read_csv('{path}', delim='\t', header=true, all_varchar=true, quote='',
                          escape='', null_padding=true, ignore_errors=true, store_rejects=true,
                          rejects_table='_rejects_{table}_{i}', rejects_scan='_rejects_scan_{table}_{i}')
        """)
        for (col,) in con.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{stage}'").fetchall():
            if col != col.upper() and col != "source_file":
                con.execute(f'ALTER TABLE {stage} RENAME COLUMN "{col}" TO "{col.upper()}"')
        n = con.execute(f"SELECT COUNT(*) FROM {stage}").fetchone()[0]
        try:
            nrej = con.execute(f"SELECT COUNT(DISTINCT line) FROM _rejects_{table}_{i}").fetchone()[0]
        except Exception:
            nrej = 0
        REJECTED[path.name.replace('.clean', '')] = (nrej, n)
        print(f"  {path.name}: {n:,} rows x {len(header_of(path))} cols; {nrej} malformed rows skipped")
        parts.append(stage)
    union = " UNION ALL BY NAME ".join(f"SELECT * FROM {p}" for p in parts)
    con.execute(f"CREATE TABLE {table} AS {union}")
    for p in parts:
        con.execute(f"DROP TABLE {p}")
    cast_columns(con, table)
    if table == "criminal":
        # FISCALYR exists only in the 1996+ file; the 1970-95 file's TAPEYEAR is the fiscal year of the record.
        con.execute("ALTER TABLE criminal ADD COLUMN fiscal_year INTEGER")
        con.execute("UPDATE criminal SET fiscal_year = COALESCE(FISCALYR, TAPEYEAR)")
    return con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def cast_columns(con, table: str) -> None:
    """Dates MM/DD/YYYY -> DATE (1900-01-01 sentinel -> NULL); pure-integer codes -> INTEGER/BIGINT
    with -8/-9 sentinels -> NULL; everything else stays VARCHAR with blanks -> NULL."""
    cols = [r[0] for r in con.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = ? ORDER BY ordinal_position", [table]
    ).fetchall()]
    total = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    for c in cols:
        if c == "source_file":
            continue
        q = f'"{c}"'
        if looks_like_date(c):
            bad, nonnull = con.execute(f"""SELECT COUNT(*) FILTER (WHERE TRY_STRPTIME({q}, '%m/%d/%Y') IS NULL
                                 AND {q} IS NOT NULL AND {q} NOT IN ('', '01/01/1900', '-8', '-9')),
                                 COUNT(*) FILTER (WHERE {q} IS NOT NULL AND {q} NOT IN ('', '01/01/1900', '-8', '-9')) FROM {table}""").fetchone()
            if nonnull and bad / nonnull < 0.001:
                # invalid calendar dates in the source (e.g. 02/30/1999) become NULL; the count is audited
                UNPARSEABLE_DATES[(table, c)] = (bad, nonnull)
                con.execute(f"""ALTER TABLE {table} ALTER COLUMN {q} SET DATA TYPE DATE USING
                                CASE WHEN {q} IN ('', '01/01/1900', '-8', '-9') THEN NULL
                                     ELSE TRY_STRPTIME({q}, '%m/%d/%Y')::DATE END""")
                continue
        # numeric code columns: every non-blank value is an integer
        bad = con.execute(f"""SELECT COUNT(*) FILTER (WHERE {q} <> '' AND NOT regexp_matches({q}, '^-?[0-9]+$')) FROM {table}""").fetchone()[0]
        if bad == 0 and c not in ("DOCKET", "DDOCKET", "TRANSDOC", "MDLDOCK", "MAGDOCK", "TRANDOCK", "DEFLGKY", "CASLGKY", "COUNTY", "SECTION", "TITL", "FTITLE1", "FTITLE2", "FTITLE3", "FTITLE4", "FTITLE5", "TTITLE1", "TTITLE2", "TTITLE3", "TTITLE4", "TTITLE5", "NOS", "OFFENSE", "CONSDKT"):
            mx = con.execute(f"SELECT MAX(LENGTH({q})) FROM {table}").fetchone()[0] or 0
            typ = "BIGINT" if mx > 9 else "INTEGER"
            con.execute(f"""ALTER TABLE {table} ALTER COLUMN {q} SET DATA TYPE {typ} USING
                            CASE WHEN {q} IN ('', '-8', '-9') THEN NULL ELSE TRY_CAST({q} AS {typ}) END""")
        else:
            con.execute(f"UPDATE {table} SET {q} = NULL WHERE {q} = '' OR {q} = '-8'")
    _ = total


VIEWS = {
    "v_civil_by_year": """
        CREATE OR REPLACE VIEW v_civil_by_year AS
        SELECT EXTRACT(YEAR FROM FILEDATE) AS filed_year, NOS AS nature_of_suit, COUNT(*) AS cases
        FROM civil WHERE FILEDATE IS NOT NULL GROUP BY 1, 2""",
    "v_criminal_by_year": """
        CREATE OR REPLACE VIEW v_criminal_by_year AS
        SELECT FISCALYR AS fiscal_year, FOFFCD1 AS lead_offense_code, COUNT(*) AS defendants
        FROM criminal GROUP BY 1, 2""",
    "v_appeals_by_year": """
        CREATE OR REPLACE VIEW v_appeals_by_year AS
        SELECT EXTRACT(YEAR FROM DKTDATE) AS docketed_year, CIRCUIT AS circuit, COUNT(*) AS appeals
        FROM appellate WHERE DKTDATE IS NOT NULL GROUP BY 1, 2""",
}


def run_validation(con, db_path: Path) -> int:
    ck = Checker("Validation")
    for t in ("civil", "criminal", "appellate"):
        ck.query(con, f"{t} non-empty", f"SELECT COUNT(*) FROM {t}", lambda n: n > 100000, lambda n: f"{n:,} rows")
    ck.query(con, "civil FILEDATE parsed (> 99%)", "SELECT COUNT(FILEDATE) * 1.0 / COUNT(*) FROM civil", lambda v: v > 0.99, lambda v: f"{v:.3%}")
    ck.query(con, "civil latest filing is recent", "SELECT MAX(FILEDATE) FROM civil", lambda d: str(d) >= "2026-01-01", str)
    ck.query(con, "criminal covers FY1970-present", "SELECT COUNT(DISTINCT fiscal_year) FROM criminal", lambda n: n >= 55, str)
    ck.query(con, "criminal FILEDATE is a DATE column", "SELECT data_type FROM information_schema.columns WHERE table_name = 'criminal' AND column_name = 'FILEDATE'", lambda t: t == "DATE", str)
    ck.query(con, "criminal has no lowercase duplicate columns", "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'criminal' AND column_name IN ('filedate', 'termdate')", lambda n: n == 0, str)
    ck.query(con, "criminal FILEDATE parsed (> 95%)", "SELECT COUNT(FILEDATE) * 1.0 / COUNT(*) FROM criminal", lambda v: v > 0.95, lambda v: f"{v:.3%}")
    ck.query(con, "appellate DKTDATE parsed (> 99%)", "SELECT COUNT(DKTDATE) * 1.0 / COUNT(*) FROM appellate", lambda v: v > 0.99, lambda v: f"{v:.3%}")
    ck.query(con, "appellate latest docket is recent", "SELECT MAX(DKTDATE) FROM appellate", lambda d: str(d) >= "2026-01-01", str)
    ck.query(con, "civil NOS present (> 99%)", "SELECT COUNT(NOS) * 1.0 / COUNT(*) FROM civil", lambda v: v > 0.99, lambda v: f"{v:.3%}")
    for v in VIEWS:
        ck.query(con, f"{v} runs", f"SELECT COUNT(*) FROM {v}", lambda n: n > 0, str)
    for (t, c), (bad, nn) in UNPARSEABLE_DATES.items():
        if bad:
            ck.check(f"{t}.{c}: invalid calendar dates nulled < 0.1%", bad / nn < 0.001, f"{bad} of {nn:,}")
    for f, (nrej, n) in REJECTED.items():
        ck.check(f"{f}: malformed rows < 0.01%", nrej <= max(1, n) * 1e-4, f"{nrej} of {n:,}")
    return ck.report()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT))
    ap.add_argument("--tables", nargs="+", choices=list(SOURCES), default=list(SOURCES))
    a = ap.parse_args()
    t0 = time.time()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    con = connect(a.output, fresh=True, memory_limit="4GB", threads=2)
    counts = {}
    for i, t in enumerate(a.tables, 1):
        print(f"\n[{i}/{len(a.tables)}] {t}")
        files = resolve_files(t)
        counts[t] = load_table(con, t, files)
        print(f"  -> {t}: {counts[t]:,} rows")
    print("\nViews")
    for name, sql in VIEWS.items():
        try:
            con.execute(sql); print(f"  {name}")
        except Exception as e:
            print(f"  WARNING {name}: {e}")
    con.execute("DROP TABLE IF EXISTS _rejected_rows")
    con.execute("CREATE TABLE _rejected_rows (source_file VARCHAR, rows_skipped INTEGER, rows_loaded BIGINT)")
    for f, (nrej, n) in REJECTED.items():
        con.execute("INSERT INTO _rejected_rows VALUES (?, ?, ?)", [f, nrej, n])
    for t in [r[0] for r in con.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE '\\_rejects\\_%' ESCAPE '\\'").fetchall()]:
        con.execute(f"DROP TABLE IF EXISTS {t}")
    print("\nMetadata + dictionary")
    ensure_metadata(con, descriptions=TABLE_DESCRIPTIONS, tables=list(counts),
                    source_url="https://www.fjc.gov/research/idb", license="Public domain", replace=True)
    build_columns_table(con, join_hints=JOIN_HINTS, tables=list(counts))
    export_dictionary(con, Path("DICTIONARY.md"), title="fjc Data Dictionary",
                      intro=["Source: [FJC Integrated Database](https://www.fjc.gov/research/idb). Column names are the IDB's own; ",
                             "see the FJC codebooks in docs/ for code values. -8/-9 and 01/01/1900 sentinels are stored as NULL."],
                      style="registry", tables=list(counts))
    con.execute("CHECKPOINT")
    failures = run_validation(con, a.output)
    con.close()
    print(f"\nBUILD DONE in {(time.time() - t0) / 60:.1f} min; {sum(counts.values()):,} rows; {a.output.stat().st_size / 1024**3:.2f} GB")
    if failures:
        print(f"BUILD FAILED: {failures} check(s) failed -- do not publish this file")
        sys.exit(1)


if __name__ == "__main__":
    main()
