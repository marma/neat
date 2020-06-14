#!/usr/bin/env python3

from sys import stdin, stdout
from fuzzywuzzy.fuzz import ratio, partial_token_sort_ratio


def match(s1, s2):
    return distance(s1, s2) > 0.8


def distance(s1, s2):
    return partial_token_sort_ratio(s1, s2) / 100


def cluster(lines):
    lines = sorted(lines, reverse=True, key=lambda x: len(x))
    ret = []

    while len(lines) > 0:
        key = lines.pop(0)
        c = [ key, [ key ] ]

        i=0
        while len(lines) > i:
            if match(key, lines[i]):
                d = lines.pop(i)

                if d not in c[1]:
                    c[1] += [ d ]
            else:
                i += 1

        ret += [ c ]

    return ret


def cluster_entities(entities):
    entities = sorted(entities, reverse=True, key=lambda x: len(x['word']))
    ret = []

    while len(entities) > 0:
        entity = entities.pop(0)
        c = [ entity['word'], [ entity ] ]

        i=0
        while len(entities) > i:
            if match(c[0], entities[i]['word']):
                c[1] += [ entities.pop(i) ]
            else:
                i += 1

        ret += [ c ]

    return ret


if __name__ == '__main__':
    c = cluster([ x[:-1] for x in stdin ])

    for x in c:
        print(f'{x[0]} - {x[1]}')

