# FJC Integrated Database (IDB) as a DuckDB database

Every civil case, criminal defendant and appeal reported by the federal courts to the
Administrative Office of the U.S. Courts, as published by the Federal Judicial Center's
[Integrated Database](https://www.fjc.gov/research/idb), in a single queryable DuckDB file.

**~21.1M rows across 3 tables** (rebuilt from the FJC's quarterly text extracts):

| Table | Rows | Coverage | Source files |
|-------|-----:|----------|--------------|
| `civil` | 10.96M | cases filed, terminated or pending, statistical year 1988 through 2026-06-30 | `cv88on.zip` |
| `criminal` | 7.74M | defendants, FY1970 through 2025 | `cr70to95.zip`, `cr96on.zip` |
| `appellate` | 2.42M | appeals docketed 1971 through 2026-06-30 | `ap71to07.zip`, `ap08on_0.zip` |

Bankruptcy data (2008+) exists in the IDB but the FJC only serves it through its
interactive query tool, not as a bulk file, so it is not included.

## Quick start

```python
import datapond
con = datapond.connect("fjc")
con.sql("""
    SELECT EXTRACT(YEAR FROM FILEDATE) AS year, COUNT(*) AS cases
    FROM civil WHERE NOS = '440' AND FILEDATE >= '2015-01-01'   -- 440 = other civil rights
    GROUP BY 1 ORDER BY 1
""").show()
```

```sql
INSTALL httpfs; LOAD httpfs;
ATTACH 'https://huggingface.co/datasets/Nason/fjc-database/resolve/main/fjc.duckdb' AS fjc (READ_ONLY);
SELECT fiscal_year, COUNT(*) FROM fjc.criminal GROUP BY 1 ORDER BY 1;
```

## What the tables contain

Column names are the IDB's own (uppercase). Their meaning and code values are in the
FJC codebooks copied into `docs/`:

- `Civil_Codebook_1970-1987.pdf` (the 1988-forward civil codebook is not posted online; the
  1970-87 one documents the same fields, and CourtListener's
  [IDB facts page](https://free.law/idb-facts/) has the nature-of-suit and office code lists)
- `Criminal_Code_Book_1970-1995.pdf`, `Criminal_Code_Book_1996_Forward.pdf`
- `Appeals_Codebook_1971-2007.pdf`, `Appeals_Codebook_2008_Forward_rev_02102021.pdf`

Two eras of each file are unioned by column name. Where the FJC changed variable names
between eras (criminal 1970-95 used `FOFFCODE`, `PRISONMO`, `SENTTYPE` ...; 1996+ uses
`FOFFCD1`, `PRISTIM1`, `DISP1` ...), both sets of columns exist and each row fills the
ones its era carried. `source_file` says which extract a row came from; `criminal.fiscal_year`
is `FISCALYR` (1996+) or `TAPEYEAR` (1970-95).

Typing: `MM/DD/YYYY` fields are `DATE`; the IDB's `-8`/`-9` "not applicable" codes and the
`01/01/1900` date sentinel are stored as `NULL`; integer-coded fields are `INTEGER`;
docket numbers, statute titles/sections and nature-of-suit codes stay text.

Views: `v_civil_by_year` (cases by filing year and nature of suit), `v_criminal_by_year`
(defendants by harmonised `fiscal_year`, source file and lead filing offense, with the
1996+ `FOFFCD1` and 1970-95 `FOFFCODE` codes kept in separate columns because the two
codebooks number offenses differently), `v_appeals_by_year`.

## Researcher caveats

- **Civil rows are case records, not unique cases.** Each row is the FJC's record of a
  case as of the extract, with `TAPEYEAR` the statistical year it was last reported;
  pending cases have no `TERMDATE`. A reopened, reinstated, remanded or transferred case
  gets a new record with an `ORIGIN` code of 4-7 (see the codebook), so the docket key
  `(CIRCUIT, DISTRICT, OFFICE, DOCKET)` is not unique: 10,959,535 rows carry 10,506,944
  distinct docket keys, and 957,929 rows have a reopening-type `ORIGIN`. To count original
  filings use `ORIGIN = 1` (or `ORIGIN IN (1, 2, 3)` for original, removed and remanded
  filings); to follow one case take all rows with its docket key ordered by `FILEDATE`.
- **Criminal rows are defendants, not cases**; join `DOCKET` + `CIRCUIT` + `DISTRICT` +
  `OFFICE` to group a case.
- **Invalid calendar dates in the source** (e.g. February 30) are `NULL`; the build asserts
  they are under 0.1% of any date column and records the counts in `_rejected_rows`
  and the build log.
- **638 civil rows (0.006%) were skipped** because a party name contains a stray tab that
  breaks the 46-column layout; they are counted in `_rejected_rows`.
- Party names (`PLT`, `DEF`, `NAME`, `APPELLAN`, `APPELLEE`) are as keyed by clerks:
  inconsistent casing, abbreviations and "ET AL".
- Appellate `DCIRC`/`DDIST`/`DOFFICE`/`DDOCKET` link an appeal to its district case, but
  the IDB warns that the district docket number is not always populated or unique.

## Build

```bash
uv sync
uv run python build_database.py            # downloads ~700 MB of zips, ~10 minutes, ~2.5 GB output
uv run python publish_to_hf.py --token hf_xxx --verify
```

Memory: DuckDB is capped at 4 GB (`DATAPOND_MEMORY_LIMIT`, `DATAPOND_THREADS`).
Shared build machinery comes from [datapond-build](https://github.com/datapond-db/datapond-build).

## License

Code: MIT. Data: public domain (U.S. federal government).
