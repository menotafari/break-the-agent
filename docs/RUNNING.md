# Running against a real local model

The unit tests use a scripted model and need nothing installed. To run a live
attack you need Ollama and a local model.

## One-time setup

1. Install Ollama on Windows (it serves to WSL over `http://localhost:11434`),
   or inside WSL. Confirm it responds: `curl http://localhost:11434/api/tags`.
2. Pull a capable instruct model, for example:
   `ollama pull llama3.1` or `ollama pull qwen2.5`.
3. Before a heavy run, note your current GPU driver version, so that if the GPU misbehaves you can tell a driver problem from a lab problem.

## Run an attack

```bash
uv run bta run prompt_injection_tool_abuse --model llama3.1
uv run bta run indirect_injection_exfil --model llama3.1
uv run bta run system_prompt_leak --model llama3.1
```

The writeups used `--model qwen2.5:7b`. To re-run an attack against its
patched target, add `--target`:

```bash
uv run bta run prompt_injection_tool_abuse --target chatbot_tools_hardened --model qwen2.5:7b
uv run bta run indirect_injection_exfil --target rag_app_hardened --model qwen2.5:7b
uv run bta run system_prompt_leak --target rag_app_hardened --model qwen2.5:7b
```

Each run prints SUCCESS or FAILED and writes `runs/<attack>.json`. Use that
transcript to fill in a writeup from `writeups/TEMPLATE.md`. A given attack may
succeed or fail depending on the model; both outcomes are worth a writeup.
