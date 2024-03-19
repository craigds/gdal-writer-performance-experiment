#!/bin/bash
set -eux
clang -O0 $(gdal-config --libs) $(gdal-config --cflags) gdal_csv.c -o gdal_csv_c
