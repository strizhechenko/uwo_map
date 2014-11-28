#!/bin/bash

. /usr/local/Reductor/etc/const
$BINDIR/diagnostic.sh markdown auto 2>&1 | sed -e 's/^#/&##/g' | markdown /dev/stdin &> $TMPDIR/markdowned
sed -E "s|\[.*OK.*\]|<i class='icon-checkmark fg-green'></i>|g" $TMPDIR/markdowned > $TMPDIR/markdowned.1
sed -E "s|\[.*СБОЙ.*\]|<i class='icon-cancel-2 fg-red'></i>|g" $TMPDIR/markdowned.1 > $TMPDIR/markdowned.2
sed -E "s|^(<h4>)(.*)(<i class='icon-.*'></i>)(.*)|\1\3 \2\4|g" $TMPDIR/markdowned.2 > $TMPDIR/diagnostic.sh
rm -f $TMPDIR/markdowned*
