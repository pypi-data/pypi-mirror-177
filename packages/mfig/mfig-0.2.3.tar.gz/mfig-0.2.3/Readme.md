## `mfig`: A tool for merging multiple figures into one
[![Alt text](https://img.shields.io/pypi/v/kfutils.svg)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/pyversions/kfutils.svg)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/dw/kfutils.svg)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/l/kfutils.svg)](https://pypi.org/project/kfutils/)
[![Alt text](https://img.shields.io/pypi/status/kfutils.svg)](https://pypi.org/project/kfutils/)


### Installation 
Download and install the latest package from the [release section](https://github.com/Koushikphy/mfig/releases/latest) or directly by pip
```
pip install mfig
```

__Prerequisite__  
1. Working LaTeX environment with `pdflatex` and necessary packages. Install `texlive-latex-extra`.
2. `pdfcrop`. Install `texlive-extra-utils`.



### Usage
Run the installed `mfig` utility to use this tool. Description of different arguments, can also be checked with `mfig -h` option. Check the [example section](example/Readme.md) for details usage.


| Argument    |  Description|
| ----------- | ----------- 
|    `-i`     | List of input figures |
|    `-o`     | Output file name  | 
|    `-it`    | Position of the subfigure index, possible values are: <br> `i` (inner), <br>`b` (bottom), <br>`t` (top-right corner),<br> `n` (no index) |
|    `-ir`    | Number of figures in one row |
|    `-w`     | Width of each figures. |
|    `-v`     | Vertical space between each rows |
|    `-s`     | Shift as x,y coordinate in position <br> for inner index type option |
