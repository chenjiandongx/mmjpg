#!/usr/bin/env python
# coding=utf-8

import os
import json


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            yield file


def gen_json(paths):
    d = [{"imgSrc": path} for path in paths]
    with open("yummy.json", "w+") as f:
        json.dump(d, f)


if __name__ == "__main__":
    gen_json(file_name('yummy'))
