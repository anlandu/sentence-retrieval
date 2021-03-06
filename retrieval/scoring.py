from whoosh.scoring import WeightingModel, WeightLengthScorer
from math import log

# OkBM25 Model

def ok_bm25(df, N, tf, fl, avgfl, B, K1):
    # df - document frequency
    # N - total number of documents 
    # tf - term frequency in the current document
    # fl - field length in the current document
    # avgfl - average field length across documents in collection
    # B, K1 - free paramters

    return log((N-df+0.5)/(df+0.5)) * ((tf * (K1 + 1)) / (tf + K1 * ((1 - B) + B * fl / avgfl)))


class OkBM25(WeightingModel):
    """Implements the OkBM25 scoring algorithm.
    """

    def __init__(self, B=0.75, K1=1.2, **kwargs):
        """

        >>> from whoosh import scoring
        >>> # Set a custom B value for the "content" field
        >>> w = scoring.OkBM25(B=0.75, K1=1.5)

        :param B: free parameter, see the BM25 literature.
        :param K1: free parameter, see the BM25 literature.
        """

        self.B = B
        self.K1 = K1

    def supports_block_quality(self):
        return True

    def scorer(self, searcher, fieldname, text, qf=1):
        B = self.B

        return OkBM25Scorer(searcher, fieldname, text, B, self.K1, qf=qf)


class OkBM25Scorer(WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, B, K1, qf=1):
        # IDF and average field length are global statistics, so get them from
        # the top-level searcher
        parent = searcher.get_parent()  # Returns self if no parent
        self.df = parent.doc_frequency(fieldname, text)
        self.N = parent.doc_count_all()
        self.idf = parent.idf(fieldname, text)
        self.avgfl = parent.avg_field_length(fieldname) or 1

        self.B = B
        self.K1 = K1
        self.qf = qf
        self.setup(searcher, fieldname, text)

    def _score(self, weight, length):
        s = ok_bm25(self.df, self.N, weight, length, self.avgfl, self.B, self.K1)
        return s

# Pivoted Length Normalization Model

def pln(df, N, tf, fl, avgfl, s):
    # df - document frequency
    # N - total number of documents 
    # tf - term frequency in the current document
    # fl - field length in the current document
    # avgfl - average field length across documents in collection
    # s - free paramters

    return log((N+1)/df) * tf * ((1 + log(1 + log(tf))) / ((1 - s) + s * fl / avgfl))


class PLN(WeightingModel):
    """Implements the Pivoted Length Normalization scoring algorithm.
    """

    def __init__(self, s=0.75, **kwargs):
        self.s = s

    def supports_block_quality(self):
        return True

    def scorer(self, searcher, fieldname, text, qf=1):
        return PLNScorer(searcher, fieldname, text, self.s, qf=qf)


class PLNScorer(WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, s, qf=1):
        # IDF and average field length are global statistics, so get them from
        # the top-level searcher
        parent = searcher.get_parent()  # Returns self if no parent
        self.df = parent.doc_frequency(fieldname, text)
        self.N = parent.doc_count_all()
        self.idf = parent.idf(fieldname, text)
        self.avgfl = parent.avg_field_length(fieldname) or 1

        self.s = s
        self.qf = qf
        self.setup(searcher, fieldname, text)

    def _score(self, weight, length):
        s = pln(self.df, self.N, weight, length, self.avgfl, self.s)
        return s
