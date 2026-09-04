def health_state(value, warning, critical):
    if value >= critical:
        return "🔴 Critical"

    if value >= warning:
        return "⚠️ Warning"

    return "✅ Healthy"


def overall_health(states):
    if any("Critical" in state for state in states):
        return "🔴 Critical"

    if any("Warning" in state for state in states):
        return "⚠️ Warning"

    return "✅ Healthy"