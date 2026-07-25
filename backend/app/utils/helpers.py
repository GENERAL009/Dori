from datetime import date, timedelta, time


def calculate_end_date(start_date: date, duration_days: int) -> date:
    return start_date + timedelta(days=duration_days)


def parse_time_string(time_str: str) -> time:
    parts = time_str.split(":")
    return time(int(parts[0]), int(parts[1]))


def format_time(t: time) -> str:
    return t.strftime("%H:%M")


def get_period_label(period: str) -> str:
    labels = {
        "morning": "08:00",
        "afternoon": "14:00",
        "evening": "20:00",
        "night": "21:00",
    }
    return labels.get(period, period)


def days_between(start: date, end: date) -> int:
    return (end - start).days


def progress_percentage(start: date, end: date, current: date = None) -> float:
    if current is None:
        current = date.today()
    total = days_between(start, end)
    if total <= 0:
        return 100.0
    elapsed = days_between(start, current)
    return min(100.0, max(0.0, elapsed / total * 100))
