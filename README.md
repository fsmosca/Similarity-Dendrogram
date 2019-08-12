# Similarity-Dendrogram
Plot dendrogram on chess engines similarity. The script will read a csv similarity output from simex program.

See dendrogram.csv for similarity matrix values.
![](https://i.imgur.com/nF1rowi.png)

### Requirements
* Python 3  
* scipy  
* matplotlib  
* numpy

### How to run
* Command line  
`python similaritydendrogram.py --input dendrogram.csv --output simex.png`

* Help  
```
usage: similaritydendrogram.py [-h] --input INPUT [--output OUTPUT]
                               [--method METHOD] [--figx FIGX] [--figy FIGY]
                               [--plotx PLOTX] [--dpi DPI] [--log]

Read engine similarity matrix and output dendrogram.

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    input similarity matrix file
  --output OUTPUT  output dendrogram image file,
                   default=similarity_dendrogram.png
  --method METHOD  input distance method [ward, complete, single, average,
                   weighted, centroid, median], default=ward
  --figx FIGX      input figure x value length, default=10
  --figy FIGY      input figure y value length, default=9
  --plotx PLOTX    input plot x value length, default=None
  --dpi DPI        input image dpi, default=300
  --log            Records program logging

Similarity Dendrogram v0.3
```
### Credits
* Similarity Tester version 03  
https://komodochess.com/downloads.htm
* SIMEX  
http://rebel13.nl/misc/simex.html

