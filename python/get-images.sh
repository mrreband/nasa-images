#!/bin/bash
cd /Users/mr/repos/nasa-images/python
source venv/bin/activate

python -m apod
python -m iotd
python -m update_readme
