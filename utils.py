#!/usr/bin/env python
# coding=utf-8

import os


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        yield files


for index, file in enumerate(file_name("yummy")):
    if index < 10:
        print(file)
    else:
        break

