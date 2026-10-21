# AI System Breaker — "Learnify"

[![CI](https://github.com/Bahae9/CTF-AI-Coding-Platform-Jailbreaker/actions/workflows/ci.yml/badge.svg)](https://github.com/Bahae9/CTF-AI-Coding-Platform-Jailbreaker/actions/workflows/ci.yml)

An intentionally vulnerable **AI-security CTF challenge**. It presents *Learnify*, a realistic
e-learning startup whose three LLM-powered features each leak one fragment of a flag through a
different class of prompt-injection / jailbreak vulnerability. Join the three fragments to recover
the flag.

Originally built for **MCTF 5.0** (MicroClub, USTHB) and re-packaged here as a standalone,
reproducible repository.

> **This is deliberately insecure software.** It exists to teach LLM-application security. Do not
> copy its patterns into real systems. See [Intentional vulnerabilities](#intentional-vulnerabilities).

---

## What it is

Learnify looks like an ordinary course platform — catalog, instructors, an "About" page — built with
a **Streamlit** frontend and a **FastAPI** backend behind an **nginx** gateway. Three features are
wired to Google **Gemini** and are the actual attack surface:

| Feature | Vulnerability class | What a solver must do |
|---|---|---|
| 🔍 **Smart Search** | Over-privileged context + instruction override | The model is handed unreleased ("upcoming") courses it is told never to surface. Get it to reveal them. |
| 🛠️ **Code Review** | Indirect prompt injection + secret in context | The reviewer is given internal reference files (including a `.env`) as context. Smuggle an instruction through the uploaded file to exfiltrate them. |
| 🤖 **Lia (chatbot)** | System-prompt leak past a two-layer guardrail | A secret lives in Lia's system prompt. Every reply is screened by a keyword filter *and* a second model acting as a judge. Get the secret out without tripping either. |

Players bring **their own Gemini API key** (free tier works); the server stores no key and holds no
API credentials of its own.

---

## Run it

```bash
docker compose up --build
# then open http://localhost:13000
```

That's the whole setup — no secrets, no config files, no API keys on the server. The only requirement
is Docker (Engine 20.10+ with the Compose plugin). The first build takes a few minutes; later starts
are seconds. Stop it with `Ctrl-C`, or `docker compose down` to remove the containers.

By default the gateway listens on `127.0.0.1:13000` (your machine only). Both parts are configurable:

```bash
LEARNIFY_PORT=8080 docker compose up --build        # if 13000 is taken
LEARNIFY_BIND=0.0.0.0 docker compose up --build      # host it for others on your LAN
```

### Play

1. Open the app, go to **Settings**, and paste a Google Gemini API key
   (get one free at [aistudio.google.com](https://aistudio.google.com); the free tier is enough).
2. Explore the site. Three features talk to the model: **Smart Search**, **Code Review**
   (under Settings → Developer Tools, or the nav), and the **Lia** assistant.
3. Extract one flag fragment from each. Concatenate them in feature order (search → review → chat)
   to form the flag: `learnify{...}`.

No key is needed to browse the catalog, instructors, or About page — only the three AI features
require one. Each player uses their own key, so you can host one instance for a whole group.

### Troubleshooting

- **Port already in use** — set a different one: `LEARNIFY_PORT=8080 docker compose up`.
- **"invalid API key" or quota errors** — the key is wrong, or the free-tier quota is spent; wait for
  the per-minute/day reset or use another key.
- **`docker-credential-desktop` not found** on build — your Docker config points at a credential helper
  that isn't installed. These are public images, so a throwaway config avoids it:
  `DOCKER_CONFIG=$(mktemp -d) docker compose up --build`.

---

## Architecture

```
            ┌─────────── nginx (:13000) ───────────┐
            │   /            → frontend (Streamlit) │
            │   /api/        → backend  (FastAPI)   │
            └──────────────────────────────────────┘
                         │                  │
                  Streamlit UI         FastAPI API ──► Google Gemini
                  (app.py)             (backend/main.py)      (gemini-2.5-flash)
                                           │
                                    SQLite (seeded on
                                    startup from code)
```

- **Frontend** — [`challenge/frontend/app.py`](challenge/frontend/app.py): the whole Learnify UI.
- **Backend** — [`challenge/backend/main.py`](challenge/backend/main.py): public catalog endpoints
  plus the three AI endpoints (`/api/search`, `/api/review-code`, `/api/chat`). The SQLite database is
  seeded from the code on startup, so it is a build artifact and is not committed.
- **Model** — `gemini-2.5-flash`. It is current and returns no hidden "thinking" tokens by default, so
  the guardrail's tiny token budget still yields a one-word verdict. If you swap in a `gemini-3.x`
  model, set `thinkingConfig.thinkingBudget=0` on the guardrail call (noted in the code).

---

## Intentional vulnerabilities

Each is deliberate, confined to the challenge, and marked in the code with a `STAGE N` comment.

1. **Over-privileged retrieval (search).** `/api/search` places unpublished `upcoming_courses` —
   including their `internal_notes` — into the model's context, then relies only on a natural-language
   instruction ("published only") to keep them hidden. Context the model shouldn't have is the bug.
2. **Secret-in-context + indirect injection (code review).** `/api/review-code` injects the contents
   of `code_examples/` — a `.py` set *and* a `.env` — into the system prompt as "reference material".
   Untrusted user input (the uploaded file) and a secret share the same context.
3. **Leaky system prompt behind an LLM guardrail (chat).** `/api/chat` keeps a secret in Lia's system
   prompt and guards replies with a keyword blocklist plus a second-model judge. The guardrail raises
   the bar but is not a substitute for keeping secrets out of the prompt.

The flag and its fragments are the challenge's own (`learnify{...}`), not real credentials. The
planted `.env` is bait and contains no real secret.

## Verification

Validated by building and running the full stack and driving the live API with a real Gemini key:

- Public endpoints, the seeded database, and the frontend load correctly.
- **Stage 1** and **Stage 2** solve end-to-end against live `gemini-2.5-flash`.
- **Stage 3** is the hardest: its guardrail blocks naive extraction, and the solve requires reading how
  the guardrail is built and chaining the injection through it. Full approach in the
  [writeup](solution/writeup.md).

Offline consistency tests (flag ↔ fragment encodings ↔ source files, plus syntax checks) run without
Docker or network:

```bash
python -m unittest discover -s tests -v
```

## Repository layout

```
.
├── docker-compose.yml        # one-command run (localhost by default)
├── MAINTAINERS.md            # intentional-vuln inventory + difficulty tuning
├── challenge/
│   ├── Dockerfile            # non-root image, shared by both services
│   ├── requirements.txt      # pinned direct dependencies
│   ├── challenge.yml         # CTFd/MicroClub challenge descriptor
│   ├── backend/              # FastAPI app (+ db helpers)
│   ├── frontend/             # Streamlit app (+ .streamlit/config.toml)
│   ├── code_examples/        # reviewer "reference" context (incl. the bait .env)
│   ├── nginx/                # gateway config
│   └── data/                 # SQLite DB is generated here at startup (gitignored)
├── tests/                    # offline consistency tests (stdlib only)
├── .github/workflows/        # CI: run tests + build the image
└── solution/
    └── writeup.md            # spoilers: full solution + the flag
```

## Limitations

- The AI features need a Google Gemini API key with available quota. Exact winning prompts depend on
  the model version; providers harden models over time, so a prompt that worked yesterday may need
  rework (this is part of the lesson).
- `gemini-2.5-flash` is hard-coded; there is no provider abstraction.
- The UI was refreshed and verified to serve and compile, but not visually screenshot-tested in this
  environment.

## Credits

Challenge by **Bahae** (Lemtai Bahaeddine) — [github.com/Bahae9](https://github.com/Bahae9).
Originally written for MCTF 5.0, organized by [MicroClub USTHB](https://github.com/MicroClub-USTHB).

## License

[MIT](LICENSE).
