import os
import re
from datetime import datetime, timezone


_DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
]


def _parse_dt(value: str) -> datetime:
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized datetime format: '{value}'")


def _ics_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _safe_filename(title: str) -> str:
    return re.sub(r"[^\w\-]", "_", title)


def create_calendar_event(
    title: str,
    start: str,
    end: str,
    description: str = "",
    location: str = "",
) -> str:
    try:
        start_dt = _parse_dt(start)
        end_dt = _parse_dt(end)
    except ValueError as e:
        return f"Error parsing datetime: {e}"

    now_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    start_str = start_dt.strftime("%Y%m%dT%H%M%S")
    end_str = end_dt.strftime("%Y%m%dT%H%M%S")

    uid = f"{start_str}-{_safe_filename(title)}@managerial-agent"

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Managerial Agent//EN",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{now_utc}",
        f"DTSTART:{start_str}",
        f"DTEND:{end_str}",
        f"SUMMARY:{_ics_escape(title)}",
    ]
    if description:
        lines.append(f"DESCRIPTION:{_ics_escape(description)}")
    if location:
        lines.append(f"LOCATION:{_ics_escape(location)}")
    lines += ["END:VEVENT", "END:VCALENDAR"]

    ics_content = "\r\n".join(lines) + "\r\n"

    filename = f"{_safe_filename(title)}_{start_dt.strftime('%Y%m%d_%H%M')}.ics"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(ics_content)
    except Exception as e:
        return f"Error writing calendar file: {e}"

    return (
        f"Calendar event created: {filepath}\n"
        f"  Title: {title}\n"
        f"  Start: {start_dt.strftime('%Y-%m-%d %H:%M')}\n"
        f"  End:   {end_dt.strftime('%Y-%m-%d %H:%M')}"
    )
