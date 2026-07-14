# Game Juice Taste Design — juice-yaml-library

**Project:** Horizontal-progression co-op RPG (UE5)  
**Repo:** github.com/marbleperfume/juice-yaml-library  
**Author:** Marcos Colon  
**Method:** Qualitative → Quantitative → Qualitative cycle (squeeze until juice)  
**Current Phase:** Rebuilding foundation — Strategy layer must precede class identity. Classes are implementations of strategic roles, not standalone kits.

---

## The Hierarchy of Fun

Each layer depends on the one above it. Nothing below can be validated without its parent being defined.

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. STRATEGY (Foundation)                                        │
│    The problem space. What challenges EXIST before classes do.   │
│    Three quantitative axes: Position × Action × Time            │
├─────────────────────────────────────────────────────────────────┤
│ 2. CHARACTER GAMEPLAY (Sells)                                   │
│    Solutions to strategic problems. Classes are implementations. │
│    Monetization lives here — gacha characters with higher        │
│    ceilings, budget characters reward deep optimization.         │
├─────────────────────────────────────────────────────────────────┤
│ 3. CHAIN REACTIONS (Synergy)                                    │
│    Cross-class and class+item interactions. Oil + Fire.          │
│    The multiplayer juice — why specific comps matter.            │
├─────────────────────────────────────────────────────────────────┤
│ 4. SKILL PROGRESSION (Pacing)                                   │
│    Locked skills, weak initial designs, flashy sells fantasy.    │
│    Same skill at different CDs across difficulty tiers.          │
├─────────────────────────────────────────────────────────────────┤
│ 5. LOOT / REWARDS (Enhancement)                                 │
│    Only matters if gameplay loop satisfies. Adjacent to          │
│    "I found this drop!!" — enhances, doesn't carry.             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: STRATEGY (Foundation)

### The Three Quantitative Axes

Strategy is chess with free-flowing position and broad-but-windowed actions:

| Axis | What It Measures | Chess Analog | Our Implementation |
| --- | --- | --- | --- |
| **Map Position (x, y, z)** | Where you ARE relative to threats, allies, terrain, escape routes | Board squares, piece placement | Procgen rooms with elevation, corridors, LoS breaks |
| **Action Availability** | What you CAN do right now — resource gates, cooldowns, consumables in inventory | Which pieces can legally move | GCD, gauge, bone economy, consumable budget, skill locks |
| **Time to Achieve Action** | How long an action takes AND what you LOSE by committing (distance-not-traveled, other actions-not-taken) | Tempo, initiative | Cast times, GCD lock, movement cost during commitment |

**The design philosophy:**
- FFXIV uses time-mapped gameplay (2-min cycles, fixed rotations). We are AGAINST this.
- ToS budget players experience opportunity cost and dead time as PUNISHMENT. We take that same pressure and reframe it as CHOICE.
- Resource gating prevents permanently pushing forward → encourages planning PRIOR to engagement.
- The goal: make the chess-like decision density FUN by promoting choice rather than punishing failure.

### Why Strategy Must Come First

Most RPGs let melee enemies dominate the game space: easy to navigate, predictable, creates a safety net for ranged characters who don't have to do very much. **We are rejecting this.**

By changing that foundation, the entire system collapses and must be rebuilt from:

1. **What SHOULD a ranged character do?** (Not what CAN it do)
2. **How is their fun determined?** (By the strategic problems they're solving)
3. **When we finally get to melee classes** — the boiled-down strategy creates much narrower design intent and forces choices to be highly intuitive for the melee player.

**The cascade:**
- Strategy defines the PROBLEM (enemies threaten from angles, positions require commitment, time is finite)
- Items/consumables define the BASELINE solution (Smokescreen, Paralysis Bombs, Potions — anyone can access these)
- Classes define PREMIUM solutions (Shaman replaces Smokescreen with permanent accuracy debuff; Elementalist replaces Potions with sustained healing)
- A class that "replaces" a consumable offers better uptime/efficiency — but the consumable MUST EXIST as the universal fallback

### The Variance Source

**Map design is where strategy experiences the HIGHEST variance.** Modular design needs simplicity in that variance before classes end up eating the mental stack budget.

If the map is too complex → players can't process class decisions ON TOP of spatial decisions → cognitive overload.  
If the map is too simple → classes degenerate (proven: Elementalist in flat rooms = Fire spam).

The map must be complex enough to CREATE strategic problems but simple enough to READ quickly. League of Legends target: 3 limited choices + 1 committed choice at any moment. The map provides the constraints; the class provides the answer within those constraints.

### Strategy Rank (Enemy AI — Solved)

| Rank | Behavior | Strategic Pressure |
| --- | --- | --- |
| SR1 | FFXIV Normal. Cluster/mash/valid. | Minimal — learn your buttons |
| SR2 | Target evaluation. Paths to squishiest. | Positional — where you stand matters |
| SR3 | Terrain use + movement cost + coordinated spawns | All three axes engaged — position × action × time |
| SR4 | Instantly reactive, exploits gaps, hunts installations | Mastery of all three axes simultaneously under pressure |

### Items/Consumables as Baseline Strategy (The Scientific Control)

Items exist BEFORE classes conceptually. They define what's achievable by ANYONE:

| Strategic Problem | Item Solution (universal) | Class Solution (premium) |
| --- | --- | --- |
| Ranged enemies hitting your party | Smokescreen (accuracy debuff) | Shaman passive accuracy curse |
| Enemy too fast to kite | Paralysis Bomb (speed reduction + action nullification) | Shaman paralysis (Pokémon-esque: lowers speed, chance to nullify actions) |
| Party taking too much damage | Health Potion | Elementalist/Shaman healing |
| Need to approach safely | Decoy / Flash | Frontliner Unfocus / Adafold Force Targeting |
| Terrain blocking path | Mobility item (grapple? jump boost?) | Class-specific traversal |
| Enemy resists physical | Elemental oil / coating | Pyrien fire DoT, Elementalist convergence |

**Principle:** If a class can do it, a consumable MUST also do it (worse). This ensures no party composition is LOCKED OUT of strategic solutions. Classes offer better uptime/efficiency/scaling — not exclusive access.

### Quantitative Asks (🔴 Unanswered — Blocking)

**Consumable Economy:**

| # | Question | Status |
| --- | --- | --- |
| 1 | Acquisition — crafted / found / bought / procgen loot? | 🔴 |
| 2 | Carry limit — per dungeon? Per player? Shared pool? | 🔴 |
| 3 | Opportunity cost — use here vs save for boss severity? | 🔴 |
| 4 | Class-agnostic vs class-specific scope? | 🟢 ANSWERED — class-agnostic baseline, classes are premium replacements |
| 5 | Effect magnitude — how MUCH does Smokescreen reduce accuracy? | 🔴 |
| 6 | Duration — covers one engagement or one floor? | 🔴 |
| 7 | Stacking/exclusivity — multiple simultaneous? | 🔴 |

> **Economy skeleton entry point (PARTIAL):** Carry limits + price tag + crafter alternative = controls loot value AND economy structure. This is the starting framework for questions 1-3.

**Level Design Primitives (Position axis):**

| Variable | Why It Matters | Status |
| --- | --- | --- |
| Base movement speed (y/s) | Determines cast commitment as distance-lost | 🔴 |
| Room width/depth | Engagement range, kiting space | 🔴 |
| Corridor width | Physical blocking viability | 🔴 |
| Elevation tier height | LoS breaks, vertical cost | 🔴 |
| Traversal time (stairs/climb) | Class mobility advantage magnitude | 🔴 |
| Engagement distance (melee) | MW suction radius is 8y — what's that relative to room? | 🔴 |
| Engagement distance (ranged) | How far can archers threaten? | 🔴 |
| Cast commitment (distance-lost) | 2s cast × 5y/s = 10y not repositioned | 🔴 |
| Spawn geometry templates | Standard room shapes | 🔴 |
| LoS break density | Ranged aggro management via terrain | 🔴 |

**Time Axis:**

| Variable | Why It Matters | Status |
| --- | --- | --- |
| GCD (base/cap) | 2.0s / 1.4s — SOLVED | 🟢 |
| Gauge fill time | 12-16s first spend, 30-40s full — SOLVED | 🟢 |
| Consumable effect duration | How many GCDs does a Smokescreen buy? | 🔴 |
| Enemy re-evaluation timer by SR | How long do enemies COMMIT before switching targets? | 🔴 |
| Kill threshold (per SR tier) | How long until situation degrades if not resolved? | 🔴 |
| Resource gate recovery | How long until action becomes available again after spending? | 🟡 Per-class, partially solved |

---

## Layer 1 Addendum: Consumable Design Decisions (Resolved)

> **Source:** Annotations on the consumables reference list. These decisions are now **AUTHORITATIVE** — they override any conflicting speculation elsewhere in this document.

### HEALING SYSTEM

- **Healer triage system:** Triage Minor (party member hits 50% HP within 30y → healer ratio shifts to 50% DPS / 50% Heal, gains bonus movement speed) → Triage Over (regen burst, max MP cost, then mana recovery mode with lower DPS/HPS until mana catches up)
- **Anti-pattern: "let them drop first"** — healer feels URGENCY to heal early
- **Anti-pattern: Freecure design** — NO RNG procs that reward bad play
- Healer can't heal themselves efficiently (needs potions or party cover). **Exception:** Shaman (Blood Sucking/Hex Drain equivalent, lower DPS as tradeoff)
- Elementalist self-defense: CC + shielding, NOT healing. Long cast stuns with massive DPS loss = doesn't copy frontliner
- Hybrids (Paladin/Druid/Crusader): Less damage, substitute healer via aggro draw / barriers / terrain (Chortasmata)
- Materials that do nothing alone: **REJECTED**

### OFFENSE

- Attack buff items: Low priority unless Berserker archetype
- **Berserker identity (NOT Madolt):** heal-on-kill with decaying HP outside combat, OR bonus ATK/speed on missing HP
- Hero Drink (4x damage): Possible as Lost Action equivalent — fun vs normals, NOT bosses
- Haste: Converted to class self-buffs, not items
- On-hit effects: Class chain reaction enablers. % chance to apply debuff

### DEFENSE

- **Shield Generator archetype: CRITICAL.** Anti-ranged/anti-melee bubble. Low-use, ultimate defense
- Block = front-only damage reduction (ToS model). Madolt exception: 360° Electron Shield
- Jade Parcels = offense, not defense (miscategorized in reference)

### STATUS/DEBUFF

- **EXPAND this category** — highest variety, most strategy-aligned
- Tenebria Scroll = Smokescreen analog. Kept.
- Guard Spec: Must NOT work on Vulnerability or unique uncleansable debuffs

### CROWD CONTROL

- **EXPAND this category**
- Alluring Skull = Adafold's Force Targeting in item form
- Traps = installations (Sapper, Caltrops, Chortasmata terrain)
- Target agnostic — not "stagger humanoids only"

### UTILITY

- Recall skill replaces Homeward Bone (FFXIV model)
- **Resupply Pod concept: YES** — procgen rooms have interactable objects (mineral nodes, ammo caches, ingredients) creating "stop to gather or push forward?" decisions
- Stealth/invisibility items: KEEPING (scouting)
- No lock challenges, no waypoint items, no permanent stat boosts
- Flying races immune to fall damage unless CC'd. Ledge grab preferred over flat negation.

### ELEMENTAL

- Dragon's Dream (gas + fire trigger): Good chain reaction item
- Debuff cleanse items: For self-inflicted or when Esuna isn't available. Item cost HIGHER than skill cost.

### SUMMONING

- Companions are ABOVE item strategy — replace what a PLAYER does
- Summoning Clock: Shaman territory
- Invisible scout familiar: Needs to exist as item (Sadhu OoB / untargetable NPC)
- Shadow Clone: Dark Knight FFXIV model with limitations
- Auto-revive: Good for Berserkers gambling on death timing

### TRANSFORMATION/META

- Rebirth Flame: MANDATORY for open world, NOT for dungeons
- No drop boosters on f2p/budget. Period.
- Nitra scavenging in spirit: Resource gathering during runs = yes

### DESIGN PRINCIPLES (Consumable-Specific)

- **Team resource tension = healer pressure (insurance). Personal resource = skill issue.**
- Dual-edge items: Risk/reward, not self-damage. Bozja elixirs as reference.
- Shared AoE buffs: Speed + mitigation, NOT ATK
- **Carry limits + price tag + crafter alternative:** Controls loot value AND economy structure
- Knowledge-gated value: Fine for SR3+

---

## Layer 2: CHARACTER GAMEPLAY (Sells)

### Design Principle

Classes are SOLUTIONS to Layer 1 problems. They don't define the game — they give players a preferred APPROACH to the game's strategic demands.

**A class answers: "Given the strategic problem, what is my APPROACH?"**

- Shaman's approach: Make enemies less dangerous (debuff accuracy, slow movement, nullify actions, delegate damage to installations). The party fights EASIER enemies.
- MW's approach: Be the threat. Kill fast, survive by aggression, suppress AI so enemies don't get smart. The party fights DUMBER enemies.
- Adafold's approach: Physically control space. Enemies can't GO where you don't want them. The party fights CONTAINED enemies.
- Elementalist's approach: Adapt to whatever the environment demands (element-reactive). The party has a FLEXIBLE answer.

### The Downstream Effect (Why This Ordering Matters)

Because Shaman handles "make enemies manageable," melee DPS doesn't NEED that utility:

> **Example — Pyrien Ninja:** Shaman is already debuffing enemy accuracy and slowing their movement. So the Ninja can focus purely on: approach, burst, retreat. It doesn't need survivability tools or CC — someone else solved that. Copy DFO's Kunoichi: spam-cast, rapid repositioning, pure aggression.

> **Example — Pyrien Samurai:** Shaman has enemies slowed and accuracy-debuffed. Samurai applies flame sword DoTs, then lands powerful explosions (detonation). Doesn't need utility — the ROLE that provides utility EXISTS, so this role doesn't duplicate it.

**The rule:** If Role A replaces a strategic consumable (Shaman replaces Smokescreen/Paralysis), then Role B (melee DPS) is FREE to specialize purely in damage/execution because Role A already solved the approach problem.

### Monetization Model — "It's There" (League Model)

Gacha exists. It is NOT the forefront. The game was never "always modest" — it's competitive and has depth. But:

| Player Type | Experience | Ceiling | Optimization Depth |
| --- | --- | --- | --- |
| **Budget player** | WORKS to get there. Grinds real challenges. Finds patterns of success without paying. | Lower raw DPS ceiling | DEEP — mastery IS the reward. Low-tier optimization as a real counter to whales. |
| **Gacha player** | Higher raw numbers. Simpler optimization path. Not going through rapid improvement until the game pushes them (WW Holograms model). | Higher DPS ceiling | SHALLOW initially — game eventually demands engagement |

**The satisfaction:** A budget player who optimizes deeply can make fools of whales who assume money = dominance. This has been done, it feels good when executed correctly.

**The caveat:** Gacha characters need genuinely higher DPS ceilings with relatively simple optimization. The whale isn't grinding — they're buying access to a higher FLOOR. But the budget player's CEILING (through mastery) can approach or match the whale's floor. The gap exists but is closeable through skill.

### Current Class Status (Reframed as Strategic Role)

| Class | Strategic Role (what it SHOULD do) | Kit Status | Needs |
| --- | --- | --- | --- |
| Shaman | Make enemies less dangerous. Debuff accuracy, slow, paralyze, delegate damage to summons/DoTs. Nuisance to enemies. Healer-capable. Replaces: Smokescreen, Paralysis Bomb, Potions. | ✅ YAML exists | Reframe around "replaces X consumable permanently" |
| Adafold | Physically contain enemies. Force Targeting = collision-based control. Replaces: Barricade items, decoys. | ✅ YAML exists | Validate vs spatial primitives |
| Madolt Warrior | Suppress enemy intelligence + deal damage. Unfocus = make enemies dumber. Replaces: Flash/distraction items. | ✅ YAML exists | Validate Capacitor Pull vs room geometry |
| Elementalist | Flexible response to environment. Element-reactive healing/DPS hybrid. Replaces: Potions, elemental coatings, AoE consumables. | ✅ YAML exists | Needs Layer 1 spatial data to stop Fire-degenerating |

### Scout's Rangda as Reference (Shaman Adjacent)

Rangda from Tree of Savior's Scout tree: "Featherfoot but not Featherfoot." A debuffer that exists to make the party's life easier through enemy degradation. Shaman can draw from this:
- Accuracy reduction (like Smokescreen but permanent while in aura)
- Speed reduction (slows enemies chasing allies)
- Attack speed reduction (fewer enemy actions per window)
- Action nullification (paralysis — Pokémon-esque: chance to skip turn)
- Damage delegation (summons and DoTs do the work while Shaman maintains debuffs)

Many places to increase class potential while still functioning as a healer — but it exists to REPLACE choices that other classes would otherwise need consumables for.

### Race → Class System

**Philosophy:** ToS-scale class count. Races are the VARIABLE NAMESPACE — same class archetype can exist across races with different execution specialties. Race lock doesn't mean "only one class per race." It means "this race's VERSION of this archetype." Fewer variable names needed; rename later if necessary. Templates in juice-yaml-library already reflect this modular approach.

#### MAGICCAPACITY Exclusion Rule

| Threshold | Access | Reasoning |
| --- | --- | --- |
| MAGICCAP < 10 | **BANNED** from traditional caster classes | Body can't hold enough magic to sustain repeated casting under mana model |
| MAGICCAP 10-12 | **Conditional** — needs lore justification OR external magic source (Noms' gem-craft) | Borderline sustain, class must account for it |
| MAGICCAP 13+ | **Unrestricted** caster access | Full mana model functions as designed |

#### Confirmed Race Locks

| Race | Class | Lock Type | Tier | Notes |
| --- | --- | --- | --- | --- |
| Rawrotin (Linfree) | Adafold | Hard | Base Available | Bodyguard → Force Targeting |
| Madolt (Landwin) | Warrior | Hard | Base Available | Precision engineer → Tech weapons, Parry, Capacitor |
| Soue (Wanderers) | Shaman | Hard (player-only) | Experienced | Isolative magic tradition → Bone/spirit |
| **Tryll (Landwin)** | **Elementalist** | Hard | Base Available | Academic tradition → all-element study. **⚠️ Potency adjustment mandatory** — STR 6/STAM 6 will skew initial test numbers before equipment normalization. Post-rework required. |
| Pyrien (Wanderers) | Ninja | Hard | Experienced | DFO Kunoichi trace. Fire chain DETONATOR. Ring of Fire = originating area gate. |
| Pyrien (Wanderers) | Samurai | Hard | Experienced | Flame sword DoTs → explosions. Fire chain PRIMER + DETONATOR. |

#### Exclusion Matrix (MAGICCAP-based Bans)

| Race | MAGICCAP | Banned From |
| --- | --- | --- |
| Wyrpincers | 6 | ALL caster classes |
| Rawrotin | 8 | ALL traditional caster classes |
| Nyanto | 8 | ALL traditional caster classes |
| Grimm | 8 | ALL traditional caster classes |
| Chunkers | 8 | ALL traditional caster classes |
| Triclaw | 8 | ALL traditional caster classes |
| Madolt | 10 | Traditional casters (tech-based magic OK — Machinist) |
| Featherin | 10 | Conditional (dodge-aura magic ≠ sustained casting — class-specific eval needed) |
| Noms | 12 | Conditional (gem-craft = external source, not self-cast — Summoner-type OK) |

#### Unassigned / Open Questions

| Class | Tier | Likely Race | Reasoning | Status |
| --- | --- | --- | --- | --- |
| Rogue | Base Available | Nyanto? Mantidia? | Agility-based, wall-climb (Nyanto) or razor-arms stealth (Mantidia) | 🟡 Open |
| Archer | Base Available | Featherin? Soue? | Aerial advantage (Featherin) or forest stealth/hearing (Soue, non-Shaman) | 🟡 Open |
| Body Specialist | Base Available | — | Unknown identity | 🔴 Undesigned |
| Lancer | Experienced | — | Was "Adafold upgrade" → now sideways | 🟡 Open |
| Dancer | Experienced | — | — | 🔴 Undesigned |
| Nightmare | Experienced | — | — | 🔴 Undesigned |
| Machinist | Experienced | Madolt? | Tech-race → tech-class, MAGICCAP 10 = external/tech magic | 🟡 Strong fit |
| Summoner | Experienced | Noms? HBD? | Gem-craft summons (Noms) or dragonic pacts (HBD) | 🟡 Open |
| Samurai | Experienced | Pyrien | Confirmed — fire sword | ✅ |
| Ninja | Experienced | Pyrien | Confirmed — DFO Kunoichi | ✅ |
| Magiknight / Fencer | Experienced | — | — | 🔴 Undesigned |
| Monster Eater / Specialist | Experienced | — | — | 🔴 Undesigned |
| Dracomancer | Special | HBD? | Closest to dragons, morphing, MAGICCAP 18 | 🟡 Strong fit |
| Tribalist | Special | — | — | 🔴 Undesigned |
| Magical Girl | Special | — | — | 🔴 Undesigned |
| Calvary | Special | — | — | 🔴 Undesigned |
| Beast Master | Special | — | — | 🔴 Undesigned |

### Lore → Economy Pipeline

Races are the IN-WORLD SOURCE of the consumable/equipment economy:

| Race | Economic Role | Produces | Connection to Player |
| --- | --- | --- | --- |
| **Noms** (Noct Aurorus) | Consumable manufacturers | Gem-craft "spells in a can" — the debuff/CC items in the catalog | Nom NPCs sell items. Player Noms get crafting bonus (budget optimization). |
| **Grimm** (Landwin) | Blacksmiths/weaponsmiths | Weapons, armor, equipment | Equipment economy backbone. |
| **Harvesters** (Linfree) | Raw material gatherers | Minerals, herbs, monster drops → crafting ingredients | 3 phenotypes (Builders, Flutters, Nightflies) = material specialization. |
| **Redels** (Landwin) | General labor / scavenging | Cheap bulk materials, salvage | Highest GATHER (9) = quantity over quality. Budget material source. |
| **Madolt** (Landwin) | Engineers / defense systems | Tech items, machines, infrastructure | High-end tech consumables (Shield Generators, Capacitor tech). |
| **Merryin** (Depth Dead) | — | Lightning/water magic items? Siren-based CC? | 🟡 Unexplored |

**Principle:** The item catalog we designed (60 debuff/CC items) should map to Nom gem-craft as the primary manufacturing source. Item NAMES should reflect mineral/gem/crystalline origins where possible. This connects lore → economy → gameplay seamlessly.

### Pyrien Fire Classes (Chain Reaction Specialists)

Both Experienced tier. Both gated behind Ring of Fire (originating area) + Mercenary Rank 2.

| Class | Trace | Chain Role | Identity |
| --- | --- | --- | --- |
| **Pyrien Ninja** | DFO Kunoichi | DETONATOR | Spam-cast, rapid reposition, approach/burst/retreat. Triggers combustible debuffs/terrain laid by others. Doesn't need utility — Shaman/items solve approach. |
| **Pyrien Samurai** | — | PRIMER + DETONATOR | Flame sword DoTs (primes targets with fire debuff), then lands explosions (self-detonates). Can also be detonated by ally Ninja or environmental fire sources. |

**Design note:** These classes don't need utility ON THEIR OWN because the Layer 1 strategy baseline (items) + Shaman (premium debuffer) already solves the "approach problem." Pyrien DPS is pure execution within a pre-solved strategic environment.

---

## Layer 3: CHAIN REACTIONS (Synergy)

### Principle

With oil comes fire. Cross-class and class+item interactions create the MULTIPLAYER JUICE.

| Interaction Type | Example | Design Function |
| --- | --- | --- |
| Element + Element | Oil terrain + Pyrien fire attack = explosion/ignite | Rewards coordination, comp diversity |
| Debuff + Detonation | Shaman curse + Samurai explosion trigger | Cross-class burst windows (emergent, not scripted) |
| Terrain + Class | Environmental trap + Force Targeting push = enemy into trap | Spatial awareness rewarded |
| Item + Class | Elemental coating + Elementalist convergence = enhanced reaction | Preparation rewarded |
| Summon + Environment | Bone Spirit positioned near explosive barrel = chain detonation | Tactical deployment rewarded |

### Design Rules

- Chain reactions must be DISCOVERABLE, not mandatory. Players who find them gain advantage. Players who don't can still clear.
- Traps around the level have meaning IF you can get a chain reaction — otherwise they're a simple stun/explosion (still useful, but not exciting).
- Gacha characters may have UNIQUE detonation triggers that budget characters access via items (e.g., Pyrien Samurai detonates fire debuffs inherently; budget Samurai uses an Ignition Powder consumable to do the same thing at lower efficiency).
- Chain reactions are the answer to "why bring THIS comp?" without making specific comps mandatory.

---

## Layer 4: SKILL PROGRESSION (Pacing)

### Principle

Locked skills. Weak initial designs. The early game gives a TASTE of power at generous intervals (20s CD skill that handles regular AI). The late game puts that same skill on 180s CD because the difficulty floor is completely different — it's not gone, but it's not going to shine due to lack of opportunity.

| Progression Stage | Skill Availability | Difficulty Context | Player Experience |
| --- | --- | --- | --- |
| Early (taste) | Key skill at 20s CD, generous | SR1 — enemies punish only with numbers | "This skill is COOL, I want to use it more" |
| Mid (learning) | Same skill at 45-60s CD | SR2 — enemies punish positioning mistakes | "I need to CHOOSE when to use this" |
| Late (mastery) | Same skill at 120-180s CD | SR3-4 — enemies exploit every gap | "This skill SAVES me when nothing else can" |

### Design Rules

- Early skills must be FLASHY — they sell the class fantasy and create aspiration
- The CD increase isn't punishment — it's the difficulty demanding you use OTHER tools between uses
- Budget players experience this grind as the JOURNEY (and it should feel good, not just grinding)
- Gacha characters may have passives that reduce CDs or enhance base skills — higher floor, not different game

---

## Layer 5: LOOT / REWARDS (Enhancement)

### Principle

Only matters if the gameplay loop is satisfying. Being a boring game before you have what makes it fun is weak design — yet many games get away with it due to "I found this drop!!" basis.

**Our position:** Adjacent to drop-excitement, not completely parallel. Loot ENHANCES an already-fun game. It does not MAKE the game fun.

- Loot should feel good to find
- Loot should create build diversity (not just stat increases)
- Loot should NOT be required for SR1-2 content to feel satisfying
- Loot SHOULD enable SR3-4 strategies that are impossible without specific gear/items

---

## The Desync (Why We Were Stuck)

We built Layer 2 (class kits) before fully defining Layer 1 (strategy). The classes know what they CAN do but not what they SHOULD do, because:

1. **Enemy AI's full range isn't defined** — Shaman's "mappable" abilities don't have a clear SHOULD until strategy is.
2. **Consumables as baseline weren't established** — classes were designed in isolation rather than as "premium replacements for universal tools."
3. **Spatial quantitative layer is missing** — can't validate position axis without room geometry.
4. **Time axis partially defined** (GCD, gauge) but missing key variables (consumable duration, enemy commitment timers, kill thresholds).

**This is not failure.** The class kits are good IDEAS. They now need to be NARROWED by the strategic foundation above them. What Shaman CAN do is broad. What Shaman SHOULD do (given Layer 1) is: "be a nuisance to enemies — decrease accuracy, slow chasers, lower attack speed, defer personal damage to installations." That's narrower. That's design intent.

---

## Design Override Principles (Authoritative)

1. NO 2-minute burst cycle. No fixed burst cadence. Classes justified by USE CASE.
2. Strategy (Position × Action × Time) defines the game BEFORE classes do.
3. Consumables/items define the BASELINE. Classes are premium replacements with better uptime.
4. Procgen maps = party splits. Branching paths force separation.
5. Tanks operate solo. Self-sustaining without healer.
6. Two tank identities: Adafold (Force Targeting, facetank) / Madolt (Unfocus suppression, damage-first).
7. Enmity = spatial/tactical. NO enmity table. Strategy Rank controls AI targeting.
8. Unfocus = AI suppression. Reduces enemy Strategy Rank.
9. Healers = DPS until not. Traditional healer only at high SR content.
10. DPS = different games. Each class is a fundamentally different input experience.
11. Shaman summons = persistent. Decent HP, deployable assets. Hold corridors.
12. >50% HP rule: ENEMIES take +25% damage above 50% HP. Not players taking incoming.
13. Anti-cheese for ranged: enemy movement + shot arc. Long-range = CC only, not damage farming.
14. **Shaman is SLOW.** Attrition/denial caster, not assassin. Makes enemies LESS DANGEROUS.
15. **Budget player mastery can match whale floor.** Gacha = higher ceiling with simpler path, not exclusive power.
16. **Resource gating encourages planning.** Prevents permanent forward push. Dead time = decision time, not punishment.
17. **Map variance is the highest-variance strategic element.** Must be simple enough to read, complex enough to matter.
18. **Classes REPLACE consumable effects** — they don't invent unique capabilities that have no item equivalent.
19. **Elementalist → Tryll.** Academic tradition learns all elements through study. Potency adjustment required for STR 6/STAM 6 base.
20. **MAGICCAP < 10 = banned from caster classes.** Physical races can't sustain the mana model.
21. **ToS-scale class count.** Races are namespaces. Same archetype across races = different execution specialties.
22. **Lore = economy.** Noms craft consumables, Grimm forge weapons, Harvesters gather materials. Item catalog maps to racial manufacturing.
23. **Enemy action selection: "last used" removed from list.** No traditional cooldowns. SR-dependent, per-enemy. Postponed until enemy designs exist.
24. **Crit is NOT RNG.** Requires backstab, flank, or CC exploit (positional/conditional). System-wide rule.
25. **Three axes of enemy impairment:** Unfocus (reduce SR), Smokescreen/accuracy debuffs (reduce hit rate), Darkness (reduce vision distance). Distinct, stackable.
26. **NTU-based damage exists.** Warrior uses reaction speed (NTU), not STR, as damage basis. Fixed + percent design for ranged EC shots.
27. **Defense ignore % for low-stat variants.** Body Specialist (and similar) use defense penetration so low-stat racial versions remain viable.
28. **Racial versions of same class = different execution.** Same archetype name, different kit emphasis per race. Not just reskins.
29. **Three classes BLOCKED on creature catalog:** Summoner, Beast Master, Calvary. Cannot design until enemy/beast designs exist.

30. **Healer triage system** — ratio-based DPS/Heal shift triggered by party HP thresholds, not manual stance toggle.
31. **Items define baseline, classes REPLACE** — if no consumable does it, no class should either.
32. **No Freecure. No "let them drop." Urgency rewards.**
33. **Resupply Pods / terrain interaction** — procgen rooms have gatherable resources that create pacing decisions.

---

## Methodology (The Cycle)

```
Qualitative₀ — Vision: "co-op RPG where classes feel fundamentally different"
    ↓
Quantitative₁ — BalanceTargets.yaml, class YAML specs (potency, GCD, gauges)
    ↓
Qualitative₁ — Simulate → "Elementalist is linear," "consumables are missing,"
               "strategy must precede class design"
    ↓
Qualitative₁b — [NOW] Hierarchy reframe. Strategy > Character > Synergy > 
                Progression > Loot. Classes are implementations, not specs.
    ↓
Quantitative₀ — [NEXT] Define Layer 1 fully: spatial primitives + consumable
                baselines + enemy behavior ranges + time variables
    ↓
Quantitative₂ — Re-derive class SHOULD from Layer 1 numbers. Narrow kits.
    ↓
Qualitative₂ — Validate or identify next gap
    ↓ ...repeat
```

**We are HERE:** Qualitative₁b. The hierarchy is established. Next step is Quantitative₀ — define the strategic foundation with real numbers so classes can be narrowed from CAN to SHOULD.

---

## Open Questions (Honest Gaps)

| # | Question | Layer | Urgency |
| --- | --- | --- | --- |
| 1 | Consumable economy (7 sub-questions) | L1 Strategy | 🔴 Blocking |
| 2 | Level design primitives (10 variables) | L1 Strategy | 🔴 Blocking |
| 3 | Enemy behavior full range (what CAN enemies do before classes exist?) | L1 Strategy | 🔴 Blocking |
| 4 | Kill thresholds by SR tier | L1 Strategy | 🔴 Blocking |
| 5 | What's the gacha ceiling vs budget ceiling delta? | L2 Character | 🟡 Qualitative answer exists, no numbers |
| 6 | Chain reaction catalog (what elements interact?) | L3 Synergy | 🟡 Examples exist, no system |
| 7 | Skill CD scaling curve across progression | L4 Progression | 🟡 Concept exists, no numbers |
| 8 | Loot impact on build diversity | L5 Loot | ⚪ Not yet relevant |
| 9 | Mercenary Rank / Tester Golem overlap | Meta | 🟡 Parked |
| 10 | Procgen room tagging (which engagement model?) | L1 Strategy | 🟡 Concept only |
| 11 | Creature/beast catalog (blocks Summoner, Beast Master, Calvary) | L1/L2 | 🔴 Blocking 3 classes |
| 12 | Crit system formalization (positional/conditional, NOT RNG) | L2 Character | 🟡 Rule established, no numbers |
| 13 | Darkness debuff specification (vision distance reduction vs Unfocus vs accuracy) | L2 Character | 🟡 Concept from Nightmare, needs quantification |
| 14 | Race → Class coverage gap (22 races, many unrepresented — Merryin, Lower Drakols, Harvesters) | L2 Character | 🟡 Expected, not urgent |
| 15 | Defense ignore % system (Body Specialist + low-stat variants) | L2 Character | 🟡 Concept exists, no formula |

---

## Next Actions (Priority Order)

| # | Action | Layer | Unblocks |
| --- | --- | --- | --- |
| 1 | Define enemy behavior range (what can enemies DO, stratified by SR) | L1 | Class SHOULD, consumable baseline, spatial requirements |
| 2 | Define consumable/item baseline (what's universally achievable) | L1 | Class identity as "premium replacement" |
| 3 | Define spatial primitives (room geometry, movement, distances) | L1 | Position axis validation, Elementalist rescue |
| 4 | Narrow class kits from CAN → SHOULD using Layer 1 answers | L2 | Kit validation, removes degenerate options |
| 5 | Define chain reaction system (what interacts with what) | L3 | Comp diversity, multiplayer juice |
| 6 | Define skill progression curves | L4 | Player pacing, gacha ceiling tuning |
| 7 | Design Archer / Pyrien classes (AFTER Layer 1 is solid) | L2 | New classes that derive from strategy, not imagination |

---

## Notes to Self

- **Strategy defines the problem. Classes are solutions.** Not the other way around.
- **Items/consumables are the BASELINE.** Classes are premium access to those same effects. If no item does it, no class should either (with rare exceptions for class-defining fantasy moves).
- **The three axes (Position × Action × Time) ARE the game.** Everything else is implementation detail.
- **We were designing solutions before fully defining the problem.** The class YAMLs are good ideas that need NARROWING, not scrapping.
- **Melee enemy dominance is rejected.** Ranged/complex threats define the strategic space. Melee becomes intuitive BECAUSE strategy already solved "how do I approach?"
- **Budget optimization beating whales is a CORE FANTASY of this game's identity.** Not a side benefit — a design pillar.
- **DRG retains without content because its moment-to-moment loop has RNG IN THE ENVIRONMENT.** Your procgen must deliver the same: every room asks different questions.
- **SR1 is intentionally easy.** Balance around SR2-3. SR1 exists so new players feel competent.
- **Dead time is decision time, not punishment.** The ToS budget player experience but reframed as CHOICE.
- **"A business bows before their consumers rather than scorning them."** — The game respects player TIME. No timegating, no mandatory daily chores, no FOMO mechanics.
- **Don't design more classes until Layer 1 is quantified.** New classes derived from strategy will be NARROWER and more purposeful than classes designed from imagination alone.
- **Qual context pass done (21 classes).** 4 complete YAMLs, 2 discussed, 12 with qual context, 3 blocked on creature catalog. See artifacts/class_list_qual_context.md.
- **Heavy frontline (7 classes).** Tracks with "procgen splits party = every path needs a frontliner." Not a balance problem — intentional.
- **Crit = positional, not RNG.** This changes BalanceTargets.yaml — remove any crit-rate assumptions. Crit is a REWARD for positioning/timing, not a stat.
- **Darkness (Nightmare) is a THIRD impairment axis.** Unfocus = make dumber. Accuracy debuff = make miss. Darkness = make blind (reduce detection/targeting range). All three stack but solve different problems.
- **Racial versions exist per class.** Warrior (Madolt) uses NTU. Another race's Warrior would use STR or DEX differently. Same class name, different execution. Templates support this already.
- **22 races vs 21 classes.** Gap is expected. Depth Dead races (Merryin, Iblis Grabbers, etc.) likely become enemy types FIRST and player races later. Harvesters may never get a combat class (economy role instead).
- **Class qual context reveals: "approach problem" is solved by support roles (Shaman, items), so melee DPS is FREED to be pure execution.** This is the Layer 1 → Layer 2 cascade working as designed.
