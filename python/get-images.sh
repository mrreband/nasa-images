#!/bin/bash
cd $HOME/repos/nasa-images/python
source venv/bin/activate

python -m apod
python -m iotd
