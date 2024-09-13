from items.itemCluster.demo.API import *
import os
import csv
import copy
import sys

def run(input_file):
    # @TODO: xlsx格式
    input_file_path = os.path.join("./datadir/uploads", input_file)

    origin_items, modify_items = API(input_file_path)
    return origin_items, modify_items