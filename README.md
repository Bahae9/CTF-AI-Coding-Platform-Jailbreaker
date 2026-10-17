# AI System Breaker — "Learnify"

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

That's the whole setup. The gateway binds to `127.0.0.1:13000` by default. To host it for remote
players, change `127.0.0.1:13000:80` to `13000:80` in [docker-compose.yml](docker-compose.yml).

### Play

1. Open the app, go to **Settings**, and paste a Google Gemini API key
   (get one free at [aistudio.google.com](https://aistudio.google.com)).
2. Explore the site. Three features talk to the model: **Smart Search**, **Code Review**
   (under Settings → Developer Tools, or the nav), and the **Lia** assistant.
3. Extract one flag fragment from each. Concatenate them in feature order (search → review → chat)
   to form the flag: `learnify{...}`.

No key is needed to browse the catalog, instructors, or About page — only the three AI features
require one.

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

Validated by building and running the stack and driving the live API with a real Gemini key:

- Public endpoints, the seeded database, and the frontend load correctly.
- **Stage 1** and **Stage 2** were solved end-to-end against live `gemini-2.5-flash`.
- **Stage 3**'s guardrail was confirmed to block naive extraction; a full solve requires an
  encoding that evades the judge (see [the writeup](solution/writeup.md)). `gemini-2.5-flash` is
  notably robust, so stage 3 is the hardest stage by design.

## Repository layout

```
.
├── docker-compose.yml        # one-command run (localhost by default)
├── challenge/
│   ├── Dockerfile            # non-root image, shared by both services
│   ├── requirements.txt      # pinned direct dependencies
│   ├── challenge.yml         # CTFd/MicroClub challenge descriptor
│   ├── backend/              # FastAPI app (+ db helpers)
│   ├── frontend/             # Streamlit app (+ .streamlit/config.toml)
│   ├── code_examples/        # reviewer "reference" context (incl. the bait .env)
│   ├── nginx/                # gateway config
│   └── data/                 # SQLite DB is generated here at startup (gitignored)
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
