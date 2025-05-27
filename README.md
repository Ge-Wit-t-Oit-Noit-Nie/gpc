# GPC

De Ge Wit't Oit Noit Nie Programma Compiler!

## Programma

Een programma wordt geschreven in een textfile. Deze kan een willekeurige extentie hebben, maar ```.gpc``` is de standaard.

Een programma bestaat uit een [instructie](./instructieset.md) per regel.

Als voorbeeld:

```txt
BEGIN_EINDE_PROGRAMMA_INDEX (index=0x0007);
ZET_POORT_AAN (POORT=0x00, HSIO=0x00);
ZET_POORT_UIT (POORT=0x01, HSIO=0x00);
WACHTEN (delay=0x05DC);
FLIP_POORT (POORT=0x01, HSIO=1);
BEWAAR_STATUS;
SPRING (index=0x0003);
BEWAAR_STATUS;
STOPPEN;
```

In dit programma, worden de volgende stappen uitgevoerd:

1. Bewaar de positie van voor het einde van de programma (instructie 8)
2. Wacht voor 1500ms
3. Zet de IO poort 1 op hoog
4. Zet de IO port 1 op laag
5. Flip de high-speed IO poort 1
6. bewaar de status (telemetry)
7. spring terug naar de 2de instructie
8. stop het programma

## Compileren

Start een [python](#python-starten) sessie en type het volgende

```ps1
    python src/gpc.py -i <input_file> -o <output_file> -v
```

Met de volgende parameters:

* -i, --input: de broncode die gecompileerd moet worden
* -o, --output: het .bin bestand dat gemaakt wordt
* -v, --verbose: Volg de uitput

### Voorbeeld

```ps1
    python src/gpc.py -i .\examples\simpel_programma_2.gpc -o .\binary_file.bin -v
```

## Python starten

Voor de compiler gebruiken we een virtuele python omgeving.

```ps1
.\.venv\Scripts\activate.ps1
pip install -r requirements.txt
```

### Virtual env aanmaken

Dit kan gedaan worden met de volgende commande:

```ps1
python -m venv .venv
```
