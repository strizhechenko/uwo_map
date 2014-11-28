#!/bin/bash

. /usr/local/Reductor/etc/const

$BINDIR/show_stat.sh gen_stat | sed -e 's/^#/&##/g' | markdown /dev/stdin &> $TMPDIR/show_stat.sh
