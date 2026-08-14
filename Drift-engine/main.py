from engine.controller import run_drift_pipeline, engine as _engine

with open("engine/prompts/system_anchor.txt", "r") as f:
    ANCHOR_TEXT = f.read()


def generate(user_input):
    """
    Single-call entry point -- works in a Kaggle notebook cell as well
    as a REPL. Prints the response plus the texture/drift telemetry
    that run_drift_pipeline already computed internally (previously
    main.py re-ran TextureAnalyzer a second time on the same output,
    duplicating work controller.py had already done).
    """
    output = run_drift_pipeline(user_input, ANCHOR_TEXT)
    print("Engine:", output)

    last = _engine.state  # DriftState -- last smoothed drift value
    print(f"  [DRIFT STATE] {round(last.get_state(), 3)}")

    return output


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if not user_input.strip():
            print("(empty input skipped)")
            continue
        generate(user_input)
