#!/usr/bin/env python3
from __future__ import annotations
import csv
from osgeo import ogr


ogr.UseExceptions()


def read_csv() -> list[tuple[str]]:
    with open("in.csv", "r") as f:
        return list(csv.reader(f))


def write_output(rows):
    ogrdriver = ogr.GetDriverByName("SQLITE")
    ds = ogrdriver.CreateDataSource("out-gdal.sqlite")
    lyr = ds.CreateLayer(
        "out-gdal.sqlite",
        None,
        ogr.wkbNone,
    )
    for fieldname in ("anzsic06", "Area", "year", "geo_count", "ec_count"):
        fd = ogr.FieldDefn(fieldname, ogr.OFTString)
        fd.SetWidth(10)
        lyr.CreateField(fd)
    layer_defn = lyr.GetLayerDefn()
    for row in rows:
        ogr_feature = ogr.Feature(layer_defn)

        for i, value in enumerate(row):
            ogr_feature.SetField(i, value)

        lyr.CreateFeature(ogr_feature)


def main():
    rows = read_csv()
    write_output(rows)


if __name__ == "__main__":
    main()
