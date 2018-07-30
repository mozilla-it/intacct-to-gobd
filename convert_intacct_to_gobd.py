#!/usr/bin/env python3

#
# TODO: error-check the CSV
#

import sys,os,errno,re,argparse
from datetime import datetime
from subprocess import call

def print_debug(level, message):
  if debug >= level:
    print("[%s] %s" % (datetime.now(),message))

def create_output_dir(infilename, overwrite):
  infile_basename = os.path.basename(infilename)
  print_debug(5, "Infile basename: %s" % infile_basename)
  m = re.match('(.*)\.', infile_basename)
  if not m:
    raise Exception("Couldn't parse infilename: %s" % infile_basename)
  else:
    output_dir = m.group(1) + '_GoBD_output'
    print_debug(3, "Output dir: %s" % output_dir)
    if os.path.exists(output_dir) and not overwrite:
      print_debug(1, "Output dir already exists! Exiting for safety!")
      exit(1)
    elif os.path.exists(output_dir) and overwrite:
      print_debug(3, "Output dir already exists! Overwriting!")
    else:
      os.makedirs(output_dir)
    return output_dir

def output_xml_file(output_dir, start_date, end_date):
  xml_template = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'INDEX.XML.tmpl')
  with open(xml_template) as fh:
    out_fh = open_output_file(output_dir, 'INDEX.XML')
    for line in fh:
      m = re.search('(START|END)_DATE', line)
      if m:
        if m.group(1) == 'START':
          line = re.sub('START_DATE', start_date, line)
        else:
          line = re.sub('END_DATE', end_date, line)
      out_fh.write(line)
    out_fh.close
  fh.close
  call(['cp',os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'gdpdu-01-08-2002.dtd'), output_dir])

def open_output_file(output_dir, filename):
  outfile = os.path.join(output_dir, filename)
  print_debug(4, "Opening %s for writing" % outfile)
  fh = open(outfile, "w")
  return fh

def output_account_line(accounts_fh, line):
  m = re.match('^(\d{4}(?:\.\d+)?) - (.*),,,,,,,,,,,,,,("?[0-9,.-]+"?)', line)
  if m:
    print_debug(4, "Writing account: {},{},{}".format(m.group(1), m.group(2), m.group(3)))
    accounts_fh.write("{},{},{}\n".format(m.group(1), m.group(2), m.group(3)))
    return m.group(1)
  else:
    raise Exception('Unable to parse account line: %s' % line)

def output_gl_line(gl_fh, account_num, line):
  gl_fh.write("{},{}\n".format(account_num, line))

def parse_csv_file(filename, accounts_fh, gl_fh):
  with open(filename, encoding='latin1') as fh:
    account_num = 0
    start_date  = "1/1/01"
    end_date    = "12/31/99"
    for line in fh:
      line = line.rstrip()

      if re.match('(?:Company|Report|Posted|Totals|Grand)', line):
        print_debug(4, "Skipping header line: %s" % line)

      elif re.match('Start Date:,([^,]+),,,,,,,,,,,,,', line):
        m = re.match('Start Date:,([^,]+),,,,,,,,,,,,,', line)
        start_date = m.group(1)
        print_debug(4, "Start date found: %s" % start_date)

      elif re.match('End Date:,([^,]+),,,,,,,,,,,,,', line):
        m = re.match('End Date:,([^,]+),,,,,,,,,,,,,', line)
        end_date = m.group(1)
        print_debug(4, "End date found: %s" % end_date)

      elif line == ',,,,,,,,,,,,,,':
        print_debug(5, "Skipping 'blank' csv line")

      elif re.match('^\d{4}(?:\.\d+)? - ', line):
        account_num = output_account_line(accounts_fh, line)

      else:
        output_gl_line(gl_fh, account_num, line)

  fh.closed
  return(start_date, end_date)
  

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Convert Intacct .csv extract to German GoBD format")
  parser.add_argument('-f', '--file', action='store', help='input filename', required=True)
  parser.add_argument('-O', '--overwrite', action='store_true', help='overwrite the output dir if it exists')
  parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
  parser.add_argument('-z', '--zip', action='store_true', help='zip the resulting dir')
  args = parser.parse_args()
  
  debug = args.debug

  print_debug(1, "Starting...")

  infile = args.file
  if not infile:
    print_debug(1, "No input file given. Exiting.")
    exit(1)
  elif not os.path.exists(infile):
    print_debug(1, "Input file does not exist! Exiting.")
    exit(1)

  out_dir = create_output_dir(infile, args.overwrite)
  accounts_fh = open_output_file(out_dir, 'accounts.csv')
  gl_fh = open_output_file(out_dir, 'general_ledger.csv')
  (start_date, end_date) = parse_csv_file(infile, accounts_fh, gl_fh)
  gl_fh.close()
  accounts_fh.close()
  output_xml_file(out_dir, start_date, end_date)
  if args.zip:
    print_debug(2, "Zipping up the result")
    call(['zip', '-r', out_dir + '.zip', out_dir])
    print_debug(1, "Zipfile: %s" % out_dir + '.zip')

  print_debug(1, "Finished.")
