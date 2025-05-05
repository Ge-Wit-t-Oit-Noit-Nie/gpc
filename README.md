# GPC

De Ge Wit't Oit Noit Nie Programma Compiler!

## Programma

Een programma wordt geschreven in een textfile. Deze kan een willekeurige extentie hebben, maar ```.gpc``` is de standaard.

Een programma bestaat uit een [instructie](./instructieset.md) per regel.

Als voorbeeld:

```txt
BEGIN_EINDE_PROGRAMMA_INDEX (0x0007)
WACHTEN (0x05DC)
ZET_PORT_AAN (PORTNR=0x01, HSIO=0x00)
ZET_PORT_UIT (PORTNR=1, HSIO=0)
FLIP_POORT (PORTNR=0x01, HSIO=0x01)
BEWAAR_STATUS
SPRING (0x0002)
STOPPEN
```

In dit programma, worden de volgende stappen uitgevoerd:

1. Bewaar de positie van voor het einde van de programma (instructie 8)
2. Wacht voor 1500ms
3. Zet de IO port 1 op hoog
4. Zet de IO port 1 op laag
5. Flip de high-speed IO port 1
6. bewaar de status (telemetry)
7. spring terug naar de 2de instructie
8. stop het programma

## Python

Voor de compiler gebruiken we een virtuele python omgeving.

```ps1
.\.venv\Scripts\activate.ps1
```

### Virtual env aanmaken

Dit kan gedaan worden met de volgende commande:

```ps1
python -m venv .venv
```
