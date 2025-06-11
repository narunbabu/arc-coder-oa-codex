# Goal  
Build an **AI Coding Agent CLI** (“arc-coder”) that:
1. Reads plan.md and spawns Steps.  
2. Routes each Step to the optimal LLM model under live rate limits.  
3. Generates / edits / debugs code, installs deps, runs tests in Docker.  
4. Launches Playwright, seeds fake data, captures screenshots.  
5. Exposes all workers over the Model Context Protocol stdio transport.  
6. Ships with full pytest + Playwright test-suite covering every module.  
7. Provides a `typer` CLI (`arc`) with `run`, `status`, `resume`, `config` commands.  

# Tech Stack  
Python 3.12, Codex CLI v0.11+, Playwright-Py 1.45, Typer, Redis (for rate-limit storage), Docker.  

# Repository Layout  
arc-coder/
├─ arc/
│ ├─ init.py
│ ├─ plan_loader.py
│ ├─ model_router.py
│ ├─ rate_limiter.py
│ ├─ codex_engine.py
│ ├─ sandbox_runner.py
│ ├─ browser_worker.py
│ ├─ insight_worker.py
│ ├─ mcp_gateway.py
│ └─ cli.py
├─ tests/ (mirrors module tree)
├─ model_registry.yaml
├─ poetry.lock / pyproject.toml
└─ README.md


# Coding Tasks  
1. **Scaffold repo** as above.  
2. Implement each module with detailed docstrings.  
3. Use `subprocess.run(["codex", …], check=True, input=json.dumps(payload).encode())` in `codex_engine.py`.  
4. Implement token-bucket RateLimiter (rpm&rpd).  
5. Implement Playwright worker that starts server on random port, seeds Faker user, takes screenshot.  
6. Provide pytest tests described earlier; mark browser tests `@pytest.mark.e2e`.  
7. Add GitHub Actions workflow running all tests on Ubuntu-22.04.  
8. Generate SAMPLE `model_registry.yaml` pre-filled with free quotas for:  
   - `gemini-2.0-flash-lite` (30 rpm, 1 500 tpm)  
   - `mistralai/devstral-small:free` (20 rpm, 50 rpd)  #in openrouter
   - `gpt-4.1-mini` (8 rpm, 40 000 tpm)  
9. Ensure Docker is optional via `--no-docker` flag for Replit.  
10. Produce a concise `GETTING_STARTED.md`.  

# Testing Expectations  
* `pytest -q` exits 0.  
* `arc run examples/hello_plan.md` completes all steps inside 5 minutes, produces `screenshots/step-1.png`.  

# Quality Bar  
• PEP-8, 100 % type-checked with `mypy --strict`.  
• No ReplitAuth or other Replit-specific imports.  
• Use environment variables for all secrets.  
• Comment every public function.  
• Use docopt-style CLI help.  

# Begin coding now.
