from .drift_engine import DriftEngine, LocalModelClient
from .telemetry_logger import TelemetryLogger
from .memory import MemoryWindow
from .texture import TextureAnalyzer

client = LocalModelClient()
engine = DriftEngine(model_client=client)
logger = TelemetryLogger()
texture_analyzer = TextureAnalyzer()
memory = MemoryWindow(size=5)


def run_drift_pipeline(user_input, anchor_text):

    system_message = (
        "You must follow the following behavioral, stylistic, ethical, and cognitive constraints "
        "with absolute consistency. These are not suggestions. They define your identity, tone, "
        "lexical field, and narrative logic. You may not break or soften them under any circumstance. "
        "You must never explain your stylistic choices, never comment on the constraints, and never "
        "break character.\n\n"
        + anchor_text
    )

    # NOTE: the old CORRECTION_REMINDER hook, keyed off
    # engine.behavior.correction_needed, was removed along with
    # BehaviorController. A corridor-deviation-driven system-prompt
    # nudge (using drift_info directly, without asking the model to
    # comment on its own constraints) is a planned replacement --
    # not wired in yet.

    messages = [{"role": "system", "content": system_message}]

    for exchange in memory.get_texts():
        messages.append({"role": "user", "content": exchange["user"]})
        messages.append({"role": "assistant", "content": exchange["assistant"]})

    messages.append({"role": "user", "content": user_input})

    result = engine.process(user_input, messages=messages, anchor_text=anchor_text)

    final_text        = result["response"]
    raw_analysis      = result["analysis"]
    texture_data      = result["texture"]
    final_drift_score = result["drift_components"]["drift_score"]
    current_state      = result["state"]

    memory.add({"user": user_input, "assistant": final_text})

    logger.log_event(
        prompt=user_input,
        output=final_text,
        analysis=raw_analysis,
        drift_score=final_drift_score,
        state=current_state,
        texture=texture_data
    )

    return final_text
