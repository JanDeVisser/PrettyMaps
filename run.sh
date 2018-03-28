#!/bin/sh

export PYTHONPATH=../grumble:. 
script=${1:-"prettymaps/index.py"}

python $script
