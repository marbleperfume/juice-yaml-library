# DESIGN_OVERRIDE_HEALER.md
# ═══════════════════════════════════════════════════════════════════════════════
# HEALER DESIGN PRINCIPLES & TAXONOMY
# ═══════════════════════════════════════════════════════════════════════════════
#
# Authority: This file > individual Healer class Design files > LLM.md
# References: DESIGN_OVERRIDE.md, DESIGN_OVERRIDE_RACIAL_LOCKS.md,
#             CombatSim/Wavecaller_Duo_Scenario.md, CombatSim/Skyreign_R3_Displacement.md
# Last updated: 2026-07-16
# ═══════════════════════════════════════════════════════════════════════════════

## Core Principle

> Healers are DPS players whose healing is efficient enough to not compete
> with their damage output. The kit must FUNCTION — identity follows mechanics.

---

## Three-Axis GCD Model

Every healer allocates GCDs across three axes:

| Axis | Purpose | What scales it |
|------|---------|----------------|
| **Damage** | Kill enemies (primary activity) | Filler potency, burst, combos |
| **Healing** | Keep frontliner alive | GCD heals (when free HPS insufficient) |
| **Utility** | Shape combat (CC, debuffs, positioning) | Enemy complexity (rank) |

### Rank Scaling (validated via simulation)

| Rank | Damage | Healing | Utility | Why |
|------|--------|---------|---------|-----|
| R1 | ~80% | ~15% | ~5% | Enemies are simple. Hit them. |
| R2 | ~70% | ~15% | ~15% | Enemies have behaviors. Some need CC/debuffs. |
| R3 | ~55% | ~15% | ~30% | Enemies REQUIRE management. Each demands a response. |

**Key insight:** Healing stays CONSTANT across ranks (~15%). Damage drops because
UTILITY demands grow. R3 healers do less damage not because they heal more, but
because they CONTROL more.

---

## Free Healing Baseline (Mandatory)

Every healer MUST have passive healing that costs zero GCDs. Without this,
the healer cannot deal damage (100% of GCDs consumed by healing).

**Target:** Free HPS should cover 75-80% of standard incoming damage.
Remaining 20-25% handled by occasional GCD heals.

**Validation:** FFXIV healers handle ~90% of healing via oGCDs.
ToS Priest handles ~70% via Heal:Linger regen + Healing Factor passive.
Both allow majority damage GCD allocation.

**Anti-pattern:** If free_hps = 0, healer allocates 90%+ GCDs to healing.
This produces a heal-bot, NOT a DPS-first healer. Files claiming "aggressive
healer" identity MUST define mechanical free HPS sources.

---

## Survival Clock (Healer Under Pressure)

Healers cannot survive tank-buster equivalents (insufficient eHP).
Healers CAN stall sustained pressure (rushers/adds) for a limited time.

**Target survival clock:** 10-15 seconds vs sustained pressure (3 dedicated enemies).
- Long enough for ANY frontliner class to notice + react + reposition
- Short enough that healer genuinely dies without help

**Formula:**
```
survival_clock = healer_hp / (effective_incoming - self_sustain) + cc_bonus + escape_bonus
```

**Tools that extend the clock (budget from):**
- Passive self-sustain (Sound redirect, HoT, leech) — adds base seconds
- CC (Stage 1-2 on enemies) — adds stun/interrupt duration
- Escape (blink, threat drop) — adds ~2-3s per use
- Slow on enemies (Tidepool equivalent) — reduces effective incoming

**Anti-pattern:** survival_clock = 0 (no tools). Healer dies instantly without
specific frontliner composition (Adabold). Kit is composition-locked.

**Anti-pattern:** survival_clock = ∞ (unkillable). Healer solos content.
No reason for frontliner to exist.

---

## Self-Healing Rules

Healers MAY self-heal under the following constraints:

1. **Self-heal MUST have a cost** — reduced ally healing, GCD loss, or resource drain
2. **Self-heal potency MUST be lower than ally-heal** — 50% is the baseline
3. **Self-heal MUST NOT make the healer unkillable** — it extends the clock, doesn't eliminate it
4. **Self-heal is a CHOICE** — "I survive but my team heals less for the next Xs"

This produces the correct tension: self-heal is AVAILABLE but COSTLY. The healer
can stall but degrades team performance while doing so. Frontliner arriving ends
the degradation — the team incentive to peel for the healer is mechanical, not just
"healer dies and we wipe."

---

## CC Budget (Healer Role)

Healers are NOT CC-heavy. Power budget: healing + damage + mobility. CC is limited.

| Stage | Healer Access | Notes |
|-------|---------------|-------|
| Stage 1 | YES — passive/environmental (Tidepool slow, terrain effects) | Low cost, always active in zone |
| Stage 2 | YES — active oGCD (interrupts, short silences) | Fast CD, single-target, reactive |
| Stage 3 | NO — healers do not hard-disable | Zero stun/paralyze/sleep access |

**Design reasoning:** If healers had Stage 3 CC, they could self-peel indefinitely
(stun → heal → stun → heal). The 10-15s clock relies on CC being Stage 1-2 ONLY.

---

## Utility Axis (Where Variety Comes From)

The utility axis is what makes healer gameplay VARIED across ranks and encounters.
Utility GCDs are NOT healing and NOT damage — they are COMBAT SHAPING.

Examples of utility actions (class-specific, not universal):
- Debuff enemy (damage amp for team, accuracy reduction)
- Exploit condition application (environmental, positional)
- Displacement (knock enemies into/out of positions)
- Terrain creation (Tidepool, healing zones, denial zones)
- Cleanse/dispel (remove enemy buffs, clear ally debuffs)
- Speed/movement manipulation (ally sprint, enemy slow)

**Key:** Each utility GCD is a DIFFERENT DECISION based on enemy state.
This is the opposite of FFXIV (where healers have ~0 utility GCDs and
spam one damage button 80% of the time). Variety scales with rank because
enemy COMPLEXITY scales — more behaviors to respond to.

---

## Healer Damage Kit (NOT Monotone)

**Anti-pattern (FFXIV):** Single-button spam filler (Glare ×90% of fight).
Mathematically optimal but experientially boring. Player feedback: "green DPS."

**Goal:** Healer damage has engagement without requiring rotation mastery.
The variety comes from ENEMY INTERACTION, not from internal button sequences.

Damage kit should include:
- Filler (ranged, reliable, low thought) — ~50% of damage GCDs
- Reactive (responds to enemy state, Exploit conditions) — ~30%
- Burst/payoff (charges via healing, releases for AoE/nuke) — ~20%

The reactive + payoff components mean the healer's damage CHANGES based on
what's happening in combat, not based on a memorized rotation.

---

## Payoff System (Lily Equivalent)

GCD heals should NOT be pure damage loss. Healing under pressure must
BUILD TOWARD a payoff.

**FFXIV WHM model:** 3 lily heals → 1 Afflatus Misery (1320p AoE nuke).
Net result: 3 Glares lost (930p) vs 1 Misery gained (1320p) = DPS POSITIVE.
Players WANT to heal because it charges a weapon.

**Principle for this game:** N consecutive GCD heals → 1 burst/utility payoff.
The payoff should ALSO apply an Exploit condition or CC effect, making it
serve the utility axis simultaneously.

This converts "I'm losing DPS to heal" into "I'm charging my burst."

---

## Reference Comparison (Validated via Simulation)

| System | Damage% | Heal% | Utility% | Free HPS | Self-Peel | Feel |
|--------|---------|-------|----------|----------|-----------|------|
| FFXIV WHM | 92% | 8% | 0% | Very high (oGCDs) | Holy stun + self-heal + sprint | Glare spam (boring) |
| ToS Priest | 88% | 12% | 0% | Low (Linger HoT) | Fade (free threat drop) + self-heal | Heal→Filler rhythm |
| Juice Healer (target) | 70-80% | 15% | 10-20% | Moderate (covers 75-80%) | Stage 1-2 CC + limited self-heal + escape | Enemy-reactive variety |

---

## Healer Contract (Universal — all healer classes)

> **Frontliner and DPS must never worry about dying to sustained damage
> while the healer is alive and in range.**
>
> The healer's FREE HEALING handles routine incoming. GCD heals handle spikes.
> Utility shapes combat so that damage never exceeds the healing ceiling.
> If damage DOES exceed the ceiling, it's because the frontliner played wrong
> (pulled too many, didn't scatter, ignored positioning) — NOT because the healer
> failed to press buttons fast enough.

---

## Healer Subcategories (Discovery — In Progress)

Mechanical behaviors a healer can express:

| Subcategory | Definition | Example |
|-------------|------------|---------|
| **Aggressive** | Deals damage as primary; heals passively/cheaply | Wavecaller (dive damage + sound healing) |
| **Reactive** | Responds to incoming spikes; strong burst healing | (TBD — possibly Spiritcaller proximity-based) |
| **Proactive** | Prevents damage before it happens; shields/DR | (TBD) |
| **Zone** | Heals via positioned areas; party fights near healer | (TBD — possibly Diev-like statue concept) |
| **Hybrid** | Splits between two of the above based on form/state | (TBD) |

Status: These are STARTING POINTS. Need the same discovery treatment frontliners got.

---

## Supersedes

- Healer section of DESIGN_OVERRIDE_OTHER_ROLES.md (removed — now DPS only)
- All "heal OR damage" false-choice framing in class Design files
- All class files claiming "aggressive healer" without defining free HPS sources
- OverFiftyRule (already superseded — confirmed removed)

---

## Simulation Tools

Template function `simulate_healer_combat()` validates kit functionality:
- Plug in class stats → outputs GCD split + survival clock + verdict
- Run across R1/R2/R3 to verify scaling behavior
- Compare against WHM/ToS baselines

See: `CombatSim/Wavecaller_Duo_Scenario.md`, `CombatSim/Skyreign_R3_Displacement.md`
