#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json


def standardize(path :str) -> int:
    BREITE :int = 768
    HOEHE :int = 640
    # Die Klasse für ein Objekt, was man bei Labelbox NICHT erkannt hat
    STANDARD_KLASSE :str = "nicht-erkannt"

    if os.path.isdir(path):
        files = [
            path+n for n in os.listdir(path) if (
                os.path.isfile(os.path.join(path, n)) and n.endswith(".min.json")
            )
        ]

        if len(files) == 0:
            return 2
    else:
        files = [path]

    for file in files:
        pics :int = 0
        objects :int = 0
        labels_not_set :int = 0

        try:
            data = json.load(open(file))
        except Exception as e:
            return 1
        
        # Liste aller Indizes, die geloescht werden koennen weil geskippt!
        marked_to_delete = []

        for i in range(len(data)):
            keys = [key for key in data[i]]
            for key in keys:
                if key == "Label":
                    pics += 1

                    # Skip wird eingetragen, wenn in Labelbox geskippt wurde (aka kein Label gefunden/ fehlerhaftes geloescht)
                    if data[i][key] == "Skip":
                        marked_to_delete.append(i)
                        break

                    for obj in data[i][key]["object"]:
                        objects += 1

                        if "label-klasse" not in obj or obj["label-klasse"] == None:
                            obj["label-klasse"] = STANDARD_KLASSE
                            labels_not_set += 1
                            print(f"Klasse nicht gesetzt: {file} => [{i}] => Label-Objekt[{data[i][key]['object'].index(obj)}]")

                        for coords in obj["geometry"]:
                            if coords["x"] >= BREITE:
                                alt = coords["x"]
                                coords["x"] = BREITE-1
                                print(f"X-Koordinate: {file} => [{i}] => Label-Objekt[{data[i][key]['object'].index(obj)}]: {alt} zu {coords['x']}")
                            elif coords["x"] < 0:
                                alt = coords["x"]
                                coords["x"] = 0
                                print(f"X-Koordinate: {file} => [{i}] => Label-Objekt[{data[i][key]['object'].index(obj)}]: {alt} zu {coords['x']}")

                            if coords["y"] >= HOEHE:
                                alt = coords["y"]
                                coords["y"] = HOEHE-1
                                print(f"Y-Koordinate: {file} => [{i}] => Label-Objekt[{data[i][key]['object'].index(obj)}]: {alt} zu {coords['y']}")
                            elif coords["y"] < 0:
                                alt = coords["y"]
                                coords["y"] = 0
                                print(f"Y-Koordinate: {file} => [{i}] => Label-Objekt[{data[i][key]['object'].index(obj)}]: {alt} zu {coords['y']}")
        
        # Reverse for through data!
        for i in reversed(marked_to_delete):
            del data[i]

        print(f"\nDatei: {file}\n{pics} Bilder bearbeitet, {objects} Objekte gefunden => {labels_not_set} nicht gelabelt! (~{round(labels_not_set/objects*100, 3)}% fehlerhaft!)\n")
        print(f"Anzahl geskippter Frames: {len(marked_to_delete)}")

        with open(file, "w") as json_out:
            json.dump(data, json_out)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        path :str = sys.argv[1]
        if os.path.exists(path):
            status :int = standardize(path)

            if status == 1:
                print("Es ist irgendein Fehler mit der Verarbeitung aufgetreten!\n")
            elif status == 2:
                print("Es wurden keine JSON-Dateien gefunden!\n")
            else:
                print("Die Datei(en) wurden standardisiert!\n")
                exit(0)
        else:
            print("Bei dem angegebenen Pfad handelt es sich weder um eine Datei noch um ein Verzeichnis!\n")
    else:
        print("Es muss der zu standardisierende (und bereits minimierte!) JSON-Export angegeben werden! Nur eine Datei oder ein ganzes Verzeichnis!\n")
    
    # For every possible Fail
    exit(1)