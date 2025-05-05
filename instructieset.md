# Instructieset

De volgende instructies zijn beschikbaar:

* ZET_PORT_AAN (PORTNR=, HSIO=)
* ZET_PORT_UIT (PORTNR=, HSIO=)
* SPRING (INDEX)
* BEWAAR_STATUS
* BEGIN_EINDE_PROGRAMMA_INDEX (INDEX=)
* WACHTEN (ms)
* STOPPEN

## Scribbles

We hebben zeker niet meer als 16 instructies:

* SET_IO
* TOGGLE_IO
* JUMP
* STR_TELEMETRY
* STR_INDEX_SHUTDOWN
* PAUZE

Binnen deze instructies hebben we nog een aantal varianten:

* IO kan in zowel gewone IO (0-16) en HSIO gaan (0-12)
* JUMP kan voorwaarts en terug uit gaan.

Al met al, zeer beperkte set van mogelijkheiden. Als ik dit uitzet in een tabel, dan kan ik alles wat we willen modeleren in een model waarbij we 16 bits per instructie nodig hebben. Door hoogste 4 bits te reserveren voor de opcode kan ik alle opcodes kwijt. Dan blijft er nog 0xFFF aan ruimte over om de rest te coderen. Voorbeeld:

SET_IO MASK
   OPCODE 0x1000 (0b0001 0000 0000 0000)
   HSIO   0x0200 (0b0000 0010 0000 0000)
   HIGH   0x0100 (0b0000 0001 0000 0000)
   PORT   0x001F (0b0000 0000 0001 1111)

TOGGLE_IO MASK
   OPCODE 0x2000 (0b0002 0000 0000 0000)
   HSIO   0x0200 (0b0000 0010 0000 0000)
   PORT   0x001F (0b0000 0000 0001 1111)

Zoals je hier kan zien, heb ik zowel de hoge als lage snelheid poorten als ook de status (in geval van SET). Dit zou onze mogelijkheid voor het geheugen gebruik (al dan niet reduceren) enorm helpen.
wat denk je hier van?

ps: Dit is bij het programmeren wel iets meer controle, maar ik denk dat dit te overzien is. Sterker nog, ik heb een parser geschreven waarmee ik dit kan automatiseren: Je kan dan een TXT file inlezen en er komt een binary file uit die direct in het geheugen kan.

Het programma kan er dan ongeveer zo uit zien:
