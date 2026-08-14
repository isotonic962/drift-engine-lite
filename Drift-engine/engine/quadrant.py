class QuadrantClassifier:
    """
    Classifies output into quadrants based on texture axes.

    Axes (replacing old volatility/entropy):
        x-axis: action_pct      (physical action density)
        y-axis: interiority_pct (named interiority density)

    Quadrants:
        Q1 -- High action + High interiority  -> CONFLICTED
        Q2 -- Low action  + High interiority  -> EXPRESSIVE DRIFT
        Q3 -- High action + Low interiority   -> NOMINAL
        Q4 -- Low action  + Low interiority   -> FLAT

    Thresholds derived from Moberg benchmark:
        action spike:      35.0  (1.5x corridor midpoint)
        action floor:      12.0
        interiority spike: 15.0  (near corridor ceiling of 17.0)
    """

    def __init__(self, action_spike=35.0, action_floor=12.0, interiority_spike=15.0):
        self.action_spike = action_spike
        self.action_floor = action_floor
        self.interiority_spike = interiority_spike

    def classify(self, action_pct, interiority_pct):
        high_action = action_pct > self.action_spike
        low_action = action_pct < self.action_floor
        high_interiority = interiority_pct > self.interiority_spike

        if high_action and high_interiority:
            return {
                "quadrant": "Q1",
                "label": "conflicted",
                "action": "downweight_expressive",
                "description": (
                    "High action + high interiority. Model is grounding scenes "
                    "physically but also naming emotional states. Strip interiority."
                )
            }
        elif high_interiority:
            return {
                "quadrant": "Q2",
                "label": "expressive_drift",
                "action": "prevent_truncation",
                "description": (
                    "Low action + high interiority. Model has lost physical grounding. "
                    "Hard intervention -- strip and flag for correction next turn."
                )
            }
        elif low_action and not high_interiority:
            return {
                "quadrant": "Q4",
                "label": "flat",
                "action": "allow_texture",
                "description": (
                    "Low action, low interiority. Output is neutral/inert. "
                    "Allow slightly more expressive texture."
                )
            }
        else:
            return {
                "quadrant": "Q3",
                "label": "nominal",
                "action": "default",
                "description": (
                    "Action and interiority within target range. "
                    "Default constrained generation."
                )
            }