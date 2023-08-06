# wai-annotations-yolo
wai.annotations module for managing YOLO datasets. 

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins
### FROM-YOLO-OD
Reads image object-detection annotations in the YOLO format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
    FROM-YOLO-OD:
      Reads image object-detection annotations in the YOLO format

      Domain(s): Image Object-Detection Domain

      usage: from-yolo-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME] [--seed SEED] [--image-path-rel PATH] [-l PATH]

      optional arguments:
        -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
        -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
        -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
        -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
        -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into
        --seed SEED     the seed to use for randomisation
        --image-path-rel PATH
                        Relative path to image files from annotations
        -l PATH, --labels PATH
                        Path to the labels file
```

### TO-YOLO-OD
Writes image object-detection annotations in the YOLO format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-yolo-od [-c PATH] [-l PATH] [-p] [--annotations-only] [--no-interleave] -o PATH
                  [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  -c PATH, --labels-csv PATH
                        Path to the labels CSV file to write (default: None)
  -l PATH, --labels PATH
                        Path to the labels file to write (default: None)
  -p, --use-polygon-format
                        Outputs the annotations in polygon format rather than bbox one. (default:
                        False)
  --annotations-only    skip the writing of data files, outputting only the annotation files
                        (default: False)
  --no-interleave       disables item interleaving (splitting will occur in runs) (default: False)
  -o PATH, --output PATH
                        output directory to write images and annotations to (default: None)
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits (default: [])
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits (default: [])
```
