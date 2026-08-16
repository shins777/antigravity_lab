---
description: Enforce team error handling and logging standards
trigger: always_on
---

# Error Handling & Logging Guidelines

1. **No Silent Exception Swallowing**: Never catch exceptions with empty blocks or return silent dummy fallbacks (`except Exception: pass`).
2. **Explicit Diagnostics**: Always log or re-raise errors with context (file, function name, root cause).
3. **Upstream Tracing**: When an API or function receives missing or null data, trace and handle the root provider rather than patching symptoms downstream.
4. **Structured Error Types**: Prefer specific exception classes (e.g., `ValueError`, `KeyError`, custom domain exceptions) over generic `Exception`.
