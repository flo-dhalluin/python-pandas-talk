#!/bin/sh

# "execute" the notebook, and export to html (slides)
jupyter nbconvert --to notebook --execute pandas-talk.ipynb --output pandas-talk-run.ipynb
jupyter nbconvert --to slides pandas-talk-run.ipynb --ExecutePreprocessor.timeout=300

