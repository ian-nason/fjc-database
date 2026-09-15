# fjc Data Dictionary

Source: [FJC Integrated Database](https://www.fjc.gov/research/idb). Column names are the IDB's own; 
see the FJC codebooks in docs/ for code values. -8/-9 and 01/01/1900 sentinels are stored as NULL.

## civil

Civil cases filed in U.S. district courts, statistical year 1988 to present: one row per case (parties, nature of suit, jurisdiction, filing/termination dates, disposition, judgment)

Rows: 10,959,535

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| CIRCUIT | INTEGER | 0.0% | 0 | Circuit number (0 = DC, 1-11); joins civil/criminal to appellate.DCIRC |
| DISTRICT | VARCHAR | 0.0% | 00 | District code within circuit; joins to appellate.DDIST |
| OFFICE | VARCHAR | 0.0% | 0 | Divisional office code; joins to appellate.DOFFICE |
| DOCKET | VARCHAR | 0.0% | 0000000 | Docket number (district) or appeal number; joins to appellate.DDOCKET for district cases |
| ORIGIN | INTEGER | 0.0% | 1 |  |
| FILEDATE | DATE | 0.0% | 1901-01-01 |  |
| FDATEUSE | DATE | 0.0% | 1901-01-01 |  |
| JURIS | INTEGER | 0.0% | 1 |  |
| NOS | VARCHAR | 0.0% | 110 | Nature of suit code (civil) — see the codebook's NOS table |
| TITL | VARCHAR | 70.4% | *4 |  |
| SECTION | VARCHAR | 6.5% | """198" |  |
| SUBSECT | VARCHAR | 59.2% |  |  |
| RESIDENC | INTEGER | 69.4% | 0 |  |
| JURY | VARCHAR | 46.8% | 0 |  |
| CLASSACT | INTEGER | 98.2% | 1 |  |
| DEMANDED | INTEGER | 3.8% | 0 |  |
| FILEJUDG | INTEGER | 100.0% |  |  |
| FILEMAG | INTEGER | 100.0% |  |  |
| COUNTY | VARCHAR | 0.0% | 00000 |  |
| ARBIT | VARCHAR | 96.7% | , |  |
| MDLDOCK | VARCHAR | 91.1% | #2 |  |
| PLT | VARCHAR | 0.2% |  |  |
| DEF | VARCHAR | 0.5% | IRR |  |
| TRANSDAT | DATE | 98.9% | 1931-01-01 |  |
| TRANSOFF | VARCHAR | 98.8% | 0 |  |
| TRANSDOC | VARCHAR | 98.7% | 0000000 |  |
| TRANSORG | VARCHAR | 97.6% | 0 |  |
| TERMDATE | DATE | 4.4% | 1973-03-28 |  |
| TDATEUSE | DATE | 4.4% | 1987-07-01 |  |
| TRCLACT | INTEGER | 99.0% | 2 |  |
| TERMJUDG | INTEGER | 100.0% |  |  |
| TERMMAG | INTEGER | 100.0% |  |  |
| PROCPROG | INTEGER | 4.4% | 1 |  |
| DISP | INTEGER | 4.4% | 0 |  |
| NOJ | INTEGER | 41.7% | 0 |  |
| AMTREC | INTEGER | 9.3% | 0 |  |
| JUDGMENT | INTEGER | 44.0% | 0 |  |
| DJOINED | VARCHAR | 65.5% | 01/01/1901 |  |
| PRETRIAL | VARCHAR | 92.5% | 01/01/1984 |  |
| TRIBEGAN | VARCHAR | 99.0% | 01/01/1989 |  |
| TRIALEND | VARCHAR | 98.6% | 01/01/1991 |  |
| TRMARB | VARCHAR | 98.2% | E |  |
| PROSE | INTEGER | 19.8% | 0 |  |
| IFP | VARCHAR | 90.3% | FP |  |
| STATUSCD | VARCHAR | 29.0% | L |  |
| TAPEYEAR | INTEGER | 0.0% | 1988 | Statistical year of the snapshot the row came from |
| source_file | VARCHAR | 0.0% | cv88on.txt |  |

## criminal

Criminal defendants in U.S. district courts, FY1970 to present: one row per defendant (filing offenses, disposition, sentence, dates)

Rows: 7,743,962

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| CIRCUIT | INTEGER | 0.0% | 0 | Circuit number (0 = DC, 1-11); joins civil/criminal to appellate.DCIRC |
| DISTRICT | VARCHAR | 0.0% | 00 | District code within circuit; joins to appellate.DDIST |
| OFFICE | VARCHAR | 0.0% | 0 | Divisional office code; joins to appellate.DOFFICE |
| DOCKET | VARCHAR | 0.5% | 0000000 | Docket number (district) or appeal number; joins to appellate.DDOCKET for district cases |
| DEFNO | INTEGER | 0.0% | 0 |  |
| FILEDATE | DATE | 0.0% | 1899-12-01 |  |
| PROCCODE | INTEGER | 81.7% | 1 |  |
| FOFFCODE | INTEGER | 81.7% | 100 |  |
| DUPDEF | INTEGER | 83.2% | 0 |  |
| TERMDATE | DATE | 49.3% | 1900-02-01 |  |
| TRDOCKET | VARCHAR | 85.8% | -1 |  |
| TRDEFNO | INTEGER | 81.7% | 0 |  |
| TRCIR | INTEGER | 81.7% | 0 |  |
| TRDIST | VARCHAR | 99.4% | 00 |  |
| TROFF | VARCHAR | 99.7% | - |  |
| INTERVAL | INTEGER | 81.7% | 0 |  |
| TOFFCODE | INTEGER | 81.7% | 100 |  |
| MAJOROFF | INTEGER | 81.9% | 0 |  |
| COUNSEL | INTEGER | 82.4% | 0 |  |
| JUDGE | INTEGER | 100.0% |  |  |
| OBSERVAT | INTEGER | 97.0% | 0 |  |
| SENTCAT | INTEGER | 89.5% | 1 |  |
| SENTSTAT | INTEGER | 89.5% | 0 |  |
| SENTTYPE | INTEGER | 89.5% | 0 |  |
| PRISONMO | INTEGER | 81.7% | 0 |  |
| PROBMO | INTEGER | 81.7% | 0 |  |
| FINE | INTEGER | 85.9% | 0 |  |
| SEX | INTEGER | 95.7% | 1 |  |
| RACE | INTEGER | 96.1% | 1 |  |
| BIRTHYR | INTEGER | 89.5% | -2 |  |
| MARITAL | INTEGER | 99.0% | 1 |  |
| EDUCAT | INTEGER | 99.3% | 1 |  |
| PRIORREC | INTEGER | 89.5% | 0 |  |
| PRESENT | INTEGER | 97.4% | 0 |  |
| RULE20 | INTEGER | 85.8% | 0 |  |
| NAME | INTEGER | 100.0% |  |  |
| MOFFLVL | INTEGER | 89.2% | 1 |  |
| TOFFLVL | INTEGER | 89.2% | 0 |  |
| TAPEYEAR | INTEGER | 0.0% | 1970 | Statistical year of the snapshot the row came from |
| source_file | VARCHAR | 0.0% | cr70to95.txt |  |
| FISCALYR | INTEGER | 18.3% | 1996 | Fiscal year of the criminal record (1996+ file) |
| CTDEF | INTEGER | 62.5% | 1 |  |
| REOPSEQ | INTEGER | 18.3% | 0 |  |
| TYPEREG | VARCHAR | 18.3% | CR |  |
| TYPETRN | VARCHAR | 99.6% | CR |  |
| TYPEMAG | VARCHAR | 67.2% | CR |  |
| DEFLGKY | VARCHAR | 18.3% | 009010000001CR0010 |  |
| CASLGKY | VARCHAR | 18.3% | 009010000001CR0 |  |
| MAGDOCK | VARCHAR | 67.2% | 0000000 |  |
| MAGDEF | VARCHAR | 67.2% | 0 |  |
| STATUSCD | VARCHAR | 18.3% | E |  |
| FUGSTAT | VARCHAR | 18.3% | N |  |
| FGSTRTDATE | DATE | 81.5% | 1915-01-07 |  |
| FGENDDATE | DATE | 86.5% | 1961-05-08 |  |
| PROCDATE | DATE | 18.3% | 1907-07-22 |  |
| PROCCD | INTEGER | 18.3% | 1 |  |
| APPDATE | DATE | 42.3% | 1905-07-21 |  |
| APPCD | VARCHAR | 42.3% | 1 |  |
| FJUDGE | INTEGER | 100.0% |  |  |
| FCOUNSEL | INTEGER | 18.3% | 0 |  |
| FTITLE1 | VARCHAR | 18.3% | 10:2408.M |  |
| FOFFLVL1 | INTEGER | 18.3% | 1 |  |
| FOFFCD1 | INTEGER | 18.3% | 100 |  |
| D2FOFFCD1 | INTEGER | 18.3% | 100 |  |
| FSEV1 | VARCHAR | 18.3% | 002 |  |
| FTITLE2 | VARCHAR | 59.2% | 10:2408.M |  |
| FOFFLVL2 | INTEGER | 59.2% | 1 |  |
| FOFFCD2 | INTEGER | 59.2% | 100 |  |
| D2FOFFCD2 | INTEGER | 59.2% | 100 |  |
| FSEV2 | VARCHAR | 59.2% | 002 |  |
| FTITLE3 | VARCHAR | 78.8% | 10:2408.M |  |
| FOFFLVL3 | INTEGER | 78.8% | 1 |  |
| FOFFCD3 | INTEGER | 78.8% | 100 |  |
| D2FOFFCD3 | INTEGER | 78.8% | 100 |  |
| FSEV3 | VARCHAR | 78.8% | 003 |  |
| FTITLE4 | VARCHAR | 87.2% | 10:2408.M |  |
| FOFFLVL4 | INTEGER | 87.2% | 1 |  |
| FOFFCD4 | INTEGER | 87.2% | 100 |  |
| D2FOFFCD4 | INTEGER | 87.2% | 100 |  |
| FSEV4 | VARCHAR | 87.2% | 003 |  |
| FTITLE5 | VARCHAR | 92.3% | 10:847.P |  |
| FOFFLVL5 | INTEGER | 92.3% | 1 |  |
| FOFFCD5 | INTEGER | 92.3% | 100 |  |
| D2FOFFCD5 | INTEGER | 92.3% | 100 |  |
| FSEV5 | VARCHAR | 92.3% | 002 |  |
| COUNTY | VARCHAR | 18.3% | 01001 |  |
| TRANDIST | VARCHAR | 99.6% | 00 |  |
| TRANOFF | VARCHAR | 99.6% | 0 |  |
| TRANDOCK | VARCHAR | 99.6% | /99 |  |
| TRANDEF | INTEGER | 99.6% | 0 |  |
| UPDATE | DATE | 52.0% | 1993-05-25 |  |
| DISPDATE | DATE | 67.6% | 1971-09-24 |  |
| SENTDATE | DATE | 70.8% | 1995-10-01 |  |
| INT1 | INTEGER | 37.2% | 0 |  |
| INT2 | INTEGER | 37.2% | 0 |  |
| INT3 | INTEGER | 37.5% | 0 |  |
| TERMOFF | VARCHAR | 67.5% | 0 |  |
| TJUDGE | INTEGER | 100.0% |  |  |
| TCOUNSEL | INTEGER | 67.6% | 0 |  |
| TTITLE1 | VARCHAR | 67.6% | 10:2408.M |  |
| TOFFLVL1 | INTEGER | 67.6% | 1 |  |
| TOFFCD1 | INTEGER | 67.6% | 100 |  |
| D2TOFFCD1 | INTEGER | 67.6% | 100 |  |
| TSEV1 | VARCHAR | 67.6% | 003 |  |
| DISP1 | INTEGER | 67.6% | 0 |  |
| PRISTIM1 | INTEGER | 42.2% | -1 |  |
| PRISCD1 | VARCHAR | 75.1% | 000 |  |
| PROBMON1 | INTEGER | 42.2% | -1 |  |
| PROBCD1 | VARCHAR | 96.5% | 0000 |  |
| SUPVREL1 | INTEGER | 42.2% | -1 |  |
| FINEAMT1 | INTEGER | 42.2% | 0 |  |
| TTITLE2 | VARCHAR | 84.5% | 10:2408.M |  |
| TOFFLVL2 | INTEGER | 84.5% | 1 |  |
| TOFFCD2 | INTEGER | 84.5% | 100 |  |
| D2TOFFCD2 | INTEGER | 84.5% | 100 |  |
| TSEV2 | VARCHAR | 84.5% | 002 |  |
| DISP2 | INTEGER | 84.5% | 0 |  |
| PRISTIM2 | INTEGER | 50.1% | -1 |  |
| PRISCD2 | VARCHAR | 95.8% | 0000 |  |
| PROBMON2 | INTEGER | 50.1% | -1 |  |
| PROBCD2 | VARCHAR | 99.7% | 00 |  |
| SUPVREL2 | INTEGER | 50.1% | -1 |  |
| FINEAMT2 | INTEGER | 50.1% | 0 |  |
| TTITLE3 | VARCHAR | 92.1% | 10:2408.M |  |
| TOFFLVL3 | INTEGER | 92.1% | 1 |  |
| TOFFCD3 | INTEGER | 92.1% | 100 |  |
| D2TOFFCD3 | INTEGER | 92.1% | 100 |  |
| TSEV3 | VARCHAR | 92.1% | 003 |  |
| DISP3 | INTEGER | 92.1% | 0 |  |
| PRISTIM3 | INTEGER | 53.5% | -1 |  |
| PRISCD3 | VARCHAR | 98.7% | ---- |  |
| PROBMON3 | INTEGER | 53.5% | -1 |  |
| PROBCD3 | VARCHAR | 99.9% | 0000 |  |
| SUPVREL3 | INTEGER | 53.5% | -1 |  |
| FINEAMT3 | INTEGER | 53.5% | 0 |  |
| TTITLE4 | VARCHAR | 95.4% | 10:2408.M |  |
| TOFFLVL4 | INTEGER | 95.4% | 1 |  |
| TOFFCD4 | INTEGER | 95.4% | 100 |  |
| D2TOFFCD4 | INTEGER | 95.4% | 100 |  |
| TSEV4 | VARCHAR | 95.4% | 003 |  |
| DISP4 | INTEGER | 95.4% | 0 |  |
| PRISTIM4 | INTEGER | 55.0% | -1 |  |
| PRISCD4 | VARCHAR | 99.5% | 0000 |  |
| PROBMON4 | INTEGER | 55.0% | -1 |  |
| PROBCD4 | VARCHAR | 100.0% | 0000 |  |
| SUPVREL4 | INTEGER | 55.0% | -1 |  |
| FINEAMT4 | INTEGER | 55.0% | 0 |  |
| TTITLE5 | VARCHAR | 97.3% | 10:847.P |  |
| TOFFLVL5 | INTEGER | 97.3% | 1 |  |
| TOFFCD5 | INTEGER | 97.3% | 100 |  |
| D2TOFFCD5 | INTEGER | 97.3% | 100 |  |
| TSEV5 | VARCHAR | 97.3% | 003 |  |
| DISP5 | INTEGER | 97.3% | 0 |  |
| PRISTIM5 | INTEGER | 55.8% | -1 |  |
| PRISCD5 | VARCHAR | 99.8% | 0000 |  |
| PROBMON5 | INTEGER | 55.8% | -1 |  |
| PROBCD5 | VARCHAR | 100.0% | 0000 |  |
| SUPVREL5 | INTEGER | 55.8% | -1 |  |
| FINEAMT5 | INTEGER | 55.8% | 0 |  |
| PRISTOT | INTEGER | 39.2% | -1 |  |
| PROBTOT | INTEGER | 48.2% | -1 |  |
| FINETOT | BIGINT | 18.3% | 0 |  |
| CTFILTRN | INTEGER | 18.3% | 0 |  |
| CTFIL | INTEGER | 18.3% | 0 |  |
| CTFILWOR | INTEGER | 18.3% | 0 |  |
| CTFILR | INTEGER | 18.3% | 0 |  |
| CTTRTRN | INTEGER | 18.3% | 0 |  |
| CTTR | INTEGER | 18.3% | 0 |  |
| CTTRWOR | INTEGER | 18.3% | 0 |  |
| CTTRR | INTEGER | 18.3% | 0 |  |
| CTPN | INTEGER | 18.3% | 0 |  |
| CTPNWOF | INTEGER | 18.3% | 0 |  |
| SOURCE | VARCHAR | 18.3% | CMECF |  |
| VER | INTEGER | 58.0% | 0 |  |
| LOADDATE | DATE | 18.3% | 2012-03-01 |  |
| fiscal_year | INTEGER | 0.0% | 1970 | Fiscal year: FISCALYR, or TAPEYEAR for the 1970-95 file |

## appellate

Appeals filed in U.S. courts of appeals, 1971 to present: one row per appeal (origin, nature of suit/offense, disposition, dates, judges)

Rows: 2,415,526

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| CIRCUIT | INTEGER | 0.0% | 0 | Circuit number (0 = DC, 1-11); joins civil/criminal to appellate.DCIRC |
| DOCKET | VARCHAR | 0.0% | 0000001 | Docket number (district) or appeal number; joins to appellate.DDOCKET for district cases |
| REOPEN | VARCHAR | 96.9% | 1 |  |
| DKTDATE | DATE | 0.0% | 1954-08-05 |  |
| USAPT | INTEGER | 4.1% | 0 |  |
| APPELLAN | VARCHAR | 23.7% | !&A RR CO ETAL |  |
| USAPE | INTEGER | 2.4% | 0 |  |
| APPELLEE | VARCHAR | 26.3% | !ANCROFT |  |
| APPTYPE | INTEGER | 0.0% | 1 |  |
| ORGPROC | INTEGER | 94.2% | 1 |  |
| IFP | INTEGER | 69.7% | 0 |  |
| DIVOFF | INTEGER | 99.8% | 1 |  |
| AGENCY | VARCHAR | 31.4% | -9 |  |
| JURIS | INTEGER | 32.0% | 0 |  |
| NOS | VARCHAR | 2.8% | -9 | Nature of suit code (civil) — see the codebook's NOS table |
| OFFENSE | VARCHAR | 4.2% | -9 |  |
| OTHTYPE | VARCHAR | 78.1% | 0 |  |
| DCIRC | INTEGER | 12.9% | 0 |  |
| DDIST | VARCHAR | 14.5% | 00 |  |
| DOFFICE | VARCHAR | 15.8% | 0 |  |
| DDOCKET | VARCHAR | 14.2% | 0000000 |  |
| DDKTDATE | DATE | 17.8% | 1901-01-01 |  |
| APPDATE | DATE | 17.7% | 1911-11-11 |  |
| AOFILEMO | INTEGER | 41.4% | 0 |  |
| AOFILEYR | INTEGER | 41.4% | 0 |  |
| DISP | INTEGER | 2.5% | 1 |  |
| OUTCOME | INTEGER | 43.3% | 1 |  |
| PROCTERM | INTEGER | 85.4% | 1 |  |
| METHOD | INTEGER | 67.6% | 1 |  |
| PUBSTAT | INTEGER | 31.1% | 0 |  |
| OPDISP | INTEGER | 94.1% | 1 |  |
| JOINAPP | INTEGER | 54.3% | 0 |  |
| CONSDKT | VARCHAR | 66.6% | 0000000 |  |
| CRECDATE | DATE | 76.5% | 1956-09-17 |  |
| BRFILED | VARCHAR | 0.0% | 01/01/1900 |  |
| SUBDATE | DATE | 62.9% | 1945-01-14 |  |
| HEARDATE | DATE | 77.7% | 1941-01-07 |  |
| JUDGDATE | DATE | 1.5% | 1915-05-22 |  |
| OPINION | INTEGER | 69.1% | 0 |  |
| JDGCODE1 | INTEGER | 100.0% |  |  |
| JDGCODE2 | INTEGER | 99.9% | 0 |  |
| JDGCODE3 | INTEGER | 100.0% |  |  |
| TAPEYEAR | INTEGER | 0.0% | 1971 | Statistical year of the snapshot the row came from |
| PROSEFLE | VARCHAR | 22.4% | 0 |  |
| PROSETRM | VARCHAR | 23.6% | 0 |  |
| STATUSCD | VARCHAR | 41.2% | L |  |
| TRUSEDMO | INTEGER | 71.7% | 1 |  |
| TRUSEDYR | INTEGER | 71.7% | 1995 |  |
| TERMDATE | DATE | 95.8% | 1970-12-13 |  |
| CPC | INTEGER | 99.9% | 1 |  |
| CPCDISC | INTEGER | 99.9% | 1 |  |
| JDGPANEL | INTEGER | 95.9% | 1 |  |
| CNSLAPP | INTEGER | 98.4% | 1 |  |
| CNSLCONT | INTEGER | 98.6% | 1 |  |
| CNSLDIS | INTEGER | 98.8% | 1 |  |
| CNSLCIR | INTEGER | 98.6% | 1 |  |
| NEWSYTRM | INTEGER | 69.8% | 1971 |  |
| source_file | VARCHAR | 0.0% | ap08on.txt |  |
| DDEFNUM | INTEGER | 91.5% | 0 |  |
| FEDCAP | VARCHAR | 100.0% | Y |  |
| TRANSDATE | DATE | 85.4% | 2007-10-24 |  |
| TRANSCODE | VARCHAR | 58.6% | E |  |
| DJUDGE | INTEGER | 100.0% |  |  |
| FILEFEE | VARCHAR | 93.3% | FP |  |
| JDG1INV | VARCHAR | 70.4% | A |  |
| JDG2INV | VARCHAR | 71.8% | A |  |
| JDG3INV | VARCHAR | 72.8% | A |  |
| ENBANC | VARCHAR | 60.1% | N |  |
| TRMTYPE | INTEGER | 60.1% | 1 |  |
| TORPROCSUB | INTEGER | 96.5% | 1 |  |
| TRMFEE | VARCHAR | 60.1% | FP |  |
