#!/usr/bin/env python3
# Fra Espens dårlige verktøykasse
import json
import sys
import os

def kommando(a):
    """Dette er dokumentasjonen du får"""
    stream = os.popen(a)
    output = stream.read()
    return output

# Leser fil og greier
def prettyprint():
    try:    
        with open(sys.argv[1], 'r') as datafil: 
            innholdString = datafil.read() 
            innholdJson = json.loads(innholdString) 
            innrykk = int(sys.argv[2]) 
            return json.dumps((innholdJson), indent=innrykk)

    except Exception: # (FileNotFoundError,IndexError,ValueError)
        print ("Pretty JSON 0.2\nSyntax: pj <filename> <indent>")
        print ("\nDebug info: " + (kommando("whoami")) + (kommando("date +%FT%X")))

def main():
    print (prettyprint())

main()