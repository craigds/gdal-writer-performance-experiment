#!/usr/bin/env python3
import csv
import io
import zipfile


def read_csv() -> list[tuple[str]]:
    with zipfile.ZipFile("in.csv.zip", "r") as z:
        with z.open("in.csv", "r") as f:
            return list(csv.reader(io.TextIOWrapper(f, "utf-8")))


def write_csv(rows):
    with open("out-python.csv", "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def main():
    rows = read_csv()
    write_csv(rows)


if __name__ == "__main__":
    main()
