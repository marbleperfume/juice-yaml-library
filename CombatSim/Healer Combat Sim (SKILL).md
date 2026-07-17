---
name: healer-combat-sim
display_name: Healer Combat Sim
description: "Run three-axis healer combat simulations (Damage/Healing/Utility GCD split) for juice-yaml-library classes. Activate when user says 'healer sim', 'simulate healer', 'run healer through template', 'test healing cadence', 'three axis', 'wavecaller check', 'does this healer kit work', or any request to validate healer GCD allocation, survival clock, or rank scaling."
icon: "⚔️"
trigger: healer sim simulate healer combat test three axis healer healing cadence run healer template wavecaller healing check survival clock
inputs:
  - name: healer_class
    description: "Which healer class to simulate (e.g., Wavecaller, Spiritcaller, Siren)"
    type: string
    required: true
  - name: frontliner_class
    description: "Which frontliner is paired in the duo (e.g., Skyreign, Adabold, MetaKnight)"
    type: string
    required: false
    default: "Adabold"
  - name: rank
    description: "Difficulty rank (1, 2, or 3). Scales enemy stats × rank multiplier."
    type: number
    required: false
    default: 1
  - name: encounter
    description: "Encounter shape description. Defaults to 13-enemy multi-elevation map if not specified."
    type: string
    required: false
    default: "standard_13_enemy"
tools: [run_python, file_read, file_write, open_in_session_tab, web_search, url_fetch]
scripts: [healer_sim_engine.py]
---

## Overview

Validates whether a healer class's kit FUNCTIONS by running it through the three-axis
GCD allocation model (Damage / Healing / Utility). Outputs survival clock, GCD split
percentages, rank scaling behavior, and comparison against FFXIV WHM and ToS Priest
baselines. Catches design conflicts where a file's stated identity doesn't match its
mechanical output.

## Workflow

### Step 1: Load Healer Data
- **Mode**: `agentic`
- **Tool**: `file_read` or `url_fetch`
- **Input**: `{{healer_class}}` — find the Design yaml (local backup or GitHub raw)
- **Output**: Extracted parameters: HP, GCD, free HPS, GCD heal amount, CC stage/CD, escape tools, self-heal, slow, utility actions
- **Validate**: All required params have numeric values
- **On failure**: If file not found locally, fetch from `https://raw.githubusercontent.com/marbleperfume/juice-yaml-library/main/Classes/2.0/{class}_Design.yaml`

Extract these params from the yaml:
- `healer_hp`: STA × 100
- `gcd`: base GCD (from file) adjusted by SPD racial
- `free_hps_allies`: sum of passive healing tools (auras, oGCD pulses, HoTs)
- `free_hps_self`: any self-sustain defined
- `gcd_heal_amount`: potency of GCD heal (average across Resonance states if applicable)
- `cc_stage`: highest CC stage available
- `cc_cd`: cooldown of primary CC tool
- `cc_is_ogcd`: whether CC costs a GCD
- `escape_cd`: escape tool cooldown
- `slow_on_enemies`: % slow applied to enemies
- `utility_actions`: estimated utility GCDs per phase (based on kit)

### Step 2: Load Frontliner Profile
- **Mode**: `agentic`
- **Input**: `{{frontliner_class}}`
- **Output**: frontliner HP, DR, peel capability (can they protect healer?)
- **Validate**: HP and DR values present
- **On failure**: Use defaults (HP=1600, DR=30%, peel=True for Adabold)

Key frontliner parameters:
- `tank_hp`: STA × 100
- `tank_dr`: passive DR (armor, shields, exoskeleton)
- `has_peel`: boolean — can this FL protect the healer? (Adabold=yes, Skyreign=no, MK=limited)
- `elevation_access`: boolean — can FL reach elevated enemies?

### Step 3: Define Encounter
- **Mode**: `agentic`
- **Input**: `{{encounter}}` (or default 13-enemy map)
- **Output**: Enemy counts, DPS values, positioning, healer-targeting enemies
- **Validate**: At least 1 enemy group defined with DPS value
- **On failure**: Use standard_13_enemy defaults

Standard encounter (default):
- 5 melee center (50 raw DPS each, ground)
- 2 bombers (40 raw DPS, elevated +5m, 60% hit rate)
- 3 archers (35 raw DPS, elevated +8m, far left)
- 3 rushers (50 raw DPS, 6.5 m/s, healer-targeting)

### Step 4: Run Simulation
- **Mode**: `deterministic`
- **Tool**: `run_python`
- **Input**: All params from Steps 1-3 + `{{rank}}`
- **Output**: Three-axis GCD allocation, survival clock, tank survival, verdict
- **Validate**: Verdict is one of: "FUNCTIONAL", "HEALER DIES", "TANK DIES", "BOTH DIE"
- **On failure**: Check that incoming_dps > 0 and healer_hp > 0

Run `simulate_healer_combat()` from the bundled engine at R1, R2, R3.
Also run reference comparisons (WHM, ToS Priest) at same incoming DPS for baseline.

### Step 5: Diagnose & Report
- **Mode**: `agentic`
- **Tool**: `file_write` + `open_in_session_tab`
- **Input**: Simulation results from Step 4
- **Output**: Formatted report with tables, verdicts, and design recommendations

Report format:
1. **Summary table** (all ranks, GCD splits, survival clocks, verdicts)
2. **Reference comparison** (vs WHM / ToS at same incoming)
3. **Diagnosis** (identify conflicts between file identity and mechanical output)
4. **Recommendations** (what needs to change for kit to function)

Open in session tab for user review.

### Step 6: Optional — Push to CombatSim/
- **Mode**: `agentic`
- **Tool**: `browser_navigate`, `browser_upload`, `browser_batch`
- **Input**: User confirmation to push
- **Output**: File in CombatSim/ folder on GitHub
- **Validate**: GitHub redirects to repo after commit
- **On failure**: Save local backup, retry push

Only push if user explicitly requests. Always save local backup first.

## Output

A markdown report containing:
- Three-axis GCD split per rank (Damage% / Heal% / Utility%)
- Survival clock (seconds healer survives under sustained pressure)
- Tank survival check (does frontliner live with this healing?)
- FFXIV WHM / ToS Priest baseline comparison
- Verdict: FUNCTIONAL or specific failure mode
- Design recommendations if kit doesn't function

## Lessons Learned

### Do
- Always check if free_hps = 0 in the yaml — this is the #1 failure indicator
- Run all three ranks even if user only asked for one — rank scaling reveals hidden issues
- Compare against WHM (GCD healer reference) not Sage/Scholar (oGCD dominant)
- Include the peeled scenario (no rushers) to show ideal-case performance
- Validate that stated identity matches mechanical output
- Use encoding="utf-8" when reading yaml files on Windows

### Don't
- Don't assume passive healing exists unless the file explicitly defines HPS sources
- Don't use potency numbers from one game system in another (normalize to HP/s)
- Don't skip the utility axis — it's what makes R3 different from R1
- Don't simulate all enemies simultaneously unless the encounter specifically clusters them
- Don't load full class files into context — extract only the parameters needed

### Common Failures
- `heal% > 100%`: Kit cannot function. Free HPS too low for incoming damage.
- `survival_clock < 8s`: Healer dies before any frontliner can react. Self-peel gap.
- `damage% = 0%`: Healer has no damage contribution. File says "aggressive" but mechanics say "heal bot."
- `utility% = 0% at R3`: Kit doesn't scale with rank. No combat-shaping tools.

### When to Ask the User
- If encounter shape is ambiguous (how many enemies target healer?)
- If the yaml doesn't specify key values (ask whether to estimate or flag as missing)
- If the healer class hasn't been updated to 2.0 yet (results will reflect outdated design)
- Before pushing to GitHub (always confirm)
