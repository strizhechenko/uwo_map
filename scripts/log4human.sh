#!/bin/bash

. /usr/local/Reductor/etc/const

log4date() {
	local date="$1"
	egrep -A 100000 ^$date $LOGFILE | fgrep -B 100000 "$(egrep ^$date $LOGFILE | tail -1)"
}

simplify() {
	sed -E "s/^\s*\t*\s*//g; s/$HOSTNAME.*[0-9]+\]://g; s/^$date //g"
}

add_id() {
	sed -e 's|\(<h1>\)\(.*\)\(</h1>\)|<h1 id="\2"><a href="#"><i class="icon-arrow-up-3"></i></a> \2\3|g'
}

trim_and_sort() {
	sed -E "s/^\s*\t*\s*//g" | grep -o "^[^ ]*" | sort -ru
}

add_hr() {
	sed -e 's/Завершено обновление списков РосКомНадзора/&<hr>/g'
}

header() {
	echo
	echo "# $1"
	echo "<a href='/info/log_full#$date'>Подробнее »</a>"
	echo
}

if [ "$1" = 'diag' ]; then
	dates="$(grep "^[0-9].*$HOSTNAME diagnostic.*.sh" $LOGFILE | trim_and_sort)"
	gen_links $dates
	for date in $dates; do
		header "$date"
		echo '<pre>'
		log4date "$date" | grep "$HOSTNAME diagnostic.*.sh" | grep -v "Сообщение уже было отослано" | simplify
		echo '</pre>'
	done
elif [ "$1" = 'update' ]; then
	dates="$(grep "^[0-9].*$HOSTNAME update.sh" $LOGFILE | trim_and_sort)"
	gen_links $dates
	for date in $dates; do
		header "$date"
		echo '<pre>'
		log4date "$date" | egrep "^($date.*update.sh|ResultComment|try|Warning|ERROR)" | simplify | add_hr
		echo '</pre>'
	done
else
	dates="$(grep "^[0-9].*$HOSTNAME update.sh" $LOGFILE | trim_and_sort)"
	gen_links $dates
	for date in $dates; do
		header "$date"
		echo '<pre>'
		log4date "$date" | simplify
		echo '</pre>'
	done

fi | markdown /dev/stdin | add_id > $TMPDIR/${0##*/}
