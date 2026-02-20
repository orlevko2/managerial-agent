def draft_email(to: str, subject: str, body: str, cc: str = "") -> str:
    lines = [
        "=" * 60,
        "EMAIL DRAFT",
        "=" * 60,
        f"To:      {to}",
    ]
    if cc:
        lines.append(f"CC:      {cc}")
    lines += [
        f"Subject: {subject}",
        "-" * 60,
        body,
        "=" * 60,
    ]
    return "\n".join(lines)
