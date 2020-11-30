# KB List Filterer

## Uppgift
Skriv ett parallelliserat program som går igenom ett antal listor med strängar (varje lista finns i en separat indatafil). Programmet ska producera en ny lista innehållande alla strängar ur indatalistorna som börjar med bokstaven 'r'. Den producerade listan ska vara fri från dubbletter. Utgå från att listorna skulle kunna vara väldigt långa (fastän din faktiska indata är liten). Du kan anta att strängarna i listorna är korta och antalet listor är litet samt att den slutgiltiga listan blir kort.

## Run
* Navigera till samma mapp som denna README
* python KBfilter.py

## Beskrivning av lösningen

Programmet skapar en lista över alla filer i folder ./assets/

Därefter skapas en pool av arbetare som asynkront läser filerna parallelt. Eftersom listorna kan antas vara långa är overheaden som paralleliseringen innebär försumbar.

Varje arbetare läser sin respektive fil i byte-mode för snabbhet, och returnerar en mängd av alla strängar som börjar med 'r'.

(Anledningen till att vi använder mängder istället för listor är för att direkt undvika dubbletter. Detta har även fördelen att sammanslagningen av resultaten blir mer effektiv; minne behöver inte skapas för en (potentiellt) enorm lista med dubbletter.)

Resultaten sätts ihop till en mängd, konverteras till en lista i enlighet med uppgiftsspecifikationen, och skrivs till ./assets/filtered\_strings.txt

## Requirements
Pythons standardbibliotek.

Testat med Python 3.7.5

