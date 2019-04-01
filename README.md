# labelbox-export-minifier
---

## minify.py:
Minifies the exported JSON from Labelbox.

---

## standardize.py:
Standardisiert die X/Y-Koordinaten auf 0-767 bzw 0-639.
Setzt ausserdem nichtgesetzte Klassen auf einen Standard-Wert!

---

## run.sh
Bash-Script, dass alle vorhandenen JSON-Dateien minimiert und standardisiert.
Danach wird abgefragt, ob man die Daten auch in den Labelbox-Ordner auf dem NAS kopieren will!

---

## TODO
1. Test auf *exported* und *minified* Verzeichnisse
2. ggf anderes Output-Directory!
3. fuers Standardisieren eine einheitliche Bezeichnung für die Label-Klasse haben!
4. auf nicht vergebene Label achten! diese auf einen anderen Wert setzen, damit sie gefunden werden können!
