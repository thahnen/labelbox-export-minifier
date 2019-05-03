# labelbox-export-minifier
---

## minify.py:
Minifies the exported JSON from Labelbox.
Deletes useless information, mostly doubles and timestamps etc.

---

## standardize.py:
Standardizes the X/Y-coordinates onto 0-767 (for X) and 0-639 (for Y).
Also looks for missing classes and adds a standard value.

---

## run.sh
Bash-script for minifying and standardizing (using the python scripts).
Afterwards the data gets copied to the NAS if said so.

---

## TODO
1. Test auf *exported* und *minified* Verzeichnisse (in minify.py nur noch)
2. parallelisieren der Minimierung/ Standardisierung!
