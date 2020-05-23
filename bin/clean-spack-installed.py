#!/usr/bin/env python

import argparse
import json
import os


def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--lock-file', dest='lock_files', action='append')
    parser.add_argument('--keep', action='store_true', default=False)
    parser.add_argument('install_dirs', nargs='+')
    args = parser.parse_args()
    installed_hashes = {}
    for install_dir in args.install_dirs:
        for package_dir in os.listdir(install_dir):
            full_path = os.path.realpath(os.path.join(install_dir, package_dir))
            installed_hash = package_dir.split('-')[-1]
            installed_hashes[installed_hash] = full_path

    locked_hashes = set()
    for lock_file in args.lock_files:
        with open(lock_file) as fp:
            lock_file_json = json.load(fp)
            for locked_hash in lock_file_json['concrete_specs'].keys():
                locked_hashes.add(locked_hash)
    if args.keep:
        for keep_hash in set(installed_hashes.keys()) & locked_hashes:
            print(installed_hashes[keep_hash])
    else:
        for clean_hash in set(installed_hashes.keys()) - locked_hashes:
            print(installed_hashes[clean_hash])
                    


if __name__ == '__main__':
    main()
