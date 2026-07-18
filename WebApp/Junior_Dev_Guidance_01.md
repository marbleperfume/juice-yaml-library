# Junior Dev Guidance #1: Architecture Concerns & Optimization Path

**Context:** The Juice Design Hub (WebApp) is an LLM-supported game design authoring tool that edits live YAML files and will eventually export to UE5 GameplayAbility/GameplayEffect DataTables.

**Date:** July 2026**Status:** Pre-Vite migration, single `components.js` frontend, FastAPI backend working

---

## Where We Are Now

A FastAPI backend reads/writes YAML files directly on disk, with a browser UI for editing. The YAML files *are* the source of truth for game classes, skills, attributes, and balance. The system is designed so:

1. A human can edit game design through the UI
2. LLMs can read/reason about the files efficiently (file splits, schemas, validation)
3. Eventually, UE5 consumes this data as GameplayAbility/GameplayEffect DataTable rows

---

## Concern 1: The Frontend Is a Bottleneck for LLM Collaboration

**Problem:** The 27 KB `components.js` isn't just hard for LLMs to read — it's hard for LLMs to *help improve*. Asking "add a new column to the Tracker panel" forces the LLM to ingest the entire file, find the TrackerPanel function, hold surrounding context, and produce a targeted edit.

**Why it matters:** This project uses LLMs as primary development assistants. Every file over ~8 KB increases the chance of hallucinated edits or missed context. A full reread consumed over 500 KB in tokens.

**Fix:** Vite migration with file splitting. Each component file becomes a self-contained unit an LLM can reason about in isolation. See `VITE_SETUP.md` for the scaffold plan.

---

## Concern 2: No Type Safety Between Backend and Frontend

**Problem:** The backend returns JSON shapes like:

```python
return {"attributes": ..., "derivedStats": ..., "pendingCoefficients": ..., "statOverrides": ...}

```

The frontend calls `fetch('/api/attributes')` and trusts whatever comes back. If you rename a key in Python, the frontend silently breaks — no error until you open the page and something is `undefined`.

**Why it matters for UE5 migration:** When mapping these structures onto GameplayEffect DataTable schemas, mismatches between what the YAML says, what the API returns, and what UE5 expects will be the #1 source of bugs. There's no contract enforcement across that boundary today.

**Fix (incremental):**

- **Short term:** The `Schemas/` folder already has JSON schemas. Backend validators enforce YAML→Schema. That's half the story.
- **Medium term:** Add TypeScript types on the frontend that mirror those schemas. Vite + TypeScript is zero-config.
- **Long term:** Auto-generate both Python models (Pydantic) and TS types from the same JSON schema file. One schema, three consumers (validator, API, UI).

---

## Concern 3: The "Live Repo Files" Model Has No Undo

**Problem:** The backend writes directly to the working tree. The README says "no copy, no database." That's elegant but dangerous — a bad save corrupts the source of truth immediately. Git is the only safety net, and only if you committed before the bad edit.

**Why it matters:** As more editing features are added (Ability Editor, stat overrides, etc.), the blast radius of a bug in `repo.py`'s merge logic grows. One malformed `merge_write_yaml()` call could silently drop keys from a class file.

**Fix:**

- **Auto-commit on save** — a small addition to the write endpoint: `subprocess.run(["git", "add", "-A"])` + commit with a message like `"WebApp: edited Skills/Fireball.yaml"`
- Or: write to a staging branch and review diffs before merging to `main`
- The validators already catch drift (`stat.drift`) — that's good defense-in-depth

---

## Concern 4: The UE5 Export Path Isn't Typed End-to-End

**Problem:** The Roadmap says Phase 3 is "map typed Effects onto GameplayEffect/GameplayAbility DataTable rows." But the current path is:

```
YAML file → Python dict → JSON API → ??? → UE5 DataTable

```

That `???` is where things get hard. UE5 DataTables expect specific row structures (FTableRowBase subclasses). The typed Effects schema was designed as the prerequisite, but there's no code yet that validates "this Effect block would produce a valid DataTable row."

**Why it matters:** If 200 skills are designed in YAML and then 30% of them use effect patterns that don't map cleanly to UE5's GameplayEffect system, that's a massive rework. Better to catch it early.

**Fix (when ready for Phase 3):**

- Define a `UE5_Export_Contract.yaml` — the subset of effect types that have confirmed GE mappings
- Add a validator severity: `skill.unexportable` — "this effect type has no UE5 mapping yet"
- Build the export as a CLI tool first (`generate_datatables.py`), not a UI feature

---

## Concern 5: Validator Coverage vs. Validator Speed

**Problem:** There are two validator systems:

- `Project_Validator.py` (original, root-level)
- `WebApp/backend/validators/` (new, schema-driven)

The new one wraps the old one (`core.integrity`). But the new validators load every YAML file in the repo to check schemas. As more classes and skills are added, validation gets slower.

**Why it matters:** If validation takes >5 seconds, you stop running it after every save. Then errors accumulate.

**Fix:**

- **Incremental validation** — only re-validate files that changed since last check (`git diff --name-only`)
- The WebApp's `/api/validate` endpoint could accept an optional `files=[]` parameter for targeted validation
- Cache the schema loads (they don't change between runs)

---

## Concern 6: Single-Developer, Two-Machine Drift

**Problem:** Work happens across a managed AWS machine and a personal machine. The integrity layer is Git, but forgetting to push/pull means divergent YAML edits.

**Why it matters:** Class files are large and interdependent (stat overrides reference Base_Attributes, skills reference effect types). A merge conflict in a 40 KB YAML file is painful to resolve.

**Fix:**

- Keep commits small and frequent (one class or one system change per commit)
- Auto-commit-on-save (from Concern 3) helps here too
- Consider a pre-push hook that runs validators — never push broken state

---

## Priority Order

| # | Task | Why |
| --- | --- | --- |
| 1 | **File split (Vite migration)** | Unblocks LLM-assisted development of the UI itself |
| 2 | **Auto-commit on save** | Safety net, almost free to implement |
| 3 | **TypeScript types from schemas** | Catches frontend/backend drift early |
| 4 | **UE5 export contract** | Prevents designing skills that can't ship |
| 5 | **Incremental validation** | Quality-of-life, do when it starts feeling slow |

---

## Progress Tracking

- [ ] Vite scaffold created (`package.json`, `vite.config.js`)
- [ ] `npm install` succeeds
- [ ] `npm run dev` serves on :5173 with proxy to :8400
- [ ] `components.js` split into individual JSX files
- [ ] All 6 components render correctly after split
- [ ] Auto-commit logic added to write endpoint
- [ ] TypeScript types drafted from JSON schemas
- [ ] UE5 export contract defined
- [ ] Incremental validation implemented

