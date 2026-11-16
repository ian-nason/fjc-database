<a id="fjc-integrated-database-idb-as-a-duckdb-database"></a>

# FJC Integrated Database (IDB)

Federal district-court civil records, criminal-defendant records and appeals from the Federal Judicial Center (FJC) Integrated Database (IDB). Civil records cover statistical years (SY) 1988 through June 2026; criminal defendants cover fiscal years (FY) 1970–2025; appeals cover 1971 through June 2026. Use this database to study filing patterns, case dispositions and sentences. Reopened or transferred civil matters can have multiple records, so row counts are not counts of unique cases.

<a id="quick-start"></a>

## Start querying

Preview civil source records filed from 2025 onward. Reopened or transferred matters can have repeated docket keys. The result shows up to five records: `FILEDATE` is the filing date and `DISTRICT` is a court district code, not a district name. A filing year is different from the statistical or fiscal reporting year.

Choose R or Python. Install the datapond package once: use `install.packages("datapond")` in R, or run `python -m pip install datapond` in a terminal.

### R

```r
library(datapond)
con <- dp_connect("fjc")
tryCatch({
  DBI::dbExecute(con, "SET threads=1")
  DBI::dbExecute(con, "SET memory_limit='128MiB'")
  DBI::dbExecute(con, "SET max_temp_directory_size='0B'")
  print(DBI::dbGetQuery(con, "SELECT FILEDATE,DISTRICT FROM civil WHERE FILEDATE>=DATE '2025-01-01' LIMIT 5"))
}, finally = dp_disconnect(con))
```

### Python

```python
import datapond
con = datapond.connect('fjc')
try:
    con.execute("SET threads=1")
    con.execute("SET memory_limit='128MiB'")
    con.execute("SET max_temp_directory_size='0B'")
    print(con.execute("""SELECT FILEDATE,DISTRICT FROM civil WHERE FILEDATE>=DATE '2025-01-01' LIMIT 5""").fetchall())
finally:
    con.close()
```

Queries run on your computer and read the byte ranges they need. A small result can still require a large scan. These examples limit DuckDB to one thread and a 128 MiB buffer pool with disk spill disabled; that is not a limit on the entire R or Python process. Larger analyses may need more memory or a local download with enough disk space.

<a id="additional-dataset-notes"></a>

## Tables and coverage

**About 21.1 million records across three tables.**

| Table  |  Rows  |  Coverage |
| ------- | -----: | ---------- |
| `civil`  |  10.96M  |  cases filed, terminated or pending, statistical year 1988 through 2026-06-30 |
| `criminal`  |  7.74M  |  defendants, FY1970 through 2025 |
| `appellate`  |  2.42M  |  appeals docketed 1971 through 2026-06-30 |

Bankruptcy data (2008+) exists in the IDB but the FJC only serves it through its interactive query tool, not as a bulk file, so it is not included.

See the [data dictionary](https://github.com/ian-nason/fjc-database/blob/main/DICTIONARY.md) for column definitions.

<a id="what-the-tables-contain"></a>

## Keys and useful views

Views: `v_civil_by_year` (cases by filing year and nature of suit), `v_criminal_by_year`
(defendants by harmonised `fiscal_year`, source file and lead filing offense, with the
1996+ `FOFFCD1` and 1970-95 `FOFFCODE` codes kept in separate columns because the two
codebooks number offenses differently), `v_appeals_by_year`.

Civil docket keys are `(CIRCUIT, DISTRICT, OFFICE, DOCKET)`. They can repeat for reopened or transferred matters; criminal rows instead represent defendants. Appellate district-case fields and the limits of these links are described in the interpretation notes below.

## Comparing reporting eras

Different reporting eras use different columns. Where the FJC changed variable names
between eras (criminal 1970-95 used `FOFFCODE`, `PRISONMO`, `SENTTYPE` ...; 1996+ uses
`FOFFCD1`, `PRISTIM1`, `DISP1` ...), both sets of columns exist and each row fills the
ones its era carried. `source_file` says which extract a row came from; `criminal.fiscal_year`
is `FISCALYR` (1996+) or `TAPEYEAR` (1970-95).

The `TAPEYEAR` field on civil records identifies the statistical year in which the record was last reported; it is not the filing year.

Date fields use SQL `DATE` values; the IDB's `-8`/`-9` "not applicable" codes and the
`01/01/1900` date sentinel are stored as `NULL`; integer-coded fields are `INTEGER`;
docket numbers, statute titles/sections and nature-of-suit codes stay text.

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
- **Invalid calendar dates in the source** (e.g. February 30) are `NULL`; counts are recorded in `_rejected_rows` and the build log. The build threshold is documented below.
- **638 civil rows (0.006%) were skipped** because a party name contains a stray tab that
  breaks the 46-column layout; they are counted in `_rejected_rows`.
- Party names (`PLT`, `DEF`, `NAME`, `APPELLAN`, `APPELLEE`) are as keyed by clerks:
  inconsistent casing, abbreviations and "ET AL".
- Appellate `DCIRC`/`DDIST`/`DOFFICE`/`DDOCKET` link an appeal to its district case, but
  the IDB warns that the district docket number is not always populated or unique.

<a id="advanced-access-quick-start"></a>

## More example queries

Count civil source records for nature-of-suit code `440` (other civil rights) by filing year from 2015 onward. This counts records, including any repeated docket keys described above.

```python
import datapond
con = datapond.connect("fjc")
con.sql("""
    SELECT EXTRACT(YEAR FROM FILEDATE) AS year, COUNT(*) AS case_records
    FROM civil WHERE NOS = '440' AND FILEDATE >= '2015-01-01'   -- 440 = other civil rights
    GROUP BY 1 ORDER BY 1
""").show()
```

## Other ways to connect

Open the hosted file directly in DuckDB and count criminal-defendant records by the harmonized fiscal reporting year. This is an alternative connection method, not an additional setup step.

```sql
INSTALL httpfs; LOAD httpfs;
ATTACH 'https://huggingface.co/datasets/Nason/fjc-database/resolve/main/fjc.duckdb' AS fjc (READ_ONLY);
SELECT fiscal_year, COUNT(*) FROM fjc.criminal GROUP BY 1 ORDER BY 1;
```

<a id="coverage-fields-and-sources"></a>

## Sources and maintenance

### Sources and codebooks

Source: [Federal Judicial Center (Integrated Database)](https://www.fjc.gov/research/idb). License: Public domain.

The federal courts report these records to the Administrative Office of the U.S. Courts; the FJC publishes quarterly text extracts. The included files are `cv88on.zip` (civil), `cr70to95.zip` and `cr96on.zip` (criminal), and `ap71to07.zip` and `ap08on_0.zip` (appeals).

Column names are the IDB's own (uppercase). Their meaning and code values are in the
FJC codebooks copied into `docs/`:

- `Civil_Codebook_1970-1987.pdf` (the 1988-forward civil codebook is not posted online; the
  1970-87 one documents the same fields, and CourtListener's
  [IDB facts page](https://free.law/idb-facts/) has the nature-of-suit and office code lists)
- `Criminal_Code_Book_1970-1995.pdf`, `Criminal_Code_Book_1996_Forward.pdf`
- `Appeals_Codebook_1971-2007.pdf`, `Appeals_Codebook_2008_Forward_rev_02102021.pdf`

The build combines the two eras of each file by column name. It asserts that invalid calendar dates are under 0.1% of any date column and records their counts in `_rejected_rows` and the build log.

### Build

```bash
uv sync
uv run python build_database.py            # downloads ~700 MB of zips, ~10 minutes, ~2.5 GB output
uv run python publish_to_hf.py --token hf_xxx --verify
```

Memory: DuckDB is capped at 4 GB (`DATAPOND_MEMORY_LIMIT`, `DATAPOND_THREADS`).
Shared build machinery comes from [datapond-build](https://github.com/datapond-db/datapond-build).

### License

Code: MIT. Data: public domain (U.S. federal government).
