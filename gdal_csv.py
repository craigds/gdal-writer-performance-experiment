#!/usr/bin/env python3
from __future__ import annotations
import csv
import io
import zipfile
from osgeo import ogr


ogr.UseExceptions()


def read_csv() -> list[tuple[str]]:
    with zipfile.ZipFile("in.csv.zip", "r") as z:
        with z.open("in.csv", "r") as f:
            return list(csv.reader(io.TextIOWrapper(f, "utf-8")))


def write_csv(rows):
    ogrdriver = ogr.GetDriverByName("CSV")
    ds = ogrdriver.CreateDataSource("out-gdal.csv")
    lyr = ds.CreateLayer(
        "out-gdal.csv",
        None,
        ogr.wkbNone,
    )
    for fieldname in "anzsic06", "Area", "year", "geo_count", "ec_count":
        lyr.CreateField(ogr.FieldDefn(fieldname, ogr.OFTString))
    layer_defn = lyr.GetLayerDefn()
    for row in rows:
        ogr_feature = ogr.Feature(layer_defn)

        for i, value in enumerate(row):
            ogr_feature.SetField(i, value)

        lyr.CreateFeature(ogr_feature)


def main():
    rows = read_csv()
    write_csv(rows)


if __name__ == "__main__":
    main()
