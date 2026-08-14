import sys
sys.path.insert(0, '.')
from engine.drift import DriftScorer

scorer = DriftScorer()

cases = [
    # --- Actual Moberg chapters (all should score 0 or very close) ---
    {"label": "Moberg ch1",  "texture": {"action_pct": 29.5, "interiority_pct": 3.8,  "neutral_pct": 66.7, "dialogue_density": 3.8,  "figurative_density": 0.06, "sentence_rhythm": 11.24}, "entropy": 7.988},
    {"label": "Moberg ch2",  "texture": {"action_pct": 24.4, "interiority_pct": 8.9,  "neutral_pct": 66.7, "dialogue_density": 2.2,  "figurative_density": 0.0,  "sentence_rhythm": 8.4},   "entropy": 7.369},
    {"label": "Moberg ch3",  "texture": {"action_pct": 34.2, "interiority_pct": 5.3,  "neutral_pct": 60.5, "dialogue_density": 10.5, "figurative_density": 0.0,  "sentence_rhythm": 15.2},  "entropy": 7.575},
    {"label": "Moberg ch4",  "texture": {"action_pct": 38.7, "interiority_pct": 0.0,  "neutral_pct": 61.3, "dialogue_density": 0.0,  "figurative_density": 0.17, "sentence_rhythm": 9.47},  "entropy": 7.291},
    {"label": "Moberg ch5",  "texture": {"action_pct": 17.0, "interiority_pct": 17.0, "neutral_pct": 66.0, "dialogue_density": 4.3,  "figurative_density": 0.0,  "sentence_rhythm": 10.46}, "entropy": 7.617},
    {"label": "Moberg ch6",  "texture": {"action_pct": 29.5, "interiority_pct": 13.6, "neutral_pct": 56.8, "dialogue_density": 13.6, "figurative_density": 0.17, "sentence_rhythm": 12.02}, "entropy": 8.065},
    {"label": "Moberg ch7",  "texture": {"action_pct": 31.3, "interiority_pct": 8.4,  "neutral_pct": 60.3, "dialogue_density": 4.6,  "figurative_density": 0.08, "sentence_rhythm": 9.39},  "entropy": 8.073},
    {"label": "Moberg ch8",  "texture": {"action_pct": 19.5, "interiority_pct": 9.8,  "neutral_pct": 70.7, "dialogue_density": 6.5,  "figurative_density": 0.08, "sentence_rhythm": 9.86},  "entropy": 8.037},
    {"label": "Moberg ch9",  "texture": {"action_pct": 34.0, "interiority_pct": 9.4,  "neutral_pct": 56.6, "dialogue_density": 15.1, "figurative_density": 0.0,  "sentence_rhythm": 8.24},  "entropy": 7.570},
    {"label": "Moberg ch10", "texture": {"action_pct": 22.5, "interiority_pct": 2.5,  "neutral_pct": 75.0, "dialogue_density": 10.0, "figurative_density": 0.12, "sentence_rhythm": 11.35}, "entropy": 7.504},

    # --- Engine outputs ---
    {"label": "Engine -- Anders returns",       "texture": {"action_pct": 50.0, "interiority_pct": 15.2, "neutral_pct": 34.8, "dialogue_density": 15.2, "figurative_density": 0.43, "sentence_rhythm": 12.36}, "entropy": 9.2},
    {"label": "Engine -- Kristina buries Karl", "texture": {"action_pct": 70.4, "interiority_pct": 9.3,  "neutral_pct": 20.3, "dialogue_density": 1.9,  "figurative_density": 0.51, "sentence_rhythm": 8.26},  "entropy": 9.1},
    {"label": "Engine -- Per plows field",      "texture": {"action_pct": 58.7, "interiority_pct": 8.7,  "neutral_pct": 32.6, "dialogue_density": 0.0,  "figurative_density": 0.52, "sentence_rhythm": 6.93},  "entropy": 9.3},
    {"label": "Engine -- Per sells farm",       "texture": {"action_pct": 61.7, "interiority_pct": 8.5,  "neutral_pct": 29.8, "dialogue_density": 6.4,  "figurative_density": 0.69, "sentence_rhythm": 9.17},  "entropy": 9.2},
    {"label": "Engine -- Per watches father",   "texture": {"action_pct": 48.4, "interiority_pct": 9.7,  "neutral_pct": 41.9, "dialogue_density": 6.5,  "figurative_density": 0.41, "sentence_rhythm": 9.07},  "entropy": 9.1},

    # --- Worst case ---
    {"label": "Worst case", "texture": {"action_pct": 10.0, "interiority_pct": 30.0, "neutral_pct": 40.0, "dialogue_density": 30.0, "figurative_density": 3.0, "sentence_rhythm": 4.0}, "entropy": 6.0},
]

print(f"\n{'DRIFT SCORER VERIFICATION':=<78}")
print(f"{'Label':<34} {'Drift':>7}  {'int_dev':>7}  {'fig_dev':>7}  {'act_dev':>7}  {'neu_dev':>7}")
print("-" * 78)

moberg_scores = []
engine_scores = []

for case in cases:
    r = scorer.score(case["texture"], entropy=case["entropy"])
    is_moberg = case["label"].startswith("Moberg")
    is_engine = case["label"].startswith("Engine")

    if is_moberg:
        moberg_scores.append(r["drift_score"])
    if is_engine:
        engine_scores.append(r["drift_score"])

    print(
        f"{case['label']:<34} "
        f"{r['drift_score']:>7.3f}  "
        f"{r['interiority_pct_dev']:>7.2f}  "
        f"{r['figurative_density_dev']:>7.3f}  "
        f"{r['action_pct_dev']:>7.2f}  "
        f"{r['neutral_pct_dev']:>7.2f}"
    )

print()
print(f"Moberg chapters  -- max: {max(moberg_scores):.3f}  mean: {sum(moberg_scores)/len(moberg_scores):.3f}")
print(f"Engine outputs   -- min: {min(engine_scores):.3f}  mean: {sum(engine_scores)/len(engine_scores):.3f}")