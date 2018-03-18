#!/bin/sh

# "execute" the notebook, and export to html (slides)
jupyter nbconvert --to slides --execute pandas-talk.ipynb --ExecutePreprocessor.timeout=300
# push slides to ftp ?
