# DESIGN_OVERRIDE_PROGRESSION.md
## Skill Unlock Quests & Strategy Rank — Supersedes Mercenary Rank System
### Authority: This document deprecates ALL references to "Mercenary Rank" as a player progression system.

---

## 1. What Was Deprecated (and Why)

### Mercenary Rank — REMOVED

The old system used a numeric player rank (Low 1-2 → Mercenary 3-4 → Strategist 5+) as a gate for:
- Class availability ("Merc Rank 2 to unlock Lancer")
- Content access ("Merc+ content demands solo operation")
- Skill ceiling expectations ("Parry becomes primary at Merc rank")

**Why it was removed:**

1. **LLM context cost.** The system creates a parallel evaluation layer (player rank vs. enemy strategy rank vs. class power tier) that forces re-parsing of contradictory rules across files. Every reference to "Mercenary" requires the LLM to distinguish between player progression gates and enemy AI tiers — consuming tokens to resolve ambiguity that shouldn't exist.

2. **Contradiction with Strategy Ranks.** Strategy Ranks already define what the game EXPECTS from the player at each tier. A separate "Mercenary Rank" measuring the same thing (player comprehension) under a different name creates variable drift — one says "Rank 3 = you split the party" while the other says "Merc 3 = you access special classes." These are different claims that share a number.

3. **The underlying ask is comprehension, not grind.** What "Merc Rank 3" actually meant was "this player understands timing and positioning." That's provable through a quest — not through XP accumulation.

4. **Cannot be expressed as a UE5 system cleanly.** A numeric grind rank tied to both class gates AND behavior expectations is two systems pretending to be one. Skill Unlock Quests are one clean system: trial → comprehension proven → ability granted.

---

## 2. What Replaces It: Skill Unlock Quests

### Core Principle
Every ability is individually gated behind a **quest that teaches the player why that ability matters and how to time it.**

### Structure
```
Skill Unlock Quest:
  trigger: Player reaches prerequisite point in progression
  quest_type: Trial / Scenario / NPC challenge
  teaches: The specific mechanic this ability introduces
  pass_condition: Player demonstrates comprehension (not just survival)
  reward: Ability permanently unlocked
```

### Strategy Rank Bars Abilities (Not Classes)

Abilities are barred from lower Strategy Ranks **if and only if** simulations show they would trivialize content at that rank.

| Condition | Result |
|-----------|--------|
| Ability does not break R1 sim balance | Available at R1 via quest |
| Ability overwhelms enemies at R1 but is balanced at R2 | Barred until R2 content is reached; quest available then |
| Ability requires R3 enemy behaviors to have counterplay | Barred until R3 content |

**This is per-ability, not per-class.** A class available at R1 may have 3 abilities locked behind R2 quests and 1 behind R3. The player still plays the class — they just don't have the full kit until they've proven they understand the full kit.

### Why Per-Ability (Not Per-Tier)

Bundling abilities into "you unlock your R2 kit" creates the same batch-gate problem as Mercenary Rank. Individual quests:
- Let players unlock in any order within a rank tier
- Create discoverable content ("oh, THAT quest gives me Sound Redirect?")
- Allow simulation-driven balancing (one ability might shift from R1→R2 during testing without dragging the whole tier)

---

## 3. Strategy Ranks — Retained, Clarified

Strategy Ranks remain the **sole difficulty/complexity axis.** They describe enemy AI behavior AND, by extension, what the content demands from players.

| Strategy Rank | Enemy Behavior | Player Demand | Content Feel |
|---------------|----------------|---------------|--------------|
| 1 | Attack nearest. No tactics. | Execute basics. Cluster. Mash. | FFXIV Normal |
| 2 | Path toward squishies. Positionals appear. | Read enemy pathing. Position intentionally. | FFXIV Extreme |
| 3 | Flank, coordinate, retreat when low, target installations. | Displacement, timing, order-of-operations. | Monster Hunter |

> **Note:** The 1-4 split in the original DESIGN_OVERRIDE.md (Rank 4 = "proactive strategy") is retained pending review. For class design purposes, R1-R3 is the primary framework. R4 is boss-specific behavior and does not gate abilities differently from R3.

### What Strategy Rank Is NOT
- NOT a player XP level
- NOT a prerequisite number attached to the player's profile
- NOT something the player "earns" — it's something the CONTENT has
- The player accesses R2 content by reaching the area/quest that contains R2 enemies, not by grinding R1 to fill a bar

---

## 4. Class Availability — No Rank Gate

### Old Model (DEPRECATED)
```
Base Available (No Merc gate) → Experienced (Merc Rank 2) → Special (Merc Rank 3)
```

### New Model
```
All classes are available when narratively appropriate.
```

Class access is determined by:
1. **Narrative location** — "You can learn Shaman when you reach the Soue forest" (geographic, not grind)
2. **Racial prerequisite** — Racially locked classes require being that race (unchanged)
3. **Prerequisite quest** — May require completing a scenario that establishes the class fantasy ("defeat the trial guardian using only positioning" → unlocks Lancer)

Classes are **never** gated behind a numeric rank grind. A player who speedruns to the Soue forest at level 1 can start Shaman if they can survive the prerequisite quest.

---

## 5. Role Subcategories — Per-Role Naming (Principle)

Subcategory labels are scoped to a single role. They are NOT shared vocabulary.

**Why:** LLMs parse subcategory names as behavioral definitions. If "Zone Control" appears in both frontliner and healer contexts, the LLM will bleed the frontliner ruleset (enemy disadvantage at positions) into healer design (ally healing at positions). These are mechanically different behaviors that happen to share spatial language.

Per-role naming prevents:
- Cross-contamination of behavioral rules between roles
- Token bloat from loading irrelevant role context during class design
- Ambiguous reads where one label carries two incompatible definitions

**Where subcategories are defined:**
- Frontliner: `DESIGN_OVERRIDE_FRONTLINE.md`
- Healer: `DESIGN_OVERRIDE_HEALER.md`
- DPS: `DESIGN_OVERRIDE_OTHER_ROLES.md` (pending)

**Rule:** Subcategory definitions for one role NEVER reference another role's subcategory. They are isolated namespaces.

---

## 6. Skill Unlock Quest Design Principles

1. **Teaches before testing.** The quest scenario should demonstrate the ability's value BEFORE asking the player to execute it under pressure.

2. **Failure is informative.** Failed quest attempts must communicate WHAT went wrong ("you used Sound Redirect too early — the rusher hadn't committed yet") not just "you died, try again."

3. **No grind component.** Quest attempts are unlimited. No consumable cost. No "wait 24 hours." The only gate is player comprehension.

4. **Simulated teammates when solo.** Unlock quests can simulate party members so the ability's ROLE is clear even to a solo player.

5. **Strategy Rank matching.** If an ability is barred to R2, its unlock quest uses R2-behavior enemies. The player proves they can handle R2 pressure WITH this new tool.

---

## 7. Deprecated Terminology — Do Not Use

| Term | Replacement | Reason |
|------|-------------|--------|
| Mercenary Rank | (removed entirely) | Conflated progression gate with comprehension tier |
| Merc+ content | R2+ content / "content with R2 enemies" | Strategy Rank names the difficulty |
| "Low Rank (1-2)" as player label | "R1 player" or "player in R1 content" | Player doesn't have a rank; content does |
| Strategist (5+) | R3 mastery / "player executing at R3" | Same — describe behavior, not a badge |
| "No Merc gate" | "Available via narrative access" | No gates are numeric anymore |
| "Experienced (Merc Rank 2)" | "Requires [specific quest] in [location]" | Geographic/narrative, not grind |
| "Special (Merc Rank 3)" | "Requires [specific trial]" | Trial-gated, not grind-gated |

---

## 8. Supersession Notice

This document supersedes the following content in other files:

| File | Section | What is superseded |
|------|---------|-------------------|
| `DESIGN_OVERRIDE.md` §2 | Player Rank table (Low/Merc/Strategist) | Replaced by §3-4 of THIS file |
| `DESIGN_OVERRIDE.md` §2b | "3-4 (Merc)" feel references | Use R2/R3 labels only |
| `DESIGN_OVERRIDE.md` §3c, §3e | "Merc+" language | Read as "R2+" |
| `class_list_qual_context.md` | Section headers | Already updated to narrative access model |
| Any class YAML | "mercenary_rank" as unlock condition | Read as quest-gated per §2 of this file |

Until these files are individually revised, read them through the lens of THIS document. Where Mercenary Rank language conflicts with this guidebook, this guidebook wins.

### Files Still Requiring Individual Revision

The following files contain Mercenary Rank references that now conflict with this guidebook:

| File | Issue | Action |
|------|-------|--------|
| `DESIGN_OVERRIDE.md` § 2 (Player Rank) | Defines Low/Merc/Strategist tiers | Rewrite: remove player rank table, retain Strategy Rank as content-only |
| `DESIGN_OVERRIDE.md` § 2b | References "3-4 (Merc)" in feel table | Replace with R2/R3 labels |
| `DESIGN_OVERRIDE.md` § 3c, 3e, 5 | "Merc+" language | Replace with "R2+" (strategy rank of content) |
| `DESIGN_OVERRIDE.md` § 14 (override table) | "Parry = skill-gated self-heal at Merc+" | Replace with "at R2+" |
| `Class List — Qual Context.md` | "Experienced (Merc Rank 2)" and "Special (Merc Rank 3)" section headers | Replace with narrative/quest-based access descriptions |
| Various class YAMLs | May reference "mercenary" as unlock condition | Replace with quest reference |
| `LLM.md` (GitHub only) | Original source of rank system | **DELETE from repository** — fully superseded by DESIGN_OVERRIDE stack |

---

## 9. Relationship to Other Guidebooks

```
DESIGN_OVERRIDE.md          — Combat philosophy, role identity, spatial rules
DESIGN_OVERRIDE_HEALER.md   — Three-axis model, free HPS, survival clock
DESIGN_OVERRIDE_FRONTLINE.md — Frontliner subcategories, tanking without enmity
DESIGN_OVERRIDE_RACIAL_LOCKS.md — Unique passives (not biology)
DESIGN_OVERRIDE_PROGRESSION.md (THIS FILE) — How abilities unlock, what gates mean
```

This file does NOT override combat mechanics. It overrides HOW PLAYERS ACCESS combat mechanics. If another guidebook says "at R2, the player needs X" — that's fine. It means the CONTENT demands X. This file ensures we never say "at Merc Rank 3, the player unlocks X" — that phrasing is dead.

---

*Last updated: 2026-07-16*
*Source: Session discussion — healer identity → role integrity → subcategory variety → Mercenary Rank deprecation*
