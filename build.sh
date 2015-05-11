#!/bin/sh
cd iosshy
for qrc in *.qrc; do
	pyrcc4 -py3 "$qrc" -o "$(basename "$qrc" ".qrc")_rc.py"
done
for ui in *.ui; do
	pyuic4 --from-imports "$ui" -o "Ui_$(basename "$ui" ".ui").py"
done
