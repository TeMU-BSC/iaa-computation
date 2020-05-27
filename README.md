Script to compute IAA from brat files.
Allows multiple annotators and multiple labels

### Usage: 
```
python main.py --datapath /path/to/brat/files/ --variables relevant,variables -l non,relevant,labels
```

## Arguments
+ --datapath: path with one subdirectory per annotator (see toy data).
+ --variables: relevant variables in IAA computation. Possible values are: annotator, filename, mark, label, offset, span, code. If we choose "--variables filename,label,span", matches are annotations in the same file, with same label and same text span. It is recommended to always use those three (filename,label,span).
+ -l: labels to ignore when computing IAA. 

### Example:
```
python main.py --datapath toy_data --variables filename,label,span -l NEGADO
```
```
python main.py --datapath toy_data --variables filename,label -l NEGADO
```

