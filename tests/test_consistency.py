"""
Offline consistency checks for the AI System Breaker challenge.

These run without Docker, without network, and without the app's dependencies
(fastapi/streamlit): they read the source files as text and assert that the flag,
its three encoded fragments, and the challenge descriptor all stay in sync. They
also syntax-check the backend and frontend.

Run:  python -m unittest discover -s tests -v
"""
import py_compile
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "challenge"

# The flag and the split points are the challenge's design, declared once here.
FRAG_A = "learnify{s34rch_l34k__"   # stage 1 (search)  -> hex in upcoming_courses
FRAG_B = "f1l3_3xf1l__"             # stage 2 (review)  -> binary in code_examples/.env
FRAG_C = "gu4rdr41l_byp4ss}"        # stage 3 (chat)    -> plaintext in Lia's system prompt
FLAG = FRAG_A + FRAG_B + FRAG_C

HEX_A = " ".join(f"{b:02X}" for b in FRAG_A.encode())
BIN_B = " ".join(format(b, "08b") for b in FRAG_B.encode())


def read(rel: str) -> str:
    return (CH / rel).read_text(encoding="utf-8")


class TestFragments(unittest.TestCase):
    def test_fragments_join_to_flag(self):
        self.assertEqual(FRAG_A + FRAG_B + FRAG_C, FLAG)

    def test_encodings_round_trip(self):
        self.assertEqual(bytes.fromhex(HEX_A.replace(" ", "")).decode(), FRAG_A)
        self.assertEqual("".join(chr(int(x, 2)) for x in BIN_B.split()), FRAG_B)


class TestFlagInSources(unittest.TestCase):
    def test_challenge_yml_flag_matches(self):
        m = re.search(r"flag:\s*\"([^\"]+)\"", read("challenge.yml"))
        self.assertIsNotNone(m, "no flag found in challenge.yml")
        self.assertEqual(m.group(1), FLAG)

    def test_stage1_hex_in_backend_seed(self):
        self.assertIn(HEX_A, read("backend/main.py"),
                      "stage-1 hex fragment missing from the upcoming_courses seed")

    def test_stage2_binary_in_bait_env(self):
        self.assertIn(BIN_B, read("code_examples/.env"),
                      "stage-2 binary fragment missing from code_examples/.env")

    def test_stage3_plaintext_in_lia_prompt(self):
        self.assertIn(f"platform_token={FRAG_C}", read("backend/main.py"),
                      "stage-3 fragment missing from Lia's system prompt")

    def test_no_stale_event_flag(self):
        # The original MCTF flag must not linger anywhere in the challenge tree.
        for p in CH.rglob("*"):
            if p.is_file() and p.suffix in {".py", ".yml", ".env", ".md", ".txt"}:
                self.assertNotIn("mctf{", p.read_text(encoding="utf-8", errors="ignore").lower(),
                                 f"stale event flag found in {p}")


class TestGuardrail(unittest.TestCase):
    def test_keyword_filter_does_not_contain_the_value(self):
        # The keyword blocklist should gate obvious leaks WITHOUT listing the
        # fragment value itself (which would make stage 3 unsolvable by keyword).
        src = read("backend/main.py")
        block = src[src.index("FLAG_PATTERNS"):src.index("def guardrail")]
        self.assertNotIn(FRAG_C, block)
        self.assertIn('"platform_token"', block)  # the label is blocked, not the value


class TestSyntax(unittest.TestCase):
    def test_backend_compiles(self):
        py_compile.compile(str(CH / "backend" / "main.py"), doraise=True)

    def test_frontend_compiles(self):
        py_compile.compile(str(CH / "frontend" / "app.py"), doraise=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
