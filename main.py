#!/usr/bin/env python3
"""Fix Human Sleep: Funniest Patch Note.

Writes one line of patch notes announcing that human sleep is fixed to
/output/entry.txt. The line must read like a real changelog entry, land its
joke on a single read, and stay within 1-160 characters on one line.

The program keeps a shortlist of candidate lines, scores each one for
changelog voice (Fixed / deprecated / bug / removed-in-a-future-update),
specificity (a concrete number or named behaviour instead of a flat claim
that sleep is fixed), and fit to the length cap, then writes the best.
Scoring is deterministic: same input, same output, every run.
"""

import os

OUT_PATH = "/output/entry.txt"
MAX_CHARS = 160

# Candidate patch notes. Each is one line, about fixing human sleep,
# written in changelog voice.
CANDIDATES = [
    "Fixed: sleep now completes in one uninterrupted 8-hour session; "
    "waking up tired is now deprecated and will be removed in a future update.",
    "Fixed a bug where 8 hours of sleep still left users tired; sleep now "
    "ships with the 'rested' feature enabled by default.",
    "Fixed: dreams no longer buffer during deep sleep; waking up rested is "
    "a known issue and we are investigating.",
    "Fixed sleep: the snooze button no longer negotiates; users now wake up "
    "on the first alarm, rested, against their will.",
    "Fixed: humans can now fall asleep without replaying every embarrassing "
    "moment from 2014 first.",
]

# Changelog-voice markers, weighted by how strongly they signal a real
# release note. "deprecated ... removed in a future update" is the
# strongest: it is the exact phrasing a changelog uses to kill a feature.
CHANGELOG_MARKERS = {
    "Fixed": 3,
    "deprecated": 4,
    "removed in a future update": 4,
    "bug": 2,
    "known issue": 2,
    "ships with": 2,
    "no longer": 2,
}

# Specificity markers: a concrete number, a named feature, or a named
# behaviour beats a flat "sleep is fixed now".
SPECIFICITY_MARKERS = {
    "8-hour": 3,
    "8 hours": 3,
    "uninterrupted": 2,
    "snooze button": 2,
    "first alarm": 2,
    "2014": 2,
    "buffer": 2,
    "'rested'": 2,
}


def score(line: str) -> int:
    """Score a candidate: changelog voice + specificity, minus length cost."""
    points = 0
    for marker, weight in CHANGELOG_MARKERS.items():
        if marker in line:
            points += weight
    for marker, weight in SPECIFICITY_MARKERS.items():
        if marker in line:
            points += weight
    # Prefer lines that use the budget without padding: reward length up
    # to 150 chars, then penalise anything creeping toward the cap.
    if len(line) > 150:
        points -= (len(line) - 150)
    return points


def pick_best(candidates) -> str:
    """Return the highest-scoring valid line (1-160 chars, single line)."""
    valid = [c for c in candidates if 1 <= len(c) <= MAX_CHARS and "\n" not in c]
    if not valid:
        raise ValueError("no candidate fits the 1-160 character single-line gate")
    # max() keeps the first on a tie, so the shortlist order breaks ties.
    return max(valid, key=score)


def main() -> None:
    line = pick_best(CANDIDATES)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"{line} ({len(line)} chars)")


if __name__ == "__main__":
    main()
