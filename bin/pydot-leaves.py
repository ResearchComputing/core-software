#!/usr/bin/env python

from __future__ import print_function

import argparse
import pydot
import sys


QUOTES="\"'"


def main ():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    for graph in pydot.graph_from_dot_data(sys.stdin.read()):
        nodes = set(node.get_name().strip(QUOTES) for node in graph.get_nodes() if node.get_label())
        destinations = set(edge.get_destination().strip(QUOTES) for edge in graph.get_edges())
        for node in nodes - destinations:
            print(node)


if __name__ == '__main__':
    main()
