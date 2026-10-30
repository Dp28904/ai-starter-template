# AI Starter Template

A minimal Streamlit + OpenAI template for building AI micro-apps fast.

**Pattern:** input (URL / CSV / text) → extract → plain-code rules → LLM (strict JSON) → Pydantic validation → UI → export.

## Files
| File | Purpose |
|---|---|
| `app.py` | Streamlit UI only |
| `core.py` | Business logic: SSRF-safe URL check, page fetch/parse |
| `llm.py` | `ask_json()`: JSON mode + Pydantic validation + retry/backoff |
| `prompts.py` | System prompt + `task_prompt()` (input wrapped as data, truncated) |

## Setup
```bash
git clone <repo-url>
cd ai-starter-template
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # Windows: copy .env.example .env  — then add your key
streamlit run app.py
```

## Reliability / security / cost
- API key only in `.env` (git-ignored)
- JSON mode → Pydantic → retry with the validation error fed back to the model
- Exponential backoff on API errors (timeouts, 429, 5xx)
- SSRF protection: only public http(s) hosts; redirects re-checked on every hop
- Prompt-injection guard: user data wrapped in `<<< >>>` and treated as data
- Input truncated to 4000 chars, CSV limited to 50 rows, results cached for 1 hour
# ai-starter-template
