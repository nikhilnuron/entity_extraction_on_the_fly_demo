import spacy
from spacy.matcher import PhraseMatcher
from read_csv import ReadCSV
import numpy as np


def read_entities(file):
    ents = {e['id']: e for e in ReadCSV(file).entities(delimiter='|')}
    return ents


def update_matcher(lookups, matcherr, nlp_model):
    for key, val in lookups.items():
        if val['alias']:
            patterns = [val['name']] + val['alias']
        else:
            patterns = [val['name']]
        if len(patterns) > 0:
            matcherr.add(key, [nlp_model(i) for i in patterns if i])
    return matcherr


def reduce_entities(entities):
    '''
    combine start idxs of duplicate entities
    '''
    list_ = list()
    d = dict()
    for e in entities:
        key = e['id']
        if key not in d:
            d[key] = {k: v for k, v in e.items()}
        else:
            d[key]['start'].extend(e['start'])
            d[key]['start'] = [int(i) for i in np.unique(d[key]['start'])]
    for k, v in d.items():
        list_.append(v)
    return list_


def caller_function(csvFile, textFile, matcher, nlp):
    ents = read_entities(csvFile)
    matcher= update_matcher(ents, matcher, nlp)
    text = textFile
    doc = nlp(text)
    matches = matcher(doc)
    resp = list()
    for id, s, e in matches:
        d = dict()
        rule = nlp.vocab.strings[id]
        d['name'] = doc[s:e].text
        d['label'] = ents[rule]['entity_label']
        d['type'] = ents[rule]['entity_type']
        d['start'] = str(s)
        d['end'] = str(e)
        d['id'] = rule
        resp.append(d)
    return resp


def caller_wrapper(csvFile, textFile):
    nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    return caller_function(csvFile, textFile, matcher, nlp)

# caller_wrapper('rain_demo.csv', 'sitagliptin is the only drug which is named as sitagliptin')