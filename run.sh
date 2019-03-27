#!/usr/bin/env bash

## Um auf /data/ Veraenderungen vorzunehmen, muss man Root sein!
if [ "$( id -u )" != "0" ]; then
	echo "Skript muss als Root ausgeführt werden!" 1>&2
	exit 1
fi

## Script muss im richtigen Ordner ausgefuert werden, da Python-Skripte ansonsten nicht laufen
FOLDER_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $FOLDER_PATH

LABELBOX_PATH="/data/DVS/DVS_HGH/labelbox"

## Minimierung der exportierten JSON-Dateien!
python3 minify.py $FOLDER_PATH/exported/ >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Minimierung der JSON-Dateien nicht erfolgreich"
    exit 1
fi

## Standardisierung der minimierten JSON-Dateien
python3 standardize.py $FOLDER_PATH/minified/ >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Standardisierung der JSON-Dateien nicht erfolgreich!"
    exit 1
fi

echo "Minimierung/ Standardisierung erfolgreich abgeschlossen!"
read -n 1 -p "Nach $LABELBOX_PATH kopieren (y|n): " ANSWER
case $ANSWER in
	N|n)    echo ""
            exit
            ;;
	*)		echo ""
            ;;
esac

## Testen, ob Labelbox-Ordner auf /data/ vorhanden!
if [ ! -d "$LABELBOX_PATH" ]; then
    echo "Labelbox-Ordner nicht erreichbar!"
    exit 1
fi

## Testen, ob LB-JSON-Ordner auf /data/ vorhanden!
LB_JSON_PATH="$LABELBOX_PATH/json"
if [ ! -d $LB_JSON_PATH ]; then
    echo "Labelbox-JSON-Ordner existiert noch nicht!"
    cd $LABELBOX_PATH
    
    mkdir json
    if [ $? -ne 0 ]; then
        echo "Labelbox-JSON-Ordner konnte nicht hinzugefuegt werden!"
        echo "Moeglicherweise keine Rechte vorhanden?"
        exit 1
    fi

    echo "Labelbox-JSON-Ordner wurde hinzugefuegt!"
fi

## Alle JSON-Dateien in LB-JSON-Ordner kopieren!
cp $FOLDER_PATH/minified/*.json $LB_JSON_PATH
if [ $? -ne 0 ]; then
    echo "Minimierte, standardisierte JSON-Dateien konnten nicht kopiert werden!"
    exit 1
fi

printf "Minimierte, standardisierte JSON-Dateien erfolgreich nach \n $LB_JSON_PATH \nkopiert!\n"
