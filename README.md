# Intacct-to-GoBD

A script (`convert_intacct_to_gobd.py`) to convert a provided CSV file (converted from Intacct's Excel export) to a format acceptable to Germany's GoBD rules. I think?

## Expected flow
1. The German Government requests some info
2. Finance exports Intacct data (perhaps a year's worth) as an Excel file
3. Finance converts the Excel file to CSV (Comma Separated Values)
3. The CSV file is sent to whomever is running this script
4. This script is run resulting in a zipfile
5. The zipfile is sent back to Finance
6. Finance passes it on

## Usage
```
$ ./convert_intacct_to_gobd.py --help
usage: convert_intacct_to_gobd.py [-h] -f FILE [-O] [-d DEBUG] [-z]

Convert Intacct .csv extract to German GoBD format

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  input filename
  -O, --overwrite       overwrite the output dir if it exists
  -d DEBUG, --debug DEBUG
                        debug level
  -z, --zip             zip the resulting dir
```

## Examples
Output to a directory:
```
$ ./convert_intacct_to_gobd.py -f general_ledger_2014.csv
[2018-07-30 16:16:46.754634] Starting...
[2018-07-30 16:16:46.754815] Output dir: general_ledger_2014_GoBD_output
[2018-07-30 16:16:46.834647] Finished.

$ ls -al general_ledger_2014_GoBD_output/
total 3360
drwxr-xr-x   6 cvalaas  staff      192 Jul 30 16:34 .
drwxr-xr-x  11 cvalaas  staff      352 Jul 30 16:34 ..
-rw-r--r--   1 cvalaas  staff     3043 Jul 30 16:34 INDEX.XML
-rw-r--r--   1 cvalaas  staff    17203 Jul 30 16:34 accounts.csv
-rwxr-xr-x@  1 cvalaas  staff     6668 Jul 30 16:34 gdpdu-01-08-2002.dtd
-rw-r--r--   1 cvalaas  staff  1685566 Jul 30 16:34 general_ledger.csv
```

Zip the resulting directory after creating:
```
$ ./convert_intacct_to_gobd.py -f general_ledger_2014.csv -z
[2018-07-30 16:26:30.734215] Starting...
[2018-07-30 16:26:30.734384] Output dir: general_ledger_2014_GoBD_output
[2018-07-30 16:26:30.734409] Output dir already exists! Exiting for safety!
```

Oops, the output dir already exists, so overwrite it:
```
$ ./convert_intacct_to_gobd.py -f general_ledger_2014.csv -z -O
[2018-07-30 16:26:35.802121] Starting...
[2018-07-30 16:26:35.802340] Output dir: general_ledger_2014_GoBD_output
[2018-07-30 16:26:35.802429] Output dir already exists! Overwriting!
[2018-07-30 16:26:35.882656] Zipping up the result
  adding: general_ledger_2014_GoBD_output/ (stored 0%)
  adding: general_ledger_2014_GoBD_output/gdpdu-01-08-2002.dtd (deflated 65%)
  adding: general_ledger_2014_GoBD_output/INDEX.XML (deflated 79%)
  adding: general_ledger_2014_GoBD_output/general_ledger.csv (deflated 87%)
  adding: general_ledger_2014_GoBD_output/accounts.csv (deflated 81%)
[2018-07-30 16:26:35.931742] Zipfile: general_ledger_2014_GoBD_output.zip
[2018-07-30 16:26:35.931899] Finished.
```

## Supporting Docs
Some sample docs provided by Audicon GmbH
