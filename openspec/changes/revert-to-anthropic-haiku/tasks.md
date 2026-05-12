## 1. Dependencies

- [x] 1.1 Remove `google-genai` from `pipeline/requirements.txt`
- [x] 1.2 Add `anthropic>=0.49.0` to `pipeline/requirements.txt`
- [x] 1.3 Re-install dependencies: `pip install -r requirements.txt`

## 2. Environment Variable Guard

- [x] 2.1 Update startup guard in `pipeline/pipeline.py` to check `ANTHROPIC_API_KEY` instead of `GEMINI_API_KEY`

## 3. Synthesis Module

- [x] 3.1 Remove `from google import genai` and `GEMINI_MODEL` constant from `pipeline/synthesis.py`
- [x] 3.2 Add `import anthropic` and `CLAUDE_MODEL = "claude-haiku-4-5"` to `pipeline/synthesis.py`
- [x] 3.3 Replace `genai.Client(api_key=os.environ["GEMINI_API_KEY"])` with `anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])`
- [x] 3.4 Replace `client.models.generate_content(model=GEMINI_MODEL, contents=prompt)` with `client.messages.create(model=CLAUDE_MODEL, max_tokens=2048, messages=[{"role": "user", "content": prompt}])`
- [x] 3.5 Replace `response.text` with `response.content[0].text` when extracting raw response text

## 4. Verification Module

- [x] 4.1 Remove `from google import genai` and `GEMINI_MODEL` constant from `pipeline/verification.py`
- [x] 4.2 Add `import anthropic` and `CLAUDE_MODEL = "claude-haiku-4-5"` to `pipeline/verification.py`
- [x] 4.3 Replace `genai.Client(api_key=os.environ["GEMINI_API_KEY"])` with `anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])`
- [x] 4.4 Replace `client.models.generate_content(model=GEMINI_MODEL, contents=prompt)` with `client.messages.create(model=CLAUDE_MODEL, max_tokens=2048, messages=[{"role": "user", "content": prompt}])`
- [x] 4.5 Replace `response.text` with `response.content[0].text` when extracting raw response text

## 5. Documentation

- [x] 5.1 Update `README.md` setup instructions to reference `ANTHROPIC_API_KEY` instead of `GEMINI_API_KEY`
