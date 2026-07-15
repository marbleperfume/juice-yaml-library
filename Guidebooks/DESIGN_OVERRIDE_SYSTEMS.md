# DESIGN_OVERRIDE_SYSTEMS.md
## System-Level Rules & Architecture — juice-yaml-library
### Continuation of DESIGN_OVERRIDE.md (§15 onward)

<!-- ▲ CONTINUES FROM: DESIGN_OVERRIDE.md -->
<!-- ▲ Core philosophy (§1-14): Strategy Rank, Player Rank, Frontliner identity, -->
<!-- ▲ Parry, Capacitor Pull, Engagement Models, Rank 1 design, >50% HP rule -->

---

## 15. Healer Stat Architecture (MAG/MED Split)

**MAG = barriers + damage. MED = direct healing + drain/sustain.**

| Stat | Scales | Does NOT Scale | Healer Type |
|------|--------|----------------|-------------|
| MAG | Barrier strength, damage output | Direct HP restoration | Proactive (Elementalist) |
| MED | Direct healing, drain/sustain | Damage | Reactive (Siren, Shaman) |

---

## 15b. Healer Identity Triad

| Class | Stat | Behavior | Failure Mode |
|-------|------|----------|--------------|
| Elementalist (Tryll) | MAG 13 / MED 13 (split) | Barriers proactively → forced reactive when barriers break → CC for survival → Triage Over → mana crash | Deteriorates under pressure. Mediocre on purpose. Ramp = situation worsening. |
| Siren/Cantor (Merryin) | MED primary | Constant passive healing through Charm drain economy. Scales with battlefield presence. | Deteriorates in isolation. Needs enemies + allies nearby. |
| Shaman (Soue) | Choice-dependent | Heals by SACRIFICING enemy debuffs (Harvested state). Not primary healer. | Must choose: keep enemy weak OR heal team. Cannot do both. |

---

## 15c. Healers CANNOT Replace Frontline

**Solo healers are NOT designed to replace frontline.** Explicit anti-pattern for ALL healer classes. Every healer design must have a clear reason they die in sustained melee combat:
- Elementalist: mana crashes under sustained reactive healing
- Siren: Charm Stage 3 pulls enemies TO her (dangerous for a healer)
- Wavecaller: slowed on land, needs water portals for full throughput
- Shaman: sacrificing debuffs to heal removes offensive pressure

---

## 15d. Siren Charm Economy

Charm as central mechanic — sustain comes from making enemies/allies LOVE her:
- **Stage 1 (Fascination):** Enemy deprioritizes Siren as target. Minor drain trickle.
- **Stage 2 (Infatuation):** Enemy approaches Siren (repositioning tool). Moderate drain.
- **Stage 3 (Devotion):** Full behavioral override, max drain. BUT enemy now in melee with Siren.

Ally Charm stacking: Allies near Siren build attachment → receive passive healing from enemy drain. Charmed allies draw indirect aggro from charmed enemies.

Control-oriented players deteriorate from misreading Position × Action × Time — wrong Charm target, wrong refresh timing = Charm drops, exposed, no heals.

---

## 16. SPD Stat ≠ Movement Speed

**SPD = reaction time, dodge frames, animation speed. NOT walk/run speed.**

All classes walk/run at the same base movement speed. SPD affects:
- Dodge i-frame duration
- Animation cancel windows
- Reaction-based mechanic timing (parry windows scale with SPD)

A Siegebreaker (SPD 5) walks at normal pace. Cannot dodge, cannot react, cannot be stopped.

---

## 16b. CC Immunity as Core Trade

Low-SPD/NTU classes receive **CC immunity** instead of reaction-based survival:
- Siegebreaker: SPD 5 / NTU 3 but immune to stun, knockback, root, fear, sleep, pull, silence, slow
- CC immunity always active while Endurance > 0
- This is the TRADE for having no dodge frames and no parry window

---

## 16c. Momentum Ramp-Up

Directional commitment builds speed (Siegebreaker):
- Momentum Gauge: Moving → Rolling → Charging → Unstoppable (4 tiers)
- Direction change resets momentum to zero
- Once committed and built up: ACCELERATES beyond base speed
- "I walk at normal speed. Can't dodge, can't react, can't be stopped. Once I build momentum, I get FASTER."

---

## 17. Feedback-Based Detection (No Gauges)

For feral/pursuit classes (Reaver), internal state communicated through environmental feedback, NOT on-screen meters:
- Enemy behavior changes (flinching → staggering → blood trail → red outline)
- Audio cues (faint bass → rapid heartbeat → THUMP)
- Visual effects (subtle red vignette → screen pulse)
- Hotbar skill swaps (available skills change based on state)

**HP bar is the ONLY numeric resource displayed.** Player reads the game state. Reading IS the skill.

---

## 17b. Sated State (Pursuit Termination)

Post-pursuit forced calm period (Reaver):
- Cannot re-engage Frenzy/berserk after pursuit ends
- Duration scales with Frenzy length (15-25s)
- Has its OWN dedicated gameplay (defensive skills, party buffs, recovery)
- NOT a cooldown timer — it's a real playstyle with active decisions
- Physiological refractory period (body cooling down after exertion)

---

## 18. Skill Budget Rule

**Skills that do nothing waste budget.** Merge passive/waiting skills with functional feedback skills.

Anti-pattern: A skill whose only purpose is "I'm waiting" or "I'm preparing."
Correct: Every skill press produces IMMEDIATE output (damage, movement, debuff, information) even if its secondary purpose is building toward something larger.

---

## 19. Colony = Special Tier

Colony (Harvesters) upgraded from Base to **Special** tier:
- 3 phenotypes (Builder/Flutter/Nightfly) = 3 complete mastery paths
- Each phenotype is its own game with unique resource interactions
- Deceptively complex despite simple individual actions

---

## 19b. Harvesters Fly (Racial Trait)

All Harvesters have innate flight. Colony class leverages this:
- Builder: 80% flight speed (construction focus, less mobile)
- Flutter: 120% flight speed (aerial bomber, permanent flight viable)
- Nightfly: 100% flight speed (balanced, darkness zones from above)

---

## 20. Water Slime = Invulnerable Spirit (Spiritcaller)

Lower Drakol racial companion:
- Water elemental spirit, NOT a pet/creature
- Cannot be killed, has NO HP. Always present.
- Produces water passively (puddles, terrain interactions)
- Player manages proximity: close = safe (Moisture maintained), far = healing allies (Moisture drains)

---

## 20b. Moisture Gauge (Spiritcaller)

Defensive resource (0-100):
- High Moisture = DR bonus (wet skin absorbs impact)
- Low Moisture = vulnerable
- Slime proximity maintains Moisture passively
- Water skills COST Moisture (offense vs defense trade)
- Core tension: keep Slime close (stay safe) vs send Slime far (heal allies, lose DR)

---

## 20c. Hydration Gauge (Wavecaller)

Water exposure tracking:
- High Hydration = full healing power + normal movement speed
- Low Hydration = healing reduced + movement SLOWED on land (not rooted)
- Water portals and submerging restore Hydration
- Creates terrain preference: water zones = Wavecaller thrives, dry land = Wavecaller weakened

---

## 20d. Wavecaller Identity

**Dolphin/orca/killer whale.** Physical, fast, playful-violent predator.
- NOT Siren. No charm, no enchantment, no lure, no allure.
- Weapon: Harpoon (aquatic hunter)
- Sound magic = healing (fast, AoE, possibly no LoS)
- Water portal dive = damage delivery
- The AGGRESSIVE HEALER — wants to fight but should be healing. Push/pull tension IS the class.

---

## 21. Strix Ground State

Weaker altitude-themed ground variants for corridors/caves:
- Low hops, short glides, wall-jumps
- Ground = weaker but FUNCTIONAL (not helpless)
- Storm Talons (dual elemental short blades) for ground combat
- Ground outputs 55-60% DPS reference (dive = full power)

---

## 21b. Evasion Baked into Dashes (Strix)

Dashes GUARANTEE evasion frames (not chance-based):
- DEX → frame duration (0.3-0.5s)
- EVA → dash cooldown reduction (4s → 2.5s)
- SPD → distance (6m → 10m)
- Fantasy: "don't get hit" — untouchable FEEL when dashing

---

## 21c. Regen Starts on Descent

Recovery begins the MOMENT altitude decreases (Strix):
- "Thermal Recovery" triggers on downward movement
- 3% HP/s during dive descent, continues 4s tapering on ground
- Ascent cancels regen
- Cycle: up = spend, down = recover

---

## 22. Low STR Weapon Philosophy

Low-STR classes use elemental/poison weapons (damage from weapon properties, not raw strength):

| Class | Weapon | Property | Rationale |
|-------|--------|----------|-----------|
| Spiritcaller | Trident | Water/elemental (Moisture-powered) | Three-pronged = spread/multi-hit potential |
| Wavecaller | Harpoon | Physical + sound (MED-scaled) | Reach weapon, piercing, aquatic predator |
| Strix | Elemental/Poison (type TBD) | Elemental coating | Flight-compatible, light weapon required |

---

## 23. File Structure — Class-Chain Split Principle

Class specifications MUST split into a multi-file chain. **Target 20-30 KB per file.** Never hardcode to exactly 2 files — use as many as the content naturally demands.

| File | Target Size | Contains |
|------|-------------|----------|
| `{Class}_Design.yaml` | 20-30 KB | Identity, race lock, role objective, class mechanic (resource system, state machine), rotation philosophy, anti-patterns, design notes |
| `{Class}_Systems.yaml` | 20-30 KB | Class-specific systems (unique subsystems, gauges, companion AI, stance logic — anything mechanically complex enough to warrant its own file) |
| `{Class}_Skills.yaml` | 20-30 KB | Full GCD/oGCD skill roster with potencies, rank progression |
| `{Class}_Validation.yaml` | 15-25 KB | Balance targets, system interactions, matchup analysis, item baseline comparison, balance validation, visualization hooks, constraints |

**Header cross-references (mandatory):**
```yaml
# In {Class}_Design.yaml footer:
# ▼ CONTINUES IN: {Class}_Systems.yaml, {Class}_Skills.yaml, {Class}_Validation.yaml

# In each continuation file header:
# ▲ CONTINUES FROM: {Class}_Design.yaml
# ▲ THIS FILE COVERS: [brief scope statement]
```

**Chain extension for complex classes:**
```
Colony_Design.yaml
Colony_Systems.yaml
Colony_Skills_Builder.yaml
Colony_Skills_Flutter.yaml
Colony_Skills_Nightfly.yaml
Colony_Validation.yaml
```

**Splitting philosophy:**
- **AIM FOR MORE FILES, NOT FEWER.** 3-5 files per class is normal. 2 is the minimum, not the target.
- 20-30 KB per file keeps each file readable in one pass and generatable without trim.
- If a section (e.g., altitude system, companion AI, stance logic) is complex enough to explain independently, it gets its own file.
- LLM generation quality degrades past ~30 KB output. Stay under.
- Each file must be independently readable (no dangling references).
- Files are cheap. Comprehension is expensive. Err toward more splits.

**Rules:**
- Design file is WHAT THE CLASS IS. Skills file is WHAT IT DOES.
- Systems file is HOW IT WORKS (mechanical subsystems in detail).
- Validation file is HOW WE CHECK IT (numbers, matchups, pass/fail).
- Potency changes, skill additions/deletions, balance tweaks → Skills file ONLY.
- Mechanic redesigns, identity shifts, resource reworks → Design file.
- Subsystem tuning (gauge rates, companion behavior) → Systems file.
- `_Complete.yaml` naming is DEPRECATED for new work. Existing files converted on next rebuild.

---

## 24. Document Chain — Design Override Split Principle

DESIGN_OVERRIDE.md itself follows the same chain logic. When this file exceeds **30 KB**:

| File | Contains |
|------|----------|
| `DESIGN_OVERRIDE.md` | Core philosophy (§1-14): Strategy Rank, Player Rank, Frontliner identity, Parry, Capacitor Pull, Engagement Models, Rank 1 design, >50% HP rule |
| `DESIGN_OVERRIDE_SYSTEMS.md` | System rules (§15+): MAG/MED split, SPD definition, CC immunity, feedback detection, Sated state, Colony tier, water systems, weapon assignments, file structure |

**Applies to ALL design documents.** Any `.md` or `.yaml` exceeding 50 KB should split at the natural design/implementation boundary. The chain is freely extensible — add or remove files as scope demands.

---

## 25. Resource Gating > Cooldowns (No Long CDs)

**Identity-defining skills are NEVER gated by long cooldowns (90s/120s/180s).** They are gated by RESOURCE COST — gauge, materials, field state, or consumables that the player actively earns through play.

### Why Cooldowns Fail

- 180s CD = 3 minutes where the class has no access to its defining power
- Player forgets the skill exists between uses → class identity is forgettable
- RPG encounter balance can't assume "maybe they used it 2 min ago"
- Opportunities permanently shut down by one bad timing → feels punishing, not strategic
- **Racially bound classes suffer double:** boring class = boring race

### Correct Pattern: Resource Gating

| Gate Type | How It Works | Example |
|-----------|--------------|---------|
| Gauge cost | Powerful skill drains gauge earned through combat actions | Reaver Frenzy (HP-gated, earned by fighting) |
| Material cost | Consumable resource (MonsterBone, Biomass, etc.) | Shaman summon deployment |
| Field state | Skill unlocks when battlefield conditions are met | Colony: terrain placed → big skill available |
| Escalation | Resource builds FASTER under pressure | Intensity-scaled gauge gen in hard fights |

### Key Principles

1. **Normal play emphasizes repetition or retreat to earn power.** The cycle of setup → payoff → reset → setup keeps the identity PRESENT. Never "wait 3 minutes."

2. **Intensity scales resource generation.** Bigger fights = more gauge = more access to powerful tools. The game REWARDS you for being in hard content with MORE of your class identity, not less. Avoid the pitfall of farming weak mobs for gauge to spend on bosses.

3. **Setup IS the resource.** For Colony, terrain placed = gauge accruing. For Shaman, hexes maintained = Harvest available. The preparatory actions ARE the gating — the payoff comes FROM the setup, not despite it.

4. **Stage 3 CC as resource-gated power** (not just burst damage). A Colony Nightfly's paralysis dust on retreat lets the party turn around and rain hell. This is IMMENSELY powerful precisely BECAUSE it's Stage 3. It's earned through positioning and resource, never trivially available on a timer.

5. **Never permanently shut down.** A missed opportunity costs time/resources to rebuild, NOT a 3-minute lockout. Player can retreat, re-earn, re-attempt. The punishment is inefficiency, not inaccessibility.

6. **Class identity present in EVERY engagement.** Player is always either USING the thing that makes their class/race special, or BUILDING TOWARD it. Zero dead-identity windows.

### Anti-Patterns

- ❌ 180s/120s/90s cooldowns on identity-defining skills
- ❌ Building gauge on weak enemies to spend on strong ones
- ❌ Spike-and-forget identity (3 strong hits then filler for 2 min — ToS Featherfoot problem)
- ❌ Opportunities permanently shut down by one bad timing
- ❌ "Ultimate" skills that exist outside normal play flow

### Correct Anti-Example: ToS Featherfoot

Featherfoot spews debuffs for 3 strong Kundela Slash hits, then goes back to Blood Sucking or other class rotations. The class identity (curse damage) only exists for ~10s every 30-40s. The rest is filler from a different class. This makes the identity forgettable. Colony/Shaman/any race-locked class CANNOT have this problem — the race will look boring.

### Short Cooldowns Are Fine

Tactical cooldowns (5-15s) that gate individual skill FREQUENCY without removing class identity are acceptable. The rule targets cooldowns long enough to create "dead identity" windows where the player has no access to what makes their class special.

---

---

## §27. Melee-Range Transformation (Anti-Dash-Button Redundancy)

**Problem:** FFXIV design excuses gap closers as damage buttons (Plunge, Stardiver, etc.). These are dash skills that deal damage as a bonus for pressing them — the actual purpose is "move to melee." This creates redundancy: the dash IS the damage, so you always press it on cooldown regardless of positioning need.

**Potential Solution (Samira model):** Basic attacks transform based on distance to target. Gun at range → sword at melee. No separate dash skill needed — movement itself changes what your attacks do.

**Implications if adopted:**
- Gap closers stop being damage buttons. They become PURE movement (no potency, or token potency).
- OR: gap closers don't exist at all. Walking/running into range transforms your attack automatically.
- Ranged attacks at range → melee attacks at melee. Same button, different output.
- Prevents "I dash on CD for damage even though I'm already in melee" anti-pattern.

**Scope:** Potentially affects multiple classes (any with a dash/gap closer). Not Skyreign-specific.

**Status:** OPEN QUESTION. Not yet adopted as rule. Flagged for evaluation during quantitative pass.

**Classes to evaluate:** Skyreign (Voltaic Rush), Strix (dive), Lancer (jump in/out), any melee with gap closer.

---

## §28. Chain Reactions vs Crits (Distinct Systems)

**Problem:** Skills files conflate "overlapping effect bonuses" with crit conditions. Overlapping terrain, stacking debuffs, and combined elemental effects are CHAIN REACTIONS (Layer 3 of Hierarchy of Fun: Synergy). They are NOT crits.

**Crits** = positional/conditional damage multiplier on a SINGLE action.
- Backstab, flank, CC exploit, >50% HP, cone center, combo finisher.
- One skill, one condition, one multiplier. No setup from separate source needed.

**Chain Reactions** = bonus effect triggered by COMBINATION of multiple sources.
- Overlapping terrain zones (fire + poison = explosion).
- Black Lightning + external elemental hit = reaction damage.
- Debuff A + Debuff B on same target = amplified effect.
- Two terrain lines crossing = enhanced zone at intersection.
- Requires setup from SEPARATE action/source/ally. Reward for coordination.

**Why this matters:**
- Crits reward INDIVIDUAL execution (position yourself correctly).
- Chain reactions reward COORDINATION (team play, setup→payoff, spatial planning).
- If chain reactions are labeled as "crits," the crit system loses meaning (becomes "everything is a crit").
- Chain reaction bonuses can exceed crit multipliers because they require more investment.

**Rule:** When writing skills files, categorize bonus damage sources correctly:
- Single-action conditional bonus → CritCondition field
- Multi-source/multi-action combinatorial bonus → ChainReaction field (separate)
- Do NOT put chain reactions in CritCondition. Do NOT put crits in ChainReaction.

**Scope:** Affects all classes with terrain, debuff stacking, elemental interactions, or overlapping zone mechanics. Particularly: Skyreign (breath terrain overlap), Tryll Elemental Scholar (saturation cross-element), Shaman (hex stacking), Colony (structure interactions).

## §29. Element Selection as UI Mode Swap

Breath/element selection (e.g. Dragonguard fire/ice/poison) is a **UI button mode swap** — trivial if unnecessary (Rank 1 content where any element works) but provides meaningful choice at higher ranks. Not a rotation. Not a combo. A menu selection that changes what your next breath DOES.

**Scope:** Any class with multiple element/damage type options on the same skill slot. The swap is free, instant, out-of-combat or between casts. NOT an in-combat decision cost — the COST is choosing wrong for the situation, not the act of switching.

---

*Last updated: 2026-07-15*
*Source conversation: Healer identity session + file structure reform + resource gating principle + Skyreign review*
