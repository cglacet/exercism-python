from operator import itemgetter
#from itertools import islice

def sorted_indexes(iterable):
    sort_options = dict(key=itemgetter(1), reverse=True)
    return (i for i, _ in sorted(enumerate(iterable), **sort_options))

def islice(iterable, n):
    for i, e in enumerate(iterable):
        if i >= n:
            return
        yield e

class HighScores(object):
    def __init__(self, scores):
        self.scores = scores
        self.ranks = list(sorted_indexes(scores))

    def latest(self):
        return self.scores[-1]

    def personal_best(self):
        return next(self.top())

    def personal_top_three(self):
        #return list(islice(self.top(), 3))
        return list(self.top())[:3]

    def top(self):
        return (self.scores[i] for i in self.ranks)
