import re


def normalize_keyword(keyword):
    return keyword.strip().casefold()


def mask_text(text, keywords):
    """Literal matching keeps original Unicode offsets, including expanding casefolds."""
    intervals = []
    for word in keywords:
        if not word:
            continue
        pattern = re.compile('(?=(' + re.escape(word) + '))', re.IGNORECASE)
        intervals.extend((m.start(1), m.end(1)) for m in pattern.finditer(text))
    merged = []
    for start, end in sorted(intervals):
        if merged and start < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    parts, previous = [], 0
    for start, end in merged:
        parts.extend((text[previous:start], '***'))
        previous = end
    return ''.join(parts) + text[previous:]


def current_keywords():
    from .db import get_db
    return [row['keyword'] for row in get_db().execute('SELECT keyword FROM masking_rules')]
