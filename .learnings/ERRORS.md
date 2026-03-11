# ERRORS

## [ERR-20260309-001] qmd-embed-download-rename-failure

**Logged**: 2026-03-09T19:00:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
`QMD_FORCE_CPU=1 qmd embed` failed after model download with ENOENT on `.ipull` → final file rename.

### Error
```
Error: ENOENT: no such file or directory, rename '/home/claw/.cache/qmd/models/hf_ggml-org_embeddinggemma-300M-Q8_0.gguf.ipull' -> '/home/claw/.cache/qmd/models/hf_ggml-org_embeddinggemma-300M-Q8_0.gguf'
Node.js v22.22.0
```

### Context
- Command: `QMD_FORCE_CPU=1 qmd embed`
- Host: Raspberry Pi (arm64)
- QMD: 1.1.0
- Prior issue: `qmd status` attempted CUDA build and failed; mitigated by `QMD_FORCE_CPU=1`.

### Suggested Fix
- Clean partial model artifacts and retry once:
  - remove stale `*.ipull` files in `~/.cache/qmd/models`
  - rerun `QMD_FORCE_CPU=1 qmd embed`
- If repeatable, pin/upgrade qmd or report upstream as downloader race/path bug.

### Metadata
- Reproducible: unknown
- Related Files: /home/claw/.cache/qmd/models
- See Also: ERR-20260309-000 (CUDA probe/build failure during status)

---
