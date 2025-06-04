# Instructieset

De volgende instructies zijn beschikbaar:

- [Instructieset](#instructieset)
- [STOPPEN](#stoppen)
- [BEGIN\_EINDE\_PROGRAMMA\_INDEX](#begin_einde_programma_index)
- [Wachten](#wachten)
- [ZET\_POORT\_AAN](#zet_poort_aan)
- [ZET\_POORT\_UIT](#zet_poort_uit)
- [FLIP\_POORT](#flip_poort)
- [BEWAAR\_STATUS](#bewaar_status)
- [SPRING](#spring)

## Stoppen

Stopt de executie van het programma.

| Element | Bitmask               | Hex    | Parameter |
| ------- | --------------------- | ------ | --------- |
| OPCODE  | 0b0000 0000 0000 0000 | 0x0000 |           |

Deze functie is by default ingevult in het geheugen.

## Pauze

Stopt de executie van enig programma totdat het pauze signaal
weer gezien wordt.

| Element | Bitmask               | Hex    | Parameter |
| ------- | --------------------- | ------ | --------- |
| OPCODE  | 0b0001 0000           | 0x10   |           |

## Wachten

De functie WACHTEN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter |
| ------- | --------------------- | ------ | --------- |
| OPCODE  | 0b0010 0000 0000 0000 | 0x2000 |           |
| DELAY   | 0b0000 1111 1111 1111 | 0x0FFF | DELAY     |

De maximale delay is dus 4095s

## Zet_poort_aan

De functie ZET_POORT_AAN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0011 0000 0000 0000 | 0x3000 |                   |
| STATUS  | 0b0000 0001 0000 0000 | 0x0100 |                   |
| HSIO    | 0b0000 0001 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |

De POORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.
De STATUS wordt gezet door de compiler.

## Zet_poort_uit

De functie ZET_POORT_AAN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0011 0000 0000 0000 | 0x3000 |                   |
| STATUS  | 0b0000 0000 0000 0000 | 0x0000 |                   |
| HSIO    | 0b0000 0001 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |

De POORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.
De STATUS wordt gezet door de compiler.

## Flip_poort

De functie FLIP_POORT wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0100 0000 0000 0000 | 0x4000 |                   |
| HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |

De POORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.

## Bewaar_status

De functie BEWAAR_STATUS wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b011 0000            | 0x50   |                   |

## Spring

De functie SPRING wordt als volgt gecodeerd:

| Element | Bitmask                         | Hex      | Parameter         |
| ------- | ------------------------------- | ------   | ----------------- |
| OPCODE  | 0b0111 0000 0000 0000 0000 0000 | 0x600000 |                   |
| INDEX   | 0b0000 0001 1111 1111 1111 1111 | 0x01FFFF | INDEX             |
