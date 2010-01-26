#!/bin/sh
cd iosshy
for qrc in *.qrc; do
	pyrcc4 "$qrc" -o "$(basename "$qrc" ".qrc")_rc.py"
done
for ui in *.ui; do
	pyuic4 "$ui" -o "Ui_$(basename "$ui" ".ui").py"
done
