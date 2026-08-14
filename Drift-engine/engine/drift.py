class DriftScorer:
    """
    Scores drift as deviation from the Moberg texture profile,
    calibrated on p10-p90 range across 10 real chapters.

    All texture metrics are corridor-scored: penalize only when a
    chapter falls outside Moberg's own observed range for that metric.
    Interiority was originally treated as a one-sided ceiling, but a
    10-chapter sample shows it swings 0-17% by scene type (introspective
    chapters run high) -- so it's now a corridor like everything else.

    Figurative density remains the one true one-sided metric: Moberg's
    own max across 10 chapters is 0.17, and there's no scene type where
    heavy figurative language is expected, so anything meaningfully
    above that ceiling is a real anchor violation, not scene variance.

    Corridors derived from p10-p90 across 10 chapters:
        action_pct:       19.5 - 38.7
        dialogue_density:  2.2 - 15.1
        neutral_pct:      56.8 - 75.0
        sentence_rhythm:   8.4 - 15.2
        interiority_pct:   0.0 - 17.0  (floor=0: anchor wants less interiority, never more)

    ch4 (0% dialogue) and ch5 (17% action) score nonzero -- accepted as noise.
    Both fall well under the stable threshold of 5.4. Do not patch corridors
    to zero them out; that is curve-fitting, not calibration.

    Entropy floor set from per-chapter observed minimum (7.29),
    not the full-book figure (9.58) which is not comparable.
    """

    CORRIDORS = {
        "action_pct":       (19.5, 38.7),
        "dialogue_density": (2.2,  15.1),
        "neutral_pct":      (56.8, 75.0),
        "sentence_rhythm":  (8.4,  15.2),
        "interiority_pct":  (0.0,  17.0),
    }

    ONE_SIDED = {
        "figurative_density": 0.17,
    }

    WEIGHTS = {
        "interiority_pct":    1.0,
        "figurative_density": 1.5,
        "action_pct":         0.5,
        "dialogue_density":   0.5,
        "neutral_pct":        0.2,
        "sentence_rhythm":    0.2,
    }

    ENTROPY_FLOOR = 7.29

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