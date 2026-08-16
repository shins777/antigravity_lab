---
description: Enforce Conventional Commits rule for all git commits
trigger: always_on
---

# Commit Message Guidelines

When creating Git commit messages, strictly adhere to the Conventional Commits specification:

1. Format: `<type>(<scope>): <subject>` (e.g. `feat(auth): add jwt token validation`)
2. Allowed Types:
   - `feat`: A new feature
   - `fix`: A bug fix
   - `docs`: Documentation only changes
   - `style`: Changes that do not affect the meaning of the code (white-space, formatting)
   - `refactor`: A code change that neither fixes a bug nor adds a feature
   - `test`: Adding missing tests or correcting existing tests
   - `chore`: Changes to the build process or auxiliary tools and libraries
