# E2M Interview Prep — Associate AI Engineer (Walk-in, 31 Oct 2026)

Rounds: **1. Technical MCQs** → **2. Build an app (AI tools allowed, on their system)** → **3. Technical interview** → **HR**.
Round 2 has its own file: [ROUND2_PLAYBOOK.md](ROUND2_PLAYBOOK.md). Prompts: [PROMPTS.md](PROMPTS.md).

---

## 0. Read these 10 lines before Round 1

1. Slicing: start included, stop excluded. `a[5:]` → `[]`, `a[5]` → IndexError.
2. `y = x` shares the list. `.sort()` returns None. Strings never change.
3. The comma makes a tuple. `"0"` and `[0]` are truthy. `-7 // 2 = -4`.
4. dict lookup is O(1). `is` = same object. `0.1 + 0.2 != 0.3`.
5. RAG = **Retrieval-Augmented Generation**. RAG = knowledge; fine-tuning = behaviour.
6. `max_tokens` = output limit. Top-p = nucleus sampling. Temperature 0–2 (OpenAI), 0–1 (Claude). Few-shot = examples.
7. Bi-encoder retrieves, cross-encoder reranks. RRF merges lists. FAISS `IndexFlatL2` = exact search.
8. The LLM decides; my code runs the tool. LangGraph **State** = shared data.
9. 401 login · 403 permission · 422 validation · 429 rate limit · 503 temporarily down. PUT is idempotent, POST isn't.
10. `-p HOST:CONTAINER` · `git revert` = safe undo · `IS NULL` not `= NULL` · JWT payload is readable.

---

## 1. Company: E2M Solutions

| Fact | Detail |
|---|---|
| Business | **White-label partner for digital agencies**: E2M does the work, agencies sell it under their own brand |
| Founded / HQ | 2012, Ahmedabad. Founder: Manish Dudharejia |
| Size | 300+ people, 400+ agencies in US, UK, Canada, Europe, Australia |
| Services | Web design/dev, WordPress, eCommerce, SEO, **AI SEO / GEO**, PPC & Meta ads, content, **AI automation & agents** |
| News | 2024: acquired **UnlimitedWP** (largest white-label WordPress provider). 2025: **Brent Weaver** became CEO |
| AI practice | White-label AI agents, workflow automation, custom AI apps / internal tools, AI SaaS, AI reporting dashboards |

**What the role does (from the job posting):** AI-native apps (backend + frontend) · REST APIs in FastAPI/Flask · LLM APIs (OpenAI, Claude, Hugging Face) · prompt engineering · RAG with embeddings and vector DBs · React/Next.js components · PostgreSQL/Supabase · Pandas/NumPy · **rapid prototyping** · debugging AI pipelines.

**Gaps and how to answer them:**

| Gap | Say |
|---|---|
| React / Next.js | "My frontend is Angular — same component model. Props ≈ `@Input()`, state ≈ class variables, `useEffect([])` ≈ `ngOnInit`. I'll pick it up quickly." |
| Supabase | "Postgres + auth + storage + auto APIs + pgvector. I've used PostgreSQL heavily and Qdrant/Chroma for vectors." |
| Flask | "Minimal, synchronous, manual validation. I use FastAPI: async, Pydantic validation, auto Swagger." |
| Web scraping | "`requests` to fetch, BeautifulSoup to parse, Scrapy for crawling, Playwright for JS pages. Respect robots.txt." |

**What they look for:** practical builder · LLM/RAG depth · fast prototyping with AI tools · business sense (SEO, content, leads, reports) · reliability mindset · fast learner · clear communication.

---

## 2. Round 1 — MCQ cheat sheet (built from my own mistakes)

### Weak-area map

| Area | Level | Risk |
|---|---|---|
| Python output traps | Weak, improving (6/15 → 4/12) | **High** |
| HTTP, idempotency, Docker ports, SQL NULL | Medium | Medium |
| n8n syntax and nodes | Medium | Medium |
| LLM parameters, prompting terms | Medium | Medium |
| RAG, vector/hybrid search | Strong | Low |
| LangChain/LangGraph, tool calling | Good | Low |

### 2.1 Python traps (biggest risk) — ❌ = I got this wrong

| Code | Output | Rule |
|---|---|---|
| `"hello"[1:4]` | `"ell"` ❌ | Start included, stop excluded, index from 0 |
| `"python"[2:5]` | `"tho"` | p0 y1 **t2 h3 o4** n5 |
| `"abc"[::-1]` | `"cba"` ❌ | Step −1 reverses |
| `a[5:]` (3 items) / `a[5]` | `[]` ❌ / IndexError | Slicing is safe, indexing isn't |
| `y = x; y.append(4)` | x changes too ❌ | Same list, two names. Copy: `x[:]`, `x.copy()` |
| `def f(l=[])` | shared between calls ❌ | Default created once → use `l=None` |
| `a == a.copy()` / `a is a.copy()` | True / False ❌ | `==` value, `is` same object |
| `print(x.sort())` | `None` ❌ | `.sort()`, `.append()`, `.reverse()` return None |
| `sorted(x)` | new list, x unchanged ❌ | |
| `s.upper(); print(s)` | unchanged ❌ | Strings immutable → `s = s.upper()` |
| `(5)` / `(5,)` / `1, 2` | int / tuple / tuple ❌ | The comma makes the tuple |
| `t[0] = 10` on a tuple | TypeError ❌ | Immutable |
| `bool("0")`, `bool([0])`, `bool(" ")` | True, True, True ❌ | Non-empty = truthy |
| `"Hi" if [] else "Bye"` | `"Bye"` ❌ | Empty list is falsy, no error |
| `[1, 2] * 2` | `[1, 2, 1, 2]` ❌ | `*` repeats |
| `2 ** 3 ** 2` | 512 | Right to left |
| `-7 // 2`, `-7 % 2` | −4, 1 ❌ | `//` rounds down toward −∞ |
| `0.1 + 0.2 == 0.3` | False ❌ | Float precision → `math.isclose` |
| `f(*args)` with `f(1, [2, 3], 4)` | 3 args ❌ | A list counts as one |
| `g(**kw)` with `g(a=1, b=2)`; `list(kw.keys())` | `['a', 'b']` ❌ | kwargs is a dict |
| `d[k] = d.get(k, 0) + 1` twice | 2 ❌ | Counting pattern |
| `[i for i in range(5) if i % 2]` | `[1, 3]` ❌ | Odd → truthy |
| O(1) lookup by key | dict / set ❌ | List search is O(n) |

**Method:** trace line by line on paper, write variable values, assume a trap (reference, None, slicing, truthiness, `//`).

### 2.2 Coding patterns

```python
d.get(k, default)                          # safe access
res[k] = res.get(k, 0) + v                 # count / group-sum
max(d, key=d.get)                          # key with highest value
sorted(items, key=lambda x: x["s"], reverse=True)
[x for x in items if x.get("active")]      # filter
groups.setdefault(k, []).append(v)         # group into lists
Counter(items).most_common(k)
df.groupby("col")["val"].sum()             # pandas
```

Practice: palindrome · anagram · Two Sum (dict) · first non-repeating char · dedup keep order (`dict.fromkeys`) · word frequency · group by category · total per customer + top customer · chunk text with overlap · cosine similarity in NumPy · safe JSON parse of LLM output · retry decorator.

```python
def customer_totals(orders):
    totals = {}
    for o in orders:
        name = o.get("customer", "unknown")
        totals[name] = totals.get(name, 0) + o.get("amount", 0)
    return totals, (max(totals, key=totals.get) if totals else None)
```

### 2.3 LLM & prompting

| Concept | Correct | My mistake |
|---|---|---|
| RAG full form | Retrieval-Augmented Generation | said "retrieve argument" |
| Token | Smallest text unit → token ID; ≈ ¾ word | |
| Context window | **Max** tokens (input + output) per request | didn't say it's a limit |
| `max_tokens` | Limits the **output** | chose context window |
| Temperature | Randomness. 0 = consistent, does **not** stop hallucination | said range 9–10 |
| Top-p | Nucleus sampling | chose beam search |
| Zero-shot / few-shot | No examples / 2–5 examples in prompt | said "follow-up questions" |
| System prompt | Developer instructions: role, rules, tone, format. Not training | said "trained" |
| Roles | `system`, `user`, `assistant`, `tool` | |
| Fine-tuning | Changes behaviour/style, not reliable facts | suggested for hallucination |

- **3 ways to reduce hallucination:** RAG grounding · strict prompt (only from context, cite, "I don't know") · low temperature + validation / tools for live facts.
- **Reduce cost:** right-sized model · caching (Redis, prompt caching) · fewer input tokens (top-3 chunks, short prompts, summarised history) · `max_tokens` · batching · code instead of LLM · track tokens.
- **Reliable JSON:** prevent (JSON mode / structured outputs, schema, temp 0) → validate (Pydantic) → retry with error → fall back.
- **Model choice:** OpenAI (ecosystem, embeddings) · Claude (long docs, writing, coding, instructions) · open source (privacy, control, fine-tuning, high volume). Test 2–3 on real data; keep code model-agnostic.

### 2.4 RAG & vector DBs

| Concept | Correct |
|---|---|
| RAG | Retrieve relevant chunks → augment prompt → generate grounded answer |
| Why chunk | Focused embeddings · precise retrieval · token limits & cost |
| Chunk size | 500–1000 tokens, 10–20% overlap, split by structure |
| Embedding | Vector capturing **meaning**; similar meaning = close |
| Cosine similarity | Angle between vectors; 1 same, 0 unrelated; `dot / (‖a‖·‖b‖)` |
| Hybrid search | BM25 (exact: SKUs, names) + vectors (meaning) |
| RRF vs reranking | RRF **merges** lists (Σ 1/(k+rank)); reranking = cross-encoder **rescoring** top 20–50 |
| Bi-encoder | Separate encoding, precomputed → fast retrieval |
| Cross-encoder | Query + doc together → accurate, slow → rerank |
| RAGAS | Faithfulness (answer supported) · context precision (chunks relevant) · recall · relevance |

| FAISS | Pinecone | pgvector / Supabase | Chroma | Qdrant |
|---|---|---|---|---|
| Library (Meta), in memory, vectors only. `IndexFlatL2` = exact ❌ | Managed cloud, paid | Postgres extension; stores/searches, doesn't create embeddings | Light DB, prototypes | Production, filters |

IVF = clusters, HNSW = graph (both approximate). FAISS never does keyword search. Supabase is **not** part of Neon ❌.

**Debug order:** retrieval or generation? → extraction (OCR, tables) → chunking → embeddings (same model) → search (top-k, hybrid, rerank, filters) → prompt → LLM settings → measure on a test set.

### 2.5 Tool calling, agents, LangChain, LangGraph

- **Tool calling:** LLM returns tool name + arguments as JSON → **my code runs it** → result back as `tool` message → final answer.
- **Agent:** tool calling in a loop until the goal is done.
- LCEL: `prompt | llm | parser`. Splitter: `RecursiveCharacterTextSplitter`.
- LangGraph: **State** = shared data ❌ · Node = function · Edge = arrow · conditional edge = routing · checkpointer = memory/resume/human-in-loop.
- MCP = standard protocol for connecting tools/data to LLMs.

### 2.6 n8n

| Need | Answer |
|---|---|
| Data between nodes | Array of items, each `{ json: {...} }` |
| Previous node field | `{{ $json.email }}` |
| Named node field | `{{ $('Webhook').item.json.email }}` ❌ |
| Custom JS/Python | **Code** node ❌ (Set/Edit Fields = no-code) |
| API · schedule · pause · combine | HTTP Request · Schedule Trigger · Wait · Merge |
| 2 branches / many | IF / Switch |
| Alert on failure | Error Trigger workflow |
| Webhook URLs | Test = editor listening; Production = workflow active |
| Reliability | Retry On Fail · error output · Error Trigger |
| Links between nodes | "connections" (not "edges") |

Lead flow: Webhook → Edit Fields/Code → IF spam → OpenAI/AI Agent (JSON) → Code parse → Switch → Slack/Gmail/CRM → Google Sheets → Respond to Webhook (+ Error Trigger).

### 2.7 APIs, HTTP, security

| Method | Purpose | Body | Idempotent |
|---|---|---|---|
| GET | Read | No — URL/query ❌ | Yes |
| POST | Create | Yes | **No** ❌ |
| PUT | Replace whole | Yes | **Yes** ❌ |
| PATCH | Partial update | Yes | Usually |
| DELETE | Remove | No | Yes |

| Code | Meaning |
|---|---|
| 200 / 201 / 204 | OK / Created / No Content |
| 400 vs 422 | Broken format vs invalid data (FastAPI/Pydantic) ❌ |
| 401 vs 403 | Not logged in vs no permission |
| 429 | Rate limited → exponential backoff |
| 500 vs 503 | Bug vs temporarily down/overloaded ❌ |
| 502 / 504 | Bad gateway / gateway timeout |

- **FastAPI vs Flask:** async, Pydantic validation (422), auto Swagger `/docs` vs minimal, sync, manual ❌.
- **JWT:** header.payload.signature; payload Base64URL-encoded → **readable**, not encrypted ❌; `Authorization: Bearer`; verify signature + expiry; short expiry + refresh tokens.
- **CORS:** Cross-Origin Resource Sharing — browser rule (Postman works); origin = protocol + domain + port; fix on backend (`CORSMiddleware`); no `*` in production.
- **Streaming:** `stream=True` → FastAPI `StreamingResponse` (SSE, `text/event-stream`) → frontend appends chunks. SSE one-way, WebSocket two-way. ❌ (it's on my resume)
- **API keys:** `.env` + `.gitignore` + `.env.example`; host env vars / secrets manager in prod; never in frontend; revoke + rotate if leaked.

### 2.8 Docker, Git, SQL

| Item | Correct |
|---|---|
| Image vs container | Blueprint vs running instance |
| `-p 8080:8000` | HOST:CONTAINER → open **8080** ❌ |
| `docker ps` · compose · volume | Running containers · many containers · persistent data |
| merge / rebase | Merge commit, history kept / replay on top, local only |
| reset / revert | Erases history / new undo commit — safe on shared ❌ |
| `WHERE x = NULL` | Always 0 rows → `IS NULL` ❌ |
| WHERE vs HAVING | Before vs after GROUP BY |
| LEFT JOIN | All left rows + matches, NULL otherwise |
| 2nd highest | `SELECT MAX(s) FROM t WHERE s < (SELECT MAX(s) FROM t)` |

### 2.9 ML metrics

- Precision = TP/(TP+FP): "when I say fraud, am I right?"
- Recall = TP/(TP+FN): "did I catch them all?" → **prioritise for fraud** ❌
- F1 = a **metric**, not an imbalance technique ❌
- Imbalance fixes: stratified split · SMOTE on training data only · class weights · threshold tuning · anomaly detection
- Heavy imbalance: PR-AUC > ROC-AUC; accuracy is misleading

### 2.10 Trap pairs

| Pair | Difference |
|---|---|
| `sort()` vs `sorted()` | None, in place vs new list |
| `*args` vs `**kwargs` | Tuple vs dict |
| max_tokens vs context window | Output limit vs model total |
| Top-p vs temperature vs beam | Nucleus vs randomness vs decoding method |
| RAG vs fine-tuning | Knowledge vs behaviour |
| Faithfulness vs context precision | Answer supported vs chunks relevant |
| `$json` vs `$('Node')` | Previous vs named node |
| 401/403 · 400/422 · 500/503 | Login/permission · format/data · bug/temporary |
| POST vs PUT | Not idempotent vs idempotent |
| reset vs revert | Erase vs safe undo |
| JWT encoded vs encrypted | Only encoded → readable |
| F1 vs SMOTE | Metric vs technique |

### 2.11 MCQ strategy

- Read the whole question: watch for NOT, except, best, first.
- Python output: trace on paper, assume a trap.
- Eliminate two options, then choose.
- Clue words: "temporarily" → 503 · "exact match" → BM25 · "shared data" → State · "creates" → POST · "safe undo" → revert · "validation" → 422.
- Over 60–90 s → mark and move on. Check negative marking; if none, answer everything.
- Don't look for answer-letter patterns.

---

## 3. Round 3 — How to answer

**Skeleton for every answer:**

```
1. Direct answer (1 line, repeat the question's key word)
2. "There are 3 parts / I'd do 3 things:"
3. First… Second… Third…  (name the tool/technique)
4. Example from MY project (Aavak / Kabra / RAG / POS)
5. Closing line (how I'd measure it / the result)
```

**Habits that cost me marks in the mocks:**

| Habit | Fix |
|---|---|
| Answering a different question ("why" instead of "how did you measure") | Repeat the key word in sentence one |
| Trailing off ("and another thing we can…") | Decide 3 points before speaking; end with a closing line |
| Saying "train" for prompting | Say "prompt template", "instruct", "give context" |
| Wrong company name | Say **"Demaze Techstudio"** slowly |
| No technical keywords | Use the terms: query rewriting, Core Web Vitals, Recall@k… |
| Asking the interviewer for the answer | "Beyond that, I'd also consider…" |
| "I don't know" and stopping | "I haven't used X directly, but my understanding is… and I've used Y" |
| "Not interested in frontend" | Never. "My frontend is Angular; React is similar." |
| Stating unsure facts | Leave them out |

**Say clearly:** RAG · Retrieval-Augmented Generation · FastAPI · Flask · CORS · JWT · BM25 · Qdrant · Reciprocal Rank Fusion · cross-encoder · BeautifulSoup · Scrapy · Supabase · Demaze Techstudio · NSE and BSE.

### Mock scores (for tracking)
Mock 1 average ≈ 4.6/10 · Mock 2 average ≈ 4.8/10. Best: Aavak architecture (7), hybrid search (7), deployment (7). Weakest: measuring search (3), slow chatbot (3), streaming (2), few-shot (2), coding (2–3).

---

## 4. Round 3 — 20 questions with model answers

> ⚠️ Adjust anything to what I actually did. Never invent numbers.

**1. Tell me about yourself.**
"I'm Deep Patel, a Computer Engineering graduate from GEC Gandhinagar. I'm an AI Full Stack Developer at **Demaze Techstudio**, where I built **Aavak**, a production hybrid search system combining Elasticsearch keyword search with Qdrant vector search, rank fusion and a cross-encoder reranker, and the backend for **Kabra CRM** in NestJS and PostgreSQL. Before that I interned at **Optimum Financial Solutions**, building mutual fund onboarding with NSE and BSE integrations and KYC. My own projects include a **RAG assistant** that answers from financial PDFs with citations, and a **fraud detection model** optimised for recall and F1. E2M brings AI automation to hundreds of agencies, and I want to build practical AI tools that real businesses use."
🔑 Who I am → 2 named work projects → internship → 2 personal projects → why E2M.

**2. Walk me through Aavak's architecture.**
"Two pipelines. **Indexing:** a product event goes to Kafka, a Bull worker enriches categories with OpenAI, embeds text with BGE-M3 and images with CLIP, and indexes into Elasticsearch and Qdrant with the same ID. **Query:** intent analysis extracts filters, BM25 and vector search run in parallel, weighted RRF merges them, a cross-encoder reranks the top 20–50, and the top 10 are returned. Redis tracks popular searches for suggestions."
🔑 How data gets in, and how it's searched. (Queries are **not** chunked; BM25 doesn't use embeddings.)

**3. Why hybrid search? Why not vector search alone?**
"BM25 is great at exact terms — 'Jordan 4', SKUs, brands — but doesn't understand meaning. Vector search understands 'maroon' ≈ 'dark red' but is weak at exact matches; it can treat 'Jordan 1' and 'Jordan 4' as almost identical. I run both and merge with Reciprocal Rank Fusion, which uses ranks, so no score normalisation is needed."
🔑 Keyword = exact, vector = meaning, hybrid = both.

**4. Bi-encoder vs cross-encoder? Why not cross-encoder for everything?**
"A bi-encoder encodes query and documents separately; document vectors are precomputed, so search is fast over millions, but less precise. A cross-encoder reads query and document together and scores relevance — much more accurate, but nothing can be precomputed, it runs once per pair. So: retrieve top 50 with bi-encoder + BM25, rerank only those with the cross-encoder."
🔑 Bi-encoder = resume shortlist, cross-encoder = detailed interview.

**5. How did you measure that search improved?**
"We compared BM25 only, hybrid, and hybrid + reranking on real sample queries — exact and descriptive — checking whether expected products appeared in the top results. Hybrid reduced zero-result searches on descriptive queries; reranking put the right item first more often. We tracked latency too. To make it rigorous: a labelled test set with Recall@10, MRR, nDCG, plus click-through rate and A/B tests."
🔑 Method + metric + result + improvement. Hybrid is **not** faster than BM25 alone.

**6. JWT and RBAC in Kabra CRM.**
"At login the server checks the bcrypt hash and issues a JWT — header, payload with user ID, role and expiry, and a signature. The client sends `Authorization: Bearer`; a NestJS guard verifies signature and expiry, else 401. A `@Roles()` decorator and RolesGuard compare the role, else 403. The payload is only encoded, so no secrets in it; short expiry with refresh tokens."
🔑 401 = who are you? 403 = not allowed.

**7. Where would you add AI to Kabra CRM?**
"Three places. **Auto-classification:** an LLM returns JSON with category, department and priority for routing. **Fix suggestions with RAG:** embed resolved complaints — text and defect images with CLIP — in Qdrant; retrieve similar past cases and summarise the fix and spare parts used. **Duplicates and summaries:** embedding similarity flags duplicates; the LLM summarises long threads. Engineers approve suggestions; measure time to resolution."
🔑 Classify · retrieve similar · summarise · detect duplicates.

**8. Fraud: why not accuracy, and how did you handle imbalance?**
"Fraud is ~1%, so always predicting 'genuine' gives 99% accuracy and is useless. Precision asks 'when I flag fraud, am I right?', recall asks 'did I catch them all?' — recall matters more, balanced with F1. For the imbalance: stratified split, class weights or SMOTE on training data only, and threshold tuning on the precision-recall curve. F1 measures; it doesn't fix."
🔑 Fraud → recall. F1 = metric. SMOTE/class weights = techniques.

**9. Explain your RAG pipeline.**
"Retrieval-Augmented Generation. Ingestion: extract PDF text, chunk ~800 tokens with 100–150 overlap, embed, store in ChromaDB with tenant ID, filename and page. Query: embed the question, retrieve top-k filtered by the tenant from the JWT, send to the LLM with a strict prompt — only from context, cite source and page, else 'I don't know'. Async FastAPI, Redis chat history, streaming Angular UI."
🔑 Retrieve → augment → generate, with tenant filters and citations.

**10. "Revenue in 2023?" then "And what about last year?"**
"Embedding the follow-up alone retrieves the wrong chunks — it has no 'revenue' and no year. I keep recent history in Redis and have the LLM **rewrite the follow-up into a standalone question** — 'What was the revenue in 2022?' — then embed and retrieve that. Only the last few turns are kept; if 'last year' is ambiguous, ask the user."
🔑 Rewrite → retrieve → answer.

**11. RAG gives wrong answers — debug it.**
"First: retrieval or generation? Check which chunks were retrieved. Retrieval: extraction (OCR, tables), chunking, same embedding model, search settings — top-k, hybrid, reranking, filters. Generation: grounding prompt, low temperature, context not too long. Then measure on ~50 real questions with RAGAS faithfulness and context precision."
🔑 Retrieval or generation → extract → chunk → embed → search → prompt → measure.

**12. How do you stream an LLM response?**
"Call the LLM with `stream=True`; in FastAPI a generator yields each chunk through `StreamingResponse` using Server-Sent Events; the Angular chat UI reads the stream and appends each chunk. SSE because it's one-way over HTTP; WebSocket is for two-way. Handle end-of-stream, errors and cancellation."
🔑 stream=True → StreamingResponse (SSE) → append chunks.

**13. How does tool calling work? What's an agent?**
"The LLM decides; my code executes. I send the question plus tool definitions — name, description, JSON schema. The model returns `get_weather(city='Ahmedabad')`; my app runs it and sends the result back as a tool message; the model writes the answer. An agent is this in a loop — e.g. an SEO agent calling fetch_page, check_keywords, update_sheet. I validate arguments and limit tools."
🔑 The LLM never runs code itself.

**14. Reliable JSON from an LLM?**
"Prevent: JSON mode or structured outputs, schema and example in the prompt, temperature 0. Validate: strip code fences, parse, Pydantic for fields and ranges; on failure retry with the error message; after 2–3 failures, fall back to a default or manual review."
🔑 Prevent → validate → retry with the error → fall back.

**15. Reduce token usage and cost?**
"Right model for the task; caching — Redis, semantic cache, prompt caching; fewer tokens — short prompts, top-3 chunks, summarised history, `max_tokens`; code before the LLM — in an SEO tool plain code checks title length, the LLM only rewrites; and track tokens per feature or client."
🔑 Right model · cache · trim · code first · track.

**16. Secure a public chatbot on a client's site.**
"Layers. Prompt injection/jailbreak: prompt rules aren't enough — the bot can only reach public data, with access control at retrieval via metadata filters; treat input as data; filter output. Abuse/cost: rate limiting, max input length, `max_tokens`, budget alerts. Privacy: key on backend only, PII masked in logs, GDPR. Brand safety: moderation, topic limits, 'I don't know' with contact option. Test with attack prompts before launch."
🔑 Don't rely on the prompt for security — control what data the bot can reach.

**17. The chatbot takes 8–10 s — make it faster.**
"Measure each stage: embedding and search are usually under 200 ms; LLM generation is the bottleneck. Per request: stream, cache frequent questions, fewer smaller chunks with `max_tokens`, faster model for simple queries. Under load: async FastAPI, more workers/containers behind a load balancer, rate limiting. Monitor p95 latency."
🔑 Measure → bottleneck → stream, cache, shrink → scale → monitor. (Chunking is ingestion-time, not per request.)

**18. Build an AI SEO audit tool.**
"Rules plus AI. Crawl with requests + BeautifulSoup (Scrapy for a site), blocking internal IPs. Code checks: title ≤60 and meta ≤155 characters, one H1, image alt text, broken links, HTTPS, canonical, mobile viewport; Core Web Vitals (LCP, INP, CLS) from the PageSpeed API. LLM only for judgement: strict JSON with score, rewritten title/meta, content issues, keywords, validated with Pydantic. Output: prioritised, white-labelled report; scheduled batches with caching."
🔑 Crawl → rules in code → PageSpeed → LLM for judgement → white-label report.

**19. Weekly AI performance report from GA4 + Google Ads.**
"A scheduler (cron or n8n Schedule Trigger) runs every Monday per client. Fetch from GA4 and Google Ads APIs with OAuth. Compute in Pandas — sessions, conversions, CTR, spend, week-over-week change — and charts; the LLM never does maths. The LLM gets only aggregated metrics with a prompt template and returns JSON: summary, wins, concerns, recommendations; I check every number matches. Build a white-labelled report and email it. On API failure, retry then alert — never send a wrong report."
🔑 Code computes, the LLM explains.

**20. Clean, maintainable code — especially with AI tools?**
"Structure: routes, logic and data access separated — NestJS modules in Kabra CRM. Readability: clear names, type hints, small functions. Reliability: DTO/Pydantic validation, explicit errors, env config, proper logging. Quality: ruff/ESLint, unit tests, Git code review. Efficiency: measure first, right data structures, caching. With ChatGPT/Claude/Cursor: clear prompts, small steps, read and test every line, never paste secrets."
🔑 Structure · validate · handle errors · test · review every AI line.

**Bonus — Why should we hire you?**
"Three things. Real AI in production — Aavak's hybrid search and a RAG assistant with citations. The full stack around AI — FastAPI, NestJS, PostgreSQL, Redis, Kafka, auth, deployment. I build fast and responsibly — AI tools for speed, plus review, testing and security. E2M delivers AI to 400+ agencies, so reliable practical tools have big impact — that's the work I want."

---

## 5. More Round 3 questions to be ready for

**Aavak:** Why Qdrant over Pinecone/Chroma? · What does k in RRF do (smooths scores, ~60)? · Keep ES and Qdrant in sync? (same Kafka event, idempotent upserts by ID) · Kafka duplicate events? (idempotency) · Why Kafka **and** Bull? (event stream vs job queue with retries) · Redis popularity scoring? (sorted sets) · Add Hindi/Gujarati search? (BGE-M3 multilingual, language analysers).

**Kabra CRM:** Complaint lifecycle · Why NestJS / MikroORM · Schema and indexes · Secure file uploads (type/size check, unique names, access checks) · Bulk import when row 500 fails (validate first, transaction or partial insert + error report, batch inserts).

**RAG project:** Tables in PDFs (pdfplumber/Unstructured → markdown) · Multi-tenant isolation (tenant ID from JWT) · Out-of-scope questions (similarity threshold + "I don't know") · Scale to 10,000 PDFs (async ingestion queue, batch embeddings).

**Fraud:** Features used · Model and why · Avoid leakage (split before SMOTE/scaling, time-based split) · Serve with FastAPI (load once at startup) · Model drift (monitor, retrain).

**Snowflake:** Stage/Clean/Consumption layers · Star schema · SCD Type 1 vs 2 · Streams + MERGE · ETL vs ELT.

**Internship:** Transactional Outbox (write data + event in one transaction, publish separately) · RabbitMQ vs Kafka · KYC flow · Penny Drop (₹1 verification) · Reliable webhooks (signature, idempotency key, return 200 fast, process async).

**Company/role:** What is white-label? · How can AI help E2M? · Which AI coding tools and how? · What is an AI-native app? · Agent vs chatbot · n8n vs code · What is MCP? · What is GEO / AI SEO? · Explain RAG to a non-technical client ("open-book exam") · How do you keep up with AI?

**Scenarios (goal → input → process → AI → output → reliability → cost → measure):**

1. SEO blog drafts for 50 agencies with brand voices → per-client brand profile + few-shot, RAG over past posts, outline → draft → human review, queue, cost per client.
2. Client chatbot by Friday → scrape site → chunk/embed → RAG API → widget → test 20 questions → "contact us" fallback.
3. Same input, different LLM answers → temp 0, structured output, fixed prompt versions, few-shot, validation.
4. Confidential client data → encryption, access control, tenant isolation, PII masking, provider with no training on data, retention.
5. Audit 1,000 sites monthly → scheduler → queue → workers → rules → LLM summaries → DB → dashboard; rate limits, retries.
6. OpenAI is down → retries, fallback provider behind a model-agnostic layer, queue, clear user message.
7. Does this task need AI? → If code solves it reliably, use code. AI for language, judgement, unstructured data.

**STAR stories to prepare (Situation, Task, Action, Result):** learned a tech fast · production bug · disagreement · tight deadline · explained tech to non-technical person · AI output was wrong · a mistake and lesson.

**Tricky questions:**

| Question | Handle |
|---|---|
| Only 5 months at Demaze — why leave? | Positive: want full focus on AI engineering and automation at scale. Never criticise. |
| Built Aavak alone? | Honest about my part vs team's |
| Resume says immediate joiner | Give the **real** notice period |
| You know Angular, we use React | Same component model; productive quickly |
| If AI writes code, why need you? | Design, debugging, security, quality judgement, business understanding |
| Rate yourself in Python | Realistic 6–7; strong in practical backend/AI, improving in algorithms |
| First 30 days? | Learn E2M's AI stack and use cases, ship one small internal tool, document learnings |

---

## 6. HR round

- **Why E2M:** "E2M delivers services to 400+ agencies, so practical AI automation has large impact. The role — RAG, LLM APIs, rapid prototyping — matches what I've been building."
- **Why leave after 5 months:** "I've learned a lot building production search at Demaze. I want a role focused fully on AI engineering and automation with broader client use cases."
- **Notice period:** one clear, true answer.
- **Salary:** "I'm open and want to understand the growth path; based on my experience I'm expecting around ___."
- **Strength:** learn fast and ship — internship fintech workflows to production AI search within months.
- **Weakness:** over-optimising; now I time-box, ship a working version first, then improve.
- **3 years:** an AI engineer who designs and leads AI automation projects end to end.
- **Never** frame AI as a backup plan or mention another field as a first choice.

**Questions to ask them (pick 2):** What AI projects would I work on first — internal or client-facing? · What's the AI stack — LangChain, n8n, custom? Which LLM providers? · How do you evaluate AI features before delivery? · What does success look like after 6 months?

---

## 7. Day-of checklist

- [ ] 3–4 printed resumes, photo ID, degree/marksheet copies, pen, water
- [ ] Phone charged; cheat sheet page and this repo open
- [ ] Notice period and salary number decided
- [ ] OpenAI spending limit set (if using own key); revoke key after Round 2
- [ ] Arrive 30 minutes early
- [ ] Every answer: direct answer → count points → my project → finish
