from collections import defaultdict
import heapq
import math

def debug():
    import ipdb
    ipdb.set_trace()

from pydwimmer import terms
from pydwimmer import utilities

index = defaultdict(set)
wordbags = defaultdict(set)
fragment_counts = defaultdict(int)

def frequency(word):
    return len(index[word]) * 1. / len(terms.all_templates)

def fragment_frequency(fragment):
    return fragment_counts[fragment] * 1. / len(terms.all_templates)

def build_index():
    for template in terms.all_templates:
        fragments = set()
        for p in str(template).split():
            for i in range(len(p)+1):
                fragments.add(p[:i])
            index[p].add(template)
            wordbags[template].add(p)
        for fragment in fragments:
            fragment_counts[fragment]+=1

def candidates(s):
    result = []
    for p in s.split():
        #this condition is dumb...
        if frequency(p) < 0.5:
            result.extend(index[p])
    return result

def best_matches(s, n):
    x = s.split()
    if not x:
        return []
    words = set(x[:-1])
    fragment = x[-1]
    templates = candidates(s)
    return heapq.nlargest(n, templates, lambda template : match_quality(template, words, fragment))

def match_quality(template, words, fragment):
    score = 0
    wordbag = wordbags[template]
    for word in wordbag:
        if word in words:
            score += -math.log(frequency(word))
    for word in wordbag:
        if utilities.starts_with([fragment], word):
            score += -math.log(fragment_frequency(fragment))
            break
    return score
