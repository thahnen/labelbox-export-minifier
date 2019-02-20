#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json


def minify(path, isdir=False) -> int:
    # Die Elemente, die wir behalten wollen:
    labels = ["Label", "Project Name", "External ID"]

    if isdir:
        files = [
            path+n for n in os.listdir(path) if (
                os.path.isfile(os.path.join(path, n)) and n.endswith(".json")
            )
        ]

        if len(files) == 0:
            return 2
    else:
        files = [path]

    for file in files:
        print(f"Input-Datei: {os.getcwd() + '/' + file}")

        try:
            data = json.load(open(file))

            # Überprüfen, ob Liste vorliegt (so normal von Labelbox) und gefüllt
            assert(type(data) == list)
            assert(len(data) > 0)

            # Überprüfen, ob all die Elemente, die drin bleiben sollen drin sind!
            assert(
                set(labels).issubset(set([
                    key for key in data[0]
                ]))
            )
        except error as e:
            #print(f"Verantwortlicher Fehler: {e}")
            return 1
        
        for i in range(len(data)):
            keys = [key for key in data[i]]
            for key in keys:
                if key not in labels:
                    del data[i][key]
        
        file_out_name = os.getcwd() + "/minified/" + data[0]["Project Name"] + ".min.json"
        print(f"Output-Datei: {file_out_name}\n")
        
        with open(file_out_name, "w") as json_out:
            json.dump(data, json_out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Es muss der zu minimierende JSON-Export angegeben werden!\n")
    elif len(sys.argv) > 2:
        print("Nur eine JSON-Datei angeben oder ein ganzes Verzeichnis!\n")
    else:
        path = sys.argv[1]
        if os.path.isdir(path):
            status = minify(path, True)
        elif os.path.isfile(path) and not os.path.isdir(path):
            status = minify(path)
        
        if status == 1:
            print("Es ist irgendein Fehler mit der Verarbeitung aufgetreten!\n")
        elif status == 2:
            print("Es wurden keine JSON-Dateien gefunden!\n")
        else:
            print("Die Datei(en) wurden minimiert!\n")