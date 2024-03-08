#!/bin/bash
source activate

python -m apod apod.py >> apod.log
python -m iotd iotd.py >> iotd.log
