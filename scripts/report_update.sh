#!/bin/bash

. /usr/local/Reductor/etc/const

FILE=$TMPDIR/${0##*/}

log4date() {
	local date="$1"
	egrep -A 100000 ^$date $LOGFILE | fgrep -B 100000 "$(egrep ^$date $LOGFILE | tail -1)"
}

simplify() {
	sed -E "s/^\s*\t*\s*//g; s/$HOSTNAME.*[0-9]+\]://g; s/^$date //g"
}

trim_and_sort() {
	sed -E "s/^\s*\t*\s*//g" | grep -o "^[^ ]*" | sort -ru
}

main() {
	dates="$(grep "^[0-9].*$HOSTNAME update.sh" $LOGFILE | trim_and_sort)"
	echo "## Успешные выгрузки реестра запрещённых сайтов" | markdown /dev/stdin 
	echo "<br>"
	echo "<p>* Время указано с учётом часового пояса $(date +%z)</p>"
	echo "<br>"
	echo "<table class='table striped bordered'>"
	echo "<thead class='text-center'><tr>"
	echo "<td><b>Дата</b></td>"
	echo "<td><b>Первая выгрузка</b></td>"
	echo "<td><b>Последняя выгрузка</b></td>"
	echo "<td><b>Количество выгрузок</b></td>"
	echo "</tr></thead>"
	echo "<tbody class='text-center'>"
	for date in $dates; do
		log4date "$date" | simplify > $TMPDIR/rkn_tmp
		count="$(grep -c "Завершено обновление списков РосКомНадзора" $TMPDIR/rkn_tmp)"
		first="$(grep "Завершено обновление списков РосКомНадзора" $TMPDIR/rkn_tmp | head -1 | egrep -o "[0-9:]*")"
		last="$(grep "Завершено обновление списков РосКомНадзора" $TMPDIR/rkn_tmp | tail -1 | egrep -o "[0-9:]*")"
		[ -z "$first" ] && first="Не было"
		[ -z "$last" ] && last="Не было"
		echo '<tr>'
		echo "<td>$date</td>"
		echo "<td>$first</td>"
		echo "<td>$last</td>"
		echo "<td>$count</td>"
		echo '</tr>'
	done
	echo '</tbody></table>'
}

main > $FILE
