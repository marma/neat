#!/usr/bin/env python3

from sys import stdin, stdout
from cluster import cluster_entities
from transformers import pipeline

nlp = pipeline('ner', model='KB/bert-base-swedish-cased-ner', tokenizer='KB/bert-base-swedish-cased-ner', ignore_labels=[])

def ner(text):
    l = []
    for token in nlp(text):
        if token['word'].startswith('##'):
            l[-1]['word'] += token['word'][2:]
        else:
            l += [ token ]

    l2 = []
    l3 = []
    last_type = None
    for token in l:
        if token['word'] in [ '[CLS]', '[SEP]' ]:
            continue

        if last_type != token['entity'] and l3:
            l2 += [ { 'word': ' '.join([ x['word'] for x in l3 ]),
                      'score': sum([ float(x['score']) for x in l3 ])/len(l3),
                      'entity': last_type } ]
            l3 = [ token ]
        else:
            l3 += [ token ]

        last_type = token['entity']

    l2 += [ { 'word': ' '.join([ x['word'] for x in l3 ]), 'entity': last_type } ]

    return [ x for x in l2 if x['word'] and x['entity'] != 'O' ]


def chunker(i):
    w=[]
    for line in i:
        t = (line[:-1] if line[-1] == '\n' else line).split()
        
        if len(w) + len(t) > 128:
            yield ' '.join(w)
            w = t
        else:
            w += t

    yield ' '.join(w)

if __name__ == '__main__':
    entities = []
    for chunk in chunker(stdin):
        entities += ner(chunk)

    clusters = cluster_entities(entities)

    print(entities)
    print()
    print(clusters)

