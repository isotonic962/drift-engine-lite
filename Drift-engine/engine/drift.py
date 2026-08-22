class DriftScorer:
    """
    Scores drift as deviation from the Moberg texture profile.

    Corridors derived from p10-p90 across 16 full chapters of The Emigrants
    (clean digital PDF), measured with the original lexicon.py PHYSICAL_VERBS
    set and a patched _split_sentences() (curly-quote lookahead + min-length
    filter -- see texture.py). Verified against verify_scorer's hand-checked
    passages. Residual action_pct/interiority_pct delta (~9pp/4pp) vs
    verify_scorer is expected: verify_scorer's entries are short hand-picked
    passages, not full chapters -- not a classifier bug, no further action
    needed on that gap. Re-validate once real Qwen3-14B generation output
    exists (Kaggle run) -- these corridors have not yet been checked against
    actual model output, only against real Moberg prose.

    All texture metrics are corridor-scored: penalize only when a
    chapter falls outside Moberg's own observed range for that metric.

    Figurative density remains the one true one-sided metric: Moberg's
    own p90 across 16 chapters is 0.15, and there's no scene type where
    heavy figurative language is expected, so anything meaningfully
    above that ceiling is a real anchor violation, not scene variance.

    Prior corridors (10-chapter sample, pre-lexicon-fix) are superseded.
    The old neutral_pct corridor in particular was measuring a lexicon bug:
    an earlier benchmark pass had misclassified speech/perception verbs
    (said, told, asked, looked...) as physical action, which collapsed
    neutral_pct and inflated action_pct. Fixed by keeping lexicon.py's
    original ~80-verb PHYSICAL_VERBS set untouched.

    Entropy floor set from the 16-chapter p10 (8.05); both old and new
    sentence-splitter classifiers agree on this within noise.
    """

    CORRIDORS = {
        "action_pct":       (17.0, 27.0),
        "dialogue_density": (0.5,  20.0),
        "neutral_pct":      (65.0, 75.0),
        "sentence_rhythm":  (9.4,  12.0),
        "interiority_pct":  (7.0,  12.0),
    }

    ONE_SIDED = {
        "figurative_density": 0.15,
    }

    WEIGHTS = {
        "interiority_pct":    1.0,
        "figurative_density": 1.5,
        "action_pct":         0.5,
        "dialogue_density":   0.5,
        "neutral_pct":        0.2,
        "sentence_rhythm":    0.2,
    }

    ENTROPY_FLOOR = 8.05

    def __init__(self):
        pass

    def _one_sided_penalty(self, actual, target):
        """Penalize only when actual exceeds target. Below target = 0."""
        return max(0.0, actual - target)

    def _corridor_penalty(self, actual, low, high):
        """Penalize only when actual falls outside [low, high]. Inside = 0."""
        if actual < low:
            return low - actual
        elif actual > high:
            return actual - high
        return 0.0

    def score(self, texture, entropy=0.0):
        """
        Args:
            texture: dict from TextureAnalyzer.analyze()
            entropy: float from EntropyCalculator.analyze()["entropy"]

        Returns dict with per-component deviations and final drift_score.
        """
        components = {}
        drift = 0.0

        for key, target in self.ONE_SIDED.items():
            actual = texture.get(key, 0.0)
            penalty = self._one_sided_penalty(actual, target)
            weight = self.WEIGHTS[key]
            components[f"{key}_dev"] = round(penalty, 3)
            drift += penalty * weight

        for key, (low, high) in self.CORRIDORS.items():
            actual = texture.get(key, 0.0)
            penalty = self._corridor_penalty(actual, low, high)
            weight = self.WEIGHTS[key]
            components[f"{key}_dev"] = round(penalty, 3)
            drift += penalty * weight

        entropy_penalty = max(0.0, self.ENTROPY_FLOOR - entropy)
        entropy_component = round(entropy_penalty * 0.3, 4)
        components["entropy_component"] = entropy_component
        drift += entropy_penalty * 0.3

        components["drift_score"] = round(drift, 4)
        return components