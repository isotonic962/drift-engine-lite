"""
Run TextureAnalyzer over multiple text files and print results.

Usage:
    python benchmark_texture.py chapter1.txt chapter2.txt ...
    python benchmark_texture.py chapters/*.txt
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from engine.texture import TextureAnalyzer

def analyze_file(path, analyzer):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return analyzer.analyze(text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python benchmark_texture.py file1.txt file2.txt ...")
        sys.exit(1)

    paths = sys.argv[1:]
    analyzer = TextureAnalyzer()
    results = []

    print(f"\n{'MOBERG TEXTURE BENCHMARK':=<72}")
    print(f"{'File':<30} {'act':>5} {'int':>5} {'neu':>5} {'dial':>5} {'fig':>6} {'rhy':>6}")
    print("-" * 72)

    for path in paths:
        if not os.path.exists(path):
            print(f"  [SKIP] {path} not found")
            continue
        r = analyze_file(path, analyzer)
        name = os.path.basename(path)[:29]
        print(
            f"{name:<30} "
            f"{r['action_pct']:>5.1f} "
            f"{r['interiority_pct']:>5.1f} "
            f"{r['neutral_pct']:>5.1f} "
            f"{r['dialogue_density']:>5.1f} "
            f"{r['figurative_density']:>6.3f} "
            f"{r['sentence_rhythm']:>6.2f}"
        )
        results.append(r)

    if len(results) < 2:
        return

    print(f"\n{'SUMMARY':=<72}")
    metrics = ["action_pct", "interiority_pct", "neutral_pct",
               "dialogue_density", "figurative_density", "sentence_rhythm"]

    print(f"{'Metric':<22} {'min':>7} {'max':>7} {'mean':>7}  corridor / ceiling")
    print("-" * 72)

    for m in metrics:
        vals = [r[m] for r in results]
        lo   = round(min(vals), 2)
        hi   = round(max(vals), 2)
        mean = round(sum(vals) / len(vals), 2)

        if m in ("interiority_pct", "figurative_density"):
            shape = f"one-sided ceiling -> {hi}"
        else:
            shape = f"corridor -> ({lo}, {hi})"

        print(f"{m:<22} {lo:>7} {hi:>7} {mean:>7}  {shape}")

    print()
    print("Paste the corridor/ceiling values above into engine/drift.py")
    print("ONE_SIDED and CORRIDORS once you're happy with the sample size.")

if __name__ == "__main__":
    main()