#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json


def standardize(path :str, isdir :bool = False) -> int:
    BREITE :int = 768
    HOEHE :int = 640
    # Die Klasse für ein Objekt, was man bei Labelbox NICHT erkannt hat
    STANDARD_KLASSE :str = "nicht-erkannt"

    if isdir:
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
        except error as e:
            return 1
        
        for i in range(len(data)):
            keys = [key for key in data[i]]
            for key in keys:
                if key == "Label":
                    pics += 1

                    for obj in data[i][key]["object"]:
                        objects += 1

                        #if "klasse" not in obj or obj["klasse"] == None:
                        if "label-klasse" not in obj or obj["label-klasse"] == None:
                            #obj["klasse"] = STANDARD_KLASSE
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
        
        print(f"\nDatei: {file}\n{pics} Bilder bearbeitet, {objects} Objekte gefunden, wobei {labels_not_set} nicht gelabelt! (~{round(labels_not_set/objects*100, 3)}% fehlerhaft!)\n")

        with open(file, "w") as json_out:
            json.dump(data, json_out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Es muss der zu standardisierende (und bereits minimierte!) JSON-Export angegeben werden!\n")
        exit(1)
    elif len(sys.argv) > 2:
        print("Nur eine minimierte JSON-Datei angeben oder ein ganzes Verzeichnis!\n")
        exit(1)
    else:
        path :str = sys.argv[1]
        if os.path.isdir(path):
            status :int = standardize(path, True)
        elif os.path.isfile(path) and not os.path.isdir(path):
            status :int = standardize(path)
        
        if status == 1:
            print("Es ist irgendein Fehler mit der Verarbeitung aufgetreten!\n")
            exit(1)
        elif status == 2:
            print("Es wurden keine JSON-Dateien gefunden!\n")
            exit(1)
        else:
            print("Die Datei(en) wurden standardisiert!\n")
                