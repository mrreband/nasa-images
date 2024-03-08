#!/bin/bash
source activate

python -m apod apod.py
python -m iotd iotd.py
