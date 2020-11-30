#!/usr/bin/env python
# coding: utf-8

import os
import multiprocessing as mp

assetPath = "assets/"

def filter_file(filename):
    """ Extracts all strings that begin with an 'r' from the specified file, returning the results as a set.

    params: the name of the file to parse
    returns: A set of strings that begin with r
    """

    filepath = assetPath + filename

    filtered_strings = set()

    with open(filepath, 'rb') as f:
        for line in f:
            if line[:1] == b'r':
                filtered_strings.update([line.decode("utf-8")])

    return filtered_strings 


def filter_multiple_files_in_parallel(filenames): 
    """ Extracts all strings that begin with an 'r' from multiple files in parallel, asynchronously, merging the results.

    param: a list of filenames to extract strings from
    returns: A list of strings that begin with r without duplicates
    """

    pool = mp.Pool()
    r = pool.map_async(filter_file, filenames)

    results = set()
    for partial_result in r.get():
        for string in partial_result:
            results.update([string])

    # Needed to terminate the opened processes
    pool.close()
    pool.join()

    return list(results)



if __name__ == "__main__":
    print("Starting list filterer...")

    try:
        filenames = os.listdir(assetPath)
        print(f"{len(filenames)} files found in {assetPath}")

        filtered_list = filter_multiple_files_in_parallel(filenames)

        result_path = assetPath + 'filtered_strings.txt'
        with open(result_path, 'w') as f:
            f.writelines(filtered_list)
            print(f"results written to {result_path}")

    except:
        print(f"Could not find folder {assetPath} when looking in {os.getcwd()}.\nPlease ensure this folder exists and contains the files of interest")

