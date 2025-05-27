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

## ZET_POORT_AAN

De functie ZET_POORT_AAN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0011 0000 0000 0000 | 0x3000 |                   |
| HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |

De POORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.

## ZET_POORT_UIT

De functie ZET_POORT_AAN wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0100 0000 0000 0000 | 0x4000 |                   |
| HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |

De POORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.

## FLIP_POORT

De functie FLIP_POORT wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0101 0000 0000 0000 | 0x5000 |                   |
| HSIO    | 0b0000 0010 0000 0000 | 0x0200 | HSIO (0x0 / 0x01) |
| POORT   | 0b0000 0000 0001 1111 | 0x001F | POORT             |

De POORT is een van de 13 (0-12) gewone IO Poorten of 0-8 HSIO poorten.

## BEWAAR_STATUS

De functie BEWAAR_STATUS wordt als volgt gecodeerd:

| Element | Bitmask               | Hex    | Parameter         |
| ------- | --------------------- | ------ | ----------------- |
| OPCODE  | 0b0110 0000 0000 0000 | 0x6000 |                   |

## SPRING

De functie BEWAAR_STATUS wordt als volgt gecodeerd:

| Element | Bitmask               | Hex   | Parameter                |
| ------- | --------------------- | ----- | ------------------------ |
| OPCODE  | 0b0110 0000 0000 0000 |       |                          |
| INDEX   | 0b0000 1111 1111 1111 | x0FFF | Spring direct naar index |
