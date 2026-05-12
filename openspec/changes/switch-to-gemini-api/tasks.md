## 1. Dependencies

- [x] 1.1 Remove `anthropic>=0.30.0` from `pipeline/requirements.txt` and add `google-generativeai>=0.8.0`
- [x] 1.2 Run `pip install -r requirements.txt` to verify the new dependency installs cleanly

## 2. Environment Variable

- [x] 2.1 Update `pipeline/pipeline.py` to check for `GEMINI_API_KEY` instead of `ANTHROPIC_API_KEY` (startup guard)

## 3. Synthesis Module

- [x] 3.1 Replace `import anthropic` with `import google.generativeai as genai` in `pipeline/synthesis.py`
- [x] 3.2 Replace `CLAUDE_MODEL = "claude-opus-4-5"` with `GEMINI_MODEL = "gemini-2.0-flash"` in `pipeline/synthesis.py`
- [x] 3.3 Replace the `anthropic.Anthropic` client init and `client.messages.create(...)` call in `run_synthesis` with `genai.configure(api_key=...)` + `genai.GenerativeModel(GEMINI_MODEL).generate_content(prompt)`
- [x] 3.4 Update response extraction from `message.content[0].text` to `response.text` in `pipeline/synthesis.py`

## 4. Verification Module

- [x] 4.1 Replace `import anthropic` with `import google.generativeai as genai` in `pipeline/verification.py`
- [x] 4.2 Replace `CLAUDE_MODEL` constant with `GEMINI_MODEL = "gemini-2.0-flash"` in `pipeline/verification.py`
- [x] 4.3 Replace `anthropic.Anthropic` client init and `client.messages.create(...)` call with Gemini equivalent in `pipeline/verification.py`
- [x] 4.4 Update response extraction from `message.content[0].text` to `response.text` in `pipeline/verification.py`

## 5. Documentation

- [x] 5.1 Update `README.md` to reference `GEMINI_API_KEY` instead of `ANTHROPIC_API_KEY` in setup and pipeline sections
