Script to compute IAA from brat files.
Allows multiple annotators and multiple labels

### Usage: 
```
python main.py --datapath /path/to/brat/files/ --variables relevant,variables -l relevant,labels
```

## Arguments
+ --datapath: path with one subdirectory per annotator (see toy data).
+ --variables: relevant variables in IAA computation. Possible values are: annotator, filename, mark, label, offset, span, code. If we choose "--variables filename,label,offset", matches are annotations in the same file, with same label and in the same position in text. It is recommended to always use those three (filename,label,offset).
+ -l: labels to consider when computing IAA. 

### Example:
```
python main.py --datapath toy_data --variables filename,label,offset -l OTROS,T_AP
```
```
python main.py --datapath toy_data --variables filename,label -l OTROS,T_AP
```

