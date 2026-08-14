from .entropy import EntropyCalculator


class DriftAnalyzer:
    """
    Computes entropy for use as a minor independent signal in DriftScorer.

    SentimentAnalyzer has been removed from this pipeline.
    It scored Moberg's own prose at drift 1182 -- the signal was wrong.
    Sentiment and volatility are now replaced by texture deviation
    (see drift.py). Entropy is retained because it is computed
    independently of the sentiment lexicon and behaved correctly
    on the Moberg benchmark (9.58, stable).

    SentimentAnalyzer is still used internally by OutputTruncator
    for per-sentence volatility scoring during truncation -- that
    is a separate job and is not affected by this change.
    """

    def __init__(self):
        self.entropy = EntropyCalculator()

    def analyze(self, text):
        e = self.entropy.analyze(text)
        return {
            "entropy": e["entropy"]
        }