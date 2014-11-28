#!/bin/bash

. /usr/local/Reductor/etc/const

set -eu

prog="urldecode.sh"

printable() {
	echo "$1" | egrep -q '^[[:print:]]+$'
}

cp1251() {
	echo "$1" | iconv -f cp1251 -t utf8
}

rm -f $TMPDIR/$prog
[ ! -f "$LISTDIR/$1" ] && exit 0

egrep '^[[:print:]]+$' "$LISTDIR/$1" > $TMPDIR/$prog.printable || true
egrep -v '^[[:print:]]+$' "$LISTDIR/$1" > $TMPDIR/$prog.unprintable || true

while read line; do
	cp1251 "$line"
done  < $TMPDIR/$prog.unprintable >> $TMPDIR/$prog.printable

/opt/reductor_web/scripts/urldecode < $TMPDIR/$prog.printable > $TMPDIR/$prog.1

egrep '^[[:print:]]+$' "$TMPDIR/$prog.1" > $TMPDIR/$prog || true
egrep -v '^[[:print:]]+$' "$TMPDIR/$prog.1" > $TMPDIR/$prog.unprintable || true

while read line; do
	printable "$line" && echo "$line" && continue
	line="$(cp1251 "$line")"
	printable "$line" && echo "$line" && continue
	echo "Не удалось декодировать строку в человекочитаемый вид"
done < $TMPDIR/$prog.unprintable >> $TMPDIR/$prog

rm -f $TMPDIR/$prog.printable $TMPDIR/$prog.unprintable $TMPDIR/$prog.1
