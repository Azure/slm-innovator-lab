#!/bin/bash

SEED_FILE="samples/math_500_tst.json"
COLUMN_NAMES="problem"


python evolve.py --seed_file "$SEED_FILE" --column_names "$COLUMN_NAMES"
# generated results are stored in math_500_tst.[uuid].json