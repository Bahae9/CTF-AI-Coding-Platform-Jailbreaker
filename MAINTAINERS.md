# Maintainer notes

This repository is an **intentionally vulnerable** CTF target. The weaknesses below are deliberate,
confined to the challenge, and marked in the code with `STAGE N` comments. Do not "fix" them — they are
the challenge. Do not report them as security issues.

## Intentional vulnerabilities

| Stage | File | Deliberate flaw |
|-------|------|-----------------|
| 1 — Search | `challenge/backend/main.py` → `ai_search()` | The unpublished `upcoming_courses` table (with `internal_notes`) is placed in the model's context; only a natural-language "published only" rule guards it. |
| 2 — Code Review | `challenge/backend/main.py` → `review_code()` / `load_code_examples()` | The whole `code_examples/` dir — including a `.env` — is injected into the system prompt as "reference material", alongside untrusted uploaded code. |
| 3 — Chat | `challenge/backend/main.py` → `chat()` / `guardrail()` | A secret lives in Lia's system prompt; replies are screened only by a keyword blocklist plus a second-model judge. |

The flag and all fragments are the challenge's own (`learnify{...}`). The planted
`challenge/code_examples/.env` is **bait** and holds no real secret; it is tracked on purpose (see the
negation rule in `.gitignore`).

## Flag fragments and encodings

| Fragment | Lives in | Encoding |
|----------|----------|----------|
| `learnify{s34rch_l34k__` | `upcoming_courses.internal_notes` ("AI for Security"), seeded in `main.py` | hex |
| `f1l3_3xf1l__` | `code_examples/.env` → `SECRET_KEY` | binary |
| `gu4rdr41l_byp4ss}` | Lia system prompt → `platform_token` | plaintext |

If you change the flag, update all three locations plus `challenge/challenge.yml`; the offline test
suite (`tests/test_consistency.py`) checks they stay in sync and decode correctly.

## Model and difficulty

The AI calls use `gemini-2.5-flash` (`GEMINI_MODEL` in `main.py`). It returns no "thinking" tokens by
default, so the guardrail's `maxOutputTokens=5` still yields a one-word `SAFE`/`UNSAFE`. If you move to
a `gemini-3.x` model, set `thinkingConfig.thinkingBudget=0` on the guardrail call or it returns empty
text.

**Difficulty.** Stage 3 is the hardest by design. The keyword blocklist in `guardrail()` deliberately
does **not** contain the fragment value, so the real gate is the second-model judge — and that judge
only ever sees the chatbot's reply as data. The intended solve is a two-layer prompt injection: get
Lia to carry the token in a reply she'll produce, then shape that reply so the judge reads it as safe.
Keep the guardrail as-is to preserve the intended difficulty.

If you are running this for a less experienced audience and want an easier variant, you can soften the
judge in `guardrail()` (e.g. drop the "encoded, obfuscated, or partial versions" clause) or drop the
judge and keep only the keyword filter. Document any such change here and in `challenge/challenge.yml`,
and keep a note that the default build is the full-difficulty one.

## Local dev without Docker

`challenge/run.sh` starts the backend (`:8000`) and frontend (`:8501`) directly (no nginx). The Docker
path (`docker compose up --build` from the repo root) is the supported one.
