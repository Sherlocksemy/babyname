# Milestone 1.3 Root Cause

## Root Causes
- Milestone 1.2 ranked mostly by universal NES quality and E1 culture evidence.
- full_name overlap hid repeated given names when surnames differed.
- Direct culture bigrams dominated the candidate pool, so the same high-evidence names resurfaced across profiles.
- Profile fit, gender tone, surname rhythm, imagery, and generation path were not hard enough ranking factors.

## Fixes
- Use given_name overlap as the core cross-case metric.
- Add deterministic ProfileSpecificity and SurnameFit scores to each candidate.
- Add semantic-role composition and imagery-transformation paths without pretending they are direct phrases.
- Require profile thresholds for Top20, Top10, and Top3.
- Select Top20 with path balance so Direct Expression is capped at 50%.

## Status
- Matrix A meets threshold: True
- Matrix B meets threshold: True
- Milestone 2: not entered