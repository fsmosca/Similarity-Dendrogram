# Similarity-Dendrogram
Plot dendrogram on chess engines similarity. The script will read matrix.txt a similarity output from sim or simex program.

Test epd: midgame.epd  
Movetime: 100 millisec or 0.1 sec
![](https://i.imgur.com/j2PCIrB.png)

### Requirements
* Python 3  
* scipy  
* matplotlib  

### How to run
* Command line
1. If using an output from simex  
`python similaritydendrogram.py --input dendrogram.csv --output simex.png`  
2. If using an output from sim  
`python similaritydendrogram.py --input matrix.txt --output sim.png --sim`

### Credits
* Similarity Tester version 03  
https://komodochess.com/downloads.htm
* SIMEX  
http://rebel13.nl/misc/simex.html

