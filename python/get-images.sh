#!/bin/bash
cd $HOME/repos/nasa-images/python
source venv/bin/activate

python -m apod
python -m iotd
python -m update_readme

git checkout main
git add ../README.md
git commit -m "set today's images"
git push
