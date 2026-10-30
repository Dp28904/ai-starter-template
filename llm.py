import os, time
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
_client = None

def _get_client() -> OpenAI:
    """Create the client lazily so the app still starts if the key is missing."""
    global _client
    if _client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set. Add it to the .env file.")
        _client = OpenAI()              # reads OPENAI_API_KEY from env
    return _client

def ask_json(system: str, user: str, schema: type[BaseModel],
             retries: int = 2, temperature: float = 0) -> BaseModel:
    """Call the LLM in JSON mode and validate against a Pydantic schema.
    Retries with the validation error so the model can self-correct.
    Note: JSON mode requires the word 'JSON' in the prompt."""
    client = _get_client()
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": user}]
    last_err = None
    for attempt in range(retries + 1):
        raw = ""
        try:
            r = client.chat.completions.create(
                model=MODEL, temperature=temperature, timeout=30,
                response_format={"type": "json_object"}, messages=messages)
            raw = r.choices[0].message.content or ""
            return schema.model_validate_json(raw)
        except ValidationError as e:                 # bad JSON / wrong fields
            last_err = e
            messages += [{"role": "assistant", "content": raw},
                         {"role": "user", "content": f"Invalid output: {e}. Return ONLY valid JSON matching the schema."}]
        except Exception as e:                       # timeout, 429, 5xx
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)             # exponential backoff
    raise RuntimeError(f"LLM failed after {retries + 1} attempts: {last_err}")
