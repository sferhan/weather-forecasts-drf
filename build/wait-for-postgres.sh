#!/bin/bash
i="0"

while [ $i -lt 10 ] ; do
    psql -U postgres -c 'select 1;' > /dev/null 2>&1
    if [ $? -eq 0 ] ; then
        exit 0
    fi
    i=$[$i+1]
    sleep 1
done

set -e
psql -U postgres -c 'select 1;'