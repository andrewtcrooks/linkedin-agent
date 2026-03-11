# Memory Routing Policy (QMD + mem0)

## Active stack

1. **QMD** (fast factual/document lookup)
   - Use for: file/workspace facts, code/doc references, "where is X", "what did we write"
   - Commands: `QMD_FORCE_CPU=1 /home/claw/.bun/bin/qmd query "..."` or `qmd search "..."`
   - 3 built-in models: embeddinggemma (embed), Qwen3-Reranker (rerank), qmd-query-expansion (expand)

2. **mem0** (user preferences + conversational habits)
   - Use for: "remember this", style/preferences, recurring user patterns
   - Add after meaningful interactions; search before personalized responses
   - Requires: `mem0-llamacpp-start` (ports 8011 LLM / 8012 embed)

## Write policy

- **QMD**: workspace documents/chunks — updated via `qmd update && qmd embed`
- **mem0**: compact preference/pattern memories — add via `mem0-add.js`, search via `mem0-search.js`

## Fallbacks

- If mem0 servers not running: start with `mem0-llamacpp-start`, wait for readiness
- If QMD vectors incomplete: run `QMD_FORCE_CPU=1 qmd embed` (incremental, safe to retry)

## PATH note

Always use full path in automation: `/home/claw/.bun/bin/qmd`
Or prepend: `export PATH="/home/claw/.bun/bin:$PATH"`

## Shelved (future use)

- **Cognee** — graph/relationship reasoning. Scripts preserved at `bin/cognee-local` and `bin/patch-cognee-local`.
  Shelved because: too CPU/RAM heavy for current Pi hardware. Revisit with faster Pi or more storage.
