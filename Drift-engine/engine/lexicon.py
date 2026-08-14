"""
Physical/transitional verb lexicon, extracted from the retired
ConstraintDetector.

ConstraintDetector itself (the sentence-level scan/classification logic
used for truncation and BehaviorController stripping) was removed in the
post-Qwen2.5 cleanup pass -- benchmarked at a 15.3% false-positive rate
against real Moberg chapters. This vocabulary set was still a legitimate
dependency of TextureAnalyzer (pure measurement: action_pct classification
in action_interiority_ratio), so it's pulled out here rather than deleted
along with the detection logic that misused it.
"""

PHYSICAL_VERBS = {
    "turned", "stopped", "set", "stood", "crossed", "lifted",
    "lowered", "opened", "closed", "entered", "left", "dropped",
    "picked", "pulled", "pushed", "cut", "broke", "struck",
    "placed", "carried", "threw", "caught", "dug", "poured",
    "split", "dragged", "loaded", "unloaded", "hitched",
    "saddled", "mounted", "dismounted", "knelt", "rose",
    "crouched", "leaned", "reached", "gripped", "released",
    "swung", "hammered", "nailed", "sawed", "chopped",
    "slipped", "stumbled", "fell", "climbed", "stepped",
    "walked", "ran", "moved", "shifted", "slid", "sat",
    "lit", "doused", "ate", "drank", "spat", "coughed",
    "dressed", "undressed", "washed", "wiped", "scraped",
    "folded", "unfolded", "packed", "unpacked", "locked",
    "unlocked", "bolted", "fastened", "unfastened",
    "began", "finished", "started", "ended", "halted",
    "paused", "resumed", "continued",
    "plowed", "ploughed", "sowed", "harvested", "reaped",
    "threshed", "harrowed", "seeded", "mowed", "scythed",
    "buried", "dug", "filled", "covered", "laid", "lowered",
    "signed", "handed", "sold", "paid", "received",
    # present tense / gerund forms
    "turns", "stops", "sets", "stands", "crosses", "lifts",
    "lowers", "opens", "closes", "enters", "leaves", "drops",
    "picks", "pulls", "pushes", "cuts", "breaks", "strikes",
    "places", "carries", "throws", "catches", "digs", "pours",
    "drags", "loads", "unloads", "kneels", "rises",
    "crouches", "leans", "reaches", "grips", "releases",
    "swings", "hammers", "nails", "saws", "chops",
    "slips", "stumbles", "falls", "climbs", "steps",
    "walks", "runs", "moves", "shifts", "slides", "sits",
    "lights", "eats", "drinks", "spits", "coughs",
    "washes", "wipes", "scrapes", "folds", "unfolds",
    "packs", "unpacks", "locks", "unlocks", "bolts",
    "fastens", "begins", "finishes", "starts", "ends",
    "halts", "pauses", "resumes", "continues",
    "plows", "sows", "harvests", "reaps", "mows",
    "buries", "fills", "covers", "lays",
    "signs", "hands", "sells", "pays", "receives",
    "dig", "sit", "run", "stand", "lean", "kneel",
    "crouch", "grip", "swing", "climb", "slip",
    "wash", "wipe", "scrape", "fold", "pack",
    "lock", "bolt", "fasten", "plow", "sow",
    "harvest", "reap", "mow", "bury", "fill",
    "cover", "lay", "sign", "sell", "pay",
}
