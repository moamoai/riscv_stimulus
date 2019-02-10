#!/bin/sh
for TEST in `ls -1 log/`
do
  # echo "log/${TEST}: `grep -e 'Pass' -e 'Fail' log/${TEST}`"
  printf "%-30s: %s\n" "log/${TEST}" "`grep -e 'Pass' -e 'Fail' log/${TEST}`"
done
