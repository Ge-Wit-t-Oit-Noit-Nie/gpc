# Instructieset

De volgende instructies zijn beschikbaar:

- [Instructieset](#instructieset)
  - [STOPPEN](#stoppen)
  - [BEGIN\_EINDE\_PROGRAMMA\_INDEX](#begin_einde_programma_index)
  - [Wachten](#wachten)
  - [ZET\_PORT\_AAN](#zet_port_aan)
  - [ZET\_PORT\_UIT](#zet_port_uit)
  - [FLIP\_POORT](#flip_poort)
  - [BEWAAR\_STATUS](#bewaar_status)
  - [Scribbles](#scribbles)

## STOPPEN

De functie STOPPEN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter |
| ------- | --------------------- | ------ | --------- |
| OPCODE  | 0b0000 0000 0000 0000 | 0x0000 |           |

Deze functie is by default ingevult in het geheugen.

## BEGIN_EINDE_PROGRAMMA_INDEX

De functie BEGIN_EINDE_PROGRAMMA_INDEX wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter |
| ------- | --------------------- | ------ | --------- |
| OPCODE  | 0b0001 0000 0000 0000 | 0x1000 |           |
| DELAY   | 0b0000 1111 1111 1111 | 0x0FFF | INDEX     |

De maximale index is dus 4095

## Wachten

De functie WACHTEN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter |
| ------- | --------------------- | ------ | --------- |
| OPCODE  | 0b0010 0000 0000 0000 | 0x2000 |           |
| DELAY   | 0b0000 1111 1111 1111 | 0x0FFF | DELAY     |

De maximale delay is dus 4095 ms

## ZET_PORT_AAN

De functie ZET_PORT_AAN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0011 0000 0000 0000 | 0x3000 |                   |
| HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| HIGH    | 0b0000 0001 0000 0000 | 0x0100 |                   |
| PORT    | 0b0000 0000 0001 1111 | 0x001F | PORTNR            |

De PORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.

## ZET_PORT_UIT

De functie ZET_PORT_AAN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0100 0000 0000 0000 | 0x4000 |                   |
| HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| HIGH    | 0b0000 0001 0000 0000 | 0x0100 |                   |
| PORT    | 0b0000 0000 0001 1111 | 0x001F | PORTNR            |

De PORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.

## FLIP_POORT

De functie FLIP_POORT wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0101 0000 0000 0000 | 0x5000 |                   |
| HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| PORT    | 0b0000 0000 0001 1111 | 0x001F | PORTNR            |

De PORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.

## BEWAAR_STATUS

De functie BEWAAR_STATUS wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0110 0000 0000 0000 | 0x6000 |                   |

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
