# Intacct-to-GoBD

A script (convert_intacct_to_gobd.py) to convert a provided CSV file (converted from Intacct's Excel export) to a format acceptable to Germany's GoBD rules. I think?

## Examples
```
$ ./convert_intacct_to_gobd.py -f general_ledger_2014.csv
[2018-07-30 16:16:46.754634] Starting...
[2018-07-30 16:16:46.754815] Output dir: general_ledger_2014_GoBD_output
[2018-07-30 16:16:46.834647] Finished.
```
```
$ ./convert_intacct_to_gobd.py -f general_ledger_2014.csv -z
[2018-07-30 16:26:30.734215] Starting...
[2018-07-30 16:26:30.734384] Output dir: general_ledger_2014_GoBD_output
[2018-07-30 16:26:30.734409] Output dir already exists! Exiting for safety!
```
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
