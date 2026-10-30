# Round 2 Playbook — Build an AI App (on E2M's system, AI tools allowed)

Everything for Round 2: likely problems, what to ask, how to break the problem down, the timed workflow, setup on an unfamiliar machine, the checklist, the demo script, and clean-up.
Prompts are in [PROMPTS.md](PROMPTS.md). Interview notes are in [INTERVIEW_PREP.md](INTERVIEW_PREP.md).

---

## 1. Likely problem statements (based on E2M's business)

E2M = white-label SEO, web, content, PPC and AI automation for 400+ agencies. The job posting stresses rapid prototyping, AI-powered internal tools, LLM APIs and RAG.

| # | Likely problem | Input → output | What impresses |
|---|---|---|---|
| 1 | **AI SEO audit tool** | URL → score, issues, AI fixes | Rules in code + LLM for judgement, SSRF check, download report |
| 2 | **Bulk meta title/description generator** | CSV of URLs/topics → titles ≤60, metas ≤155 | Length validation in code, batching, retry only failed rows |
| 3 | **Website/PDF Q&A chatbot (RAG)** | URL or PDF → chat with citations | Chunking, citations, "I don't know", follow-up rewriting |
| 4 | **Blog content brief generator** | Keyword + audience → outline, H2s, FAQs, meta | Structured JSON brief, tone option, Markdown export |
| 5 | **Google Ads copy generator** | Product + USP → 15 headlines ≤30 chars, 4 descriptions ≤90 | Character-limit validation, regenerate only invalid items |
| 6 | **Lead/email classifier + reply drafter** | Email text/CSV → category, priority, draft | JSON classification, confidence, human approval |
| 7 | **Analytics/ads CSV → AI insights** | CSV → KPIs, charts, summary | Pandas computes, LLM explains |
| 8 | **Client brief → task breakdown + estimate** | Brief → tasks, hours, team, risks | Structured output, editable table, export |
| 9 | **Competitor page comparison** | 2 URLs → SEO/content gaps | Reuse scraper, side-by-side table |
| 10 | **Review sentiment analyser** | Reviews CSV → sentiment, themes, summary | Batching, aggregate chart |

**They nearly all follow one pattern** — this template is built for it:

```
INPUT (URL / CSV / PDF / text)
  → EXTRACT (scrape / parse / read)
  → CODE (rules, calculations, validation)
  → LLM (strict JSON, only the thinking/writing part)
  → VALIDATE (Pydantic + business rules, e.g. char limits)
  → SHOW (Streamlit: metric, table, chart)
  → EXPORT (CSV / JSON / Markdown download)
```

**Golden rule:** plain code does everything objective; the LLM does only language and judgement. Cheaper, faster, more reliable — and a strong demo point.

---

## 2. Questions to ask before starting (pick 3–5)

1. How much time do I have, and how long is the demo?
2. Who is the user — agency SEO person, client, internal team?
3. Is there sample input (URLs, CSV, PDFs)?
4. What output do you expect — UI, API, downloadable report?
5. Preferred stack, or is Python with Streamlit/FastAPI fine?
6. Will you provide an LLM API key?
7. One item or bulk?
8. Deployed or running locally?
9. What matters most — features, code quality or UX?
10. **"May I start from a small starter template I prepared on GitHub, or should I build from scratch?"** — always ask; never use it without permission.

---

## 3. Break the problem down (5 minutes on paper)

```
GOAL:          One line — e.g. "Agency user enters URL → gets prioritised SEO fixes."
USER:          Who uses it?
INPUT:         Exactly what goes in (URL / CSV columns / PDF)?
OUTPUT:        Exactly what comes out (fields, format)?
STEPS:         5–7 steps max
CODE PART:     What plain code can do (fetch, parse, calculate, validate)
AI PART:       What ONLY the LLM can do (write, judge, classify, summarise)
EDGE CASES:    Bad input, empty data, API failure, bad LLM JSON, oversized input
MUST-HAVE:     Core flow end to end (MVP)
NICE-TO-HAVE:  Bulk mode, chart, caching, export formats
```

Then paste the problem into **Prompt 0** (PROMPTS.md) to check your plan.

---

## 4. First 5 minutes on their computer — check the environment

```bash
python --version      # or python3 --version / py --version
pip --version
git --version
code --version        # VS Code?
```

Ask: Which AI tools are allowed (ChatGPT/Claude in browser, Cursor, Copilot)? API key provided? Can I pip install? How do I submit (show on machine, zip, GitHub)?

| Finding | Action |
|---|---|
| Python + pip work | Set up below |
| No Python, no admin rights | Ask them to install, or use what's installed and let AI write in that language |
| pip blocked | Try `pip install --user ...` or ask for an approved environment |
| No VS Code | Use any editor; the browser AI writes, you paste |

---

## 5. Setup (about 5–10 minutes)

**If the template is allowed:**

```bash
git clone https://github.com/Dp28904/ai-starter-template.git
cd ai-starter-template
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env           # Mac/Linux: cp .env.example .env  → then add the key
streamlit run app.py
```

- A venv needs no admin rights.
- Creating `.env` in Notepad: choose "All files" so it doesn't become `.env.txt`.

**If the template is not allowed:** paste the **"Backup: recreate this template with AI"** prompt from PROMPTS.md, then continue.

---

## 6. Timed workflow (2 hours — scale to the time given)

| Phase | Time | Do | Done when |
|---|---|---|---|
| 0. Understand | 0–10 | Read problem, ask questions, fill breakdown, check environment | Plan on paper |
| 1. Setup | 10–20 | Clone/recreate template, install, `.env`, run | Empty app runs |
| 2. Core flow (MVP) | 20–65 | Prompt 0 → Prompt 1. Input → extract → LLM JSON → show | **Works end to end** |
| 3. Reliable + secure | 65–85 | Prompt 2: validation, errors, retries, limits, business rules | Bad input handled |
| 4. One standout feature | 85–100 | Prompt 3: bulk CSV / chart / caching / export — pick **one** | "Wow" moment |
| 5. Test | 100–110 | Prompt 6: normal, bad input, edge case | Confident |
| 6. README + demo prep | 110–120 | Prompt 7 README, Prompt 5 understand code, rehearse | Ready to present |

**Rules during the build**

- By the halfway point the core flow must work; if not, cut features.
- One feature per AI prompt; test, then next.
- Commit after each working step: `git add . && git commit -m "core flow working"`.
- Read every line the AI writes — they will ask you to explain it.
- Don't switch stacks mid-way.

**Browser AI on someone else's machine**

- Ask for **complete files**, not fragments: "Return the complete updated app.py."
- Keep files small (UI / logic / LLM separate) so each fits one paste.
- Paste the full error message when something fails (Prompt 4).
- Keep a `notes.txt` with decisions — it helps the demo.
- If Cursor/Copilot is installed, use it in the editor instead.

---

## 7. Reliability & security checklist (tick before the demo)

- [ ] API key only in `.env`; `.env` in `.gitignore`; never pasted into the AI chat
- [ ] Input validation: empty, wrong type, size/row/char limits
- [ ] URL safety check (SSRF) if the app fetches URLs — `core.is_safe_url`
- [ ] Prompt-injection safety: input wrapped in `<<< >>>` as data — `prompts.task_prompt`
- [ ] LLM output: JSON mode → Pydantic → business rules (char limits etc.) — `llm.ask_json`
- [ ] Retry with backoff on API errors; friendly error messages
- [ ] Input truncated; results cached (`st.cache_data`)
- [ ] Bulk mode: one failed item doesn't crash the run
- [ ] Tested: normal, bad input, edge case
- [ ] README with architecture and future improvements

---

## 8. Demo script (5 minutes)

| Time | Say / do |
|---|---|
| 0:00–0:30 Problem | "Agencies spend hours on X. This tool does it in seconds, for one item or in bulk." |
| 0:30–2:00 Live demo | Normal input → results → download. **Then a bad input** — handled gracefully. |
| 2:00–3:00 Architecture | "Input → extract → code for objective checks → LLM only for judgement in strict JSON → Pydantic validation → UI and export." |
| 3:00–4:00 Decisions | "Reliability: JSON mode, validation, retry with the error. Cost: rules in code, truncated input, caching. Security: key in .env, SSRF check, input treated as data." |
| 4:00–5:00 Next steps | "FastAPI backend for scale, a queue for bulk jobs, white-label PDF reports for agencies, quality evaluation on a test set, deploy on Render." |

**Likely questions after the demo**

| Question | Answer |
|---|---|
| Why Streamlit? | Fastest working Python UI in a timed round; production would be FastAPI + React. |
| 1,000 rows? | Background queue, batching, rate limits, progress tracking, results in a DB, per-item retries. |
| How do you know the AI output is right? | JSON mode + Pydantic + business rules, temp 0, grounded in provided data; human spot-check and a small test set. |
| Cost? | One small call per item, truncated input, caching, track tokens per client. |
| What did AI write vs you? | I designed the architecture and prompts and reviewed every function; AI sped up boilerplate. I can explain any line. |
| What breaks first in production? | Rate limits and slow pages in bulk → queue, concurrency limits, timeouts. |

---

## 9. API key safety and clean-up

**If they provide a key:** use it.
**If using my own key:** set a low spending limit beforehand; key only in `.env`; never in code or chat.

**Before leaving their computer**

- [ ] Delete `.env` (or remove the key)
- [ ] Log out of ChatGPT, Claude, GitHub and any accounts
- [ ] Don't let the browser save passwords
- [ ] Close terminals and the app
- [ ] Revoke my API key from my phone right after the round
- [ ] Submit the work the way they asked

---

## 10. Worked example — AI SEO audit (problem #1)

Adapt `app.py` with this logic. Plain-code checks first, LLM only for suggestions.

```python
from bs4 import BeautifulSoup

def seo_checks(html: str, url: str) -> tuple[dict, list[tuple[str, str]], str]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    meta = soup.find("meta", attrs={"name": "description"})
    desc = (meta.get("content") or "").strip() if meta else ""
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    imgs = soup.find_all("img")
    no_alt = [i for i in imgs if not i.get("alt")]
    text = " ".join(soup.get_text(" ").split())
    words = len(text.split())

    issues = []
    if not title: issues.append(("High", "Missing title tag"))
    elif not 30 <= len(title) <= 60: issues.append(("Medium", f"Title is {len(title)} chars (ideal 30–60)"))
    if not desc: issues.append(("High", "Missing meta description"))
    elif not 70 <= len(desc) <= 160: issues.append(("Medium", f"Meta description is {len(desc)} chars (ideal 70–160)"))
    if not h1s: issues.append(("High", "No H1 heading"))
    elif len(h1s) > 1: issues.append(("Medium", f"{len(h1s)} H1 tags (use one)"))
    if no_alt: issues.append(("Medium", f"{len(no_alt)} of {len(imgs)} images missing alt text"))
    if not soup.find("link", rel="canonical"): issues.append(("Low", "No canonical tag"))
    if not soup.find("meta", attrs={"name": "viewport"}): issues.append(("High", "No viewport meta (not mobile-friendly)"))
    if words < 300: issues.append(("Medium", f"Thin content: {words} words"))
    if not url.startswith("https"): issues.append(("High", "Not using HTTPS"))

    facts = {"title": title, "meta_description": desc, "h1": h1s, "word_count": words,
             "images": len(imgs), "images_missing_alt": len(no_alt)}
    return facts, issues, text[:3000]
```

LLM schema (Pydantic) for the suggestions:

```python
from pydantic import BaseModel

class Recommendation(BaseModel):
    priority: str
    fix: str

class SeoAI(BaseModel):
    score: int
    summary: str
    suggested_title: str
    suggested_meta: str
    target_keywords: list[str]
    recommendations: list[Recommendation]
```

Business rule after the LLM: if `len(suggested_title) > 60` or `len(suggested_meta) > 155`, retry once asking for shorter text.

Extensions if time allows: bulk CSV of URLs · competitor comparison · `@st.cache_data` per URL · PageSpeed API for Core Web Vitals · white-label PDF.

---

## 11. Three-step plan for tomorrow

1. **Get the core flow working.**
2. **Make it reliable and secure.**
3. **Explain it clearly.**

A simple app that works, handles errors and is explained well beats a complex app that breaks.
