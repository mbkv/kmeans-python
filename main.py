#!/usr/bin/env python3

from PIL import Image
import numpy as np
import scipy.cluster as cluster
import argparse

def run_kmeans(i,k_count):
    i = np.copy(i)
    missing = "raise" if k_count < 8 else "warn"
    while True:
        try:
            centroids,values = cluster.vq.kmeans2(i, k_count, iter=20, missing=missing)
            for index,k in enumerate(centroids):
                i[values==index] = k
            return np.uint8(np.reshape(i,(i_img.size[1],i_img.size[0],3)))
        except cluster.vq.ClusterError:
            continue

def get_new_filename(filename, k):
    filename = filename.split('.')
    filename[-2] += '_' + str(k)
    return ".".join(filename)

def run_once(i_arr, output, k_count):
    values = run_kmeans(i_arr, k_count)
    Image.fromarray(values).save(output)

def run_all(i_arr, output):
    for k_count in range(1,16):
        out_file = get_new_filename(output, k_count)

        print("Starting ", k_count)
        run_once(i_arr, out_file, k_count)

    for k_count in range(4,9):
        k_count = 2**k_count
        out_file = get_new_filename(output, k_count)

        print("Starting ", k_count)
        run_once(i_arr, out_file, k_count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform K means progression on an image")
    parser.add_argument('filename', metavar='file', type=str)
    parser.add_argument('-o', '--output', dest="output", metavar='file', type=str, help="Specify the filename to output, otherwise save as same filename with _k at the end, if --all is specified, _k as appended to the filename")
    parser.add_argument('-k', dest="k_count", metavar='k', type=int, help="Specify which value of k to run")
    parser.add_argument('--all', action="store_true", help="Run the image from k=1-16, then 16-256 using only powers of 2")

    args = parser.parse_args()

    filename = args.filename
    i_img = Image.open(filename)
    i_arr = np.array(i_img).reshape((-1,3))
    i_arr = i_arr.astype(float)


    if args.k_count != None:
        if args.output == None:
            output = get_new_filename(args.filename, args.k_count)
        else:
            output = args.output
        run_once(i_arr, output, args.k_count)
    else:
        if args.output == None:
            output = args.filename
        else:
            output = args.output
        run_all(i_arr, output)
