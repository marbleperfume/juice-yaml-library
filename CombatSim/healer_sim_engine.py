"""Three-axis healer combat simulation engine.

Validates healer kit functionality by computing GCD allocation across
Damage / Healing / Utility axes, survival clock under pressure, and
rank scaling behavior.

Reference: Guidebooks/DESIGN_OVERRIDE_HEALER.md
"""


def simulate_healer_combat(
    # Identity
    label="Healer",

    # Encounter
    duration_s=60,
    incoming_on_tank=150,
    incoming_on_healer=0,
    threat_tier="sustained",
    rank=1,

    # Healer stats
    healer_hp=800,
    healer_dr=0.0,
    gcd=1.8,

    # Free healing (Axis 0 - no GCD cost)
    free_hps_allies=120,
    free_hps_self=0,

    # Axis 1: Damage
    filler_potency=60,
    burst_potency=120,
    burst_cd=12,
    payoff_every_n=0,
    payoff_potency=0,

    # Axis 2: Healing (GCD)
    gcd_heal_amount=300,
    gcd_self_heal=0,
    self_heal_penalty=0,

    # Axis 3: Utility
    utility_actions=0,
    utility_type="none",
    utility_survival_bonus=0,
    cc_stage=0,
    cc_cd=0,
    cc_is_ogcd=False,

    # Self-peel tools
    escape_cd=0,
    escape_cost="none",
    slow_on_enemies=0,
):
    """Three-axis healer simulation: Damage / Healing / Utility.

    Returns GCD allocation, survival clock, and kit functionality assessment.

    Args:
        label: Display name for this configuration
        duration_s: Encounter phase duration in seconds
        incoming_on_tank: eDPS hitting the frontliner
        incoming_on_healer: eDPS hitting the healer (rushers etc)
        threat_tier: "chip", "sustained", or "buster"
        rank: 1, 2, or 3 (scales enemy stats)
        healer_hp: Healer max HP (STA * 100)
        healer_dr: Damage reduction % (0.0 to 1.0)
        gcd: GCD in seconds
        free_hps_allies: Passive healing on tank (no GCD cost)
        free_hps_self: Passive self-sustain
        filler_potency: Damage potency per filler GCD
        burst_potency: Burst damage potency per use
        burst_cd: Burst cooldown in seconds
        payoff_every_n: N GCD heals triggers 1 payoff (0=disabled)
        payoff_potency: Potency of payoff burst
        gcd_heal_amount: HP restored per GCD heal
        gcd_self_heal: HP restored per self-heal GCD (0=can't)
        self_heal_penalty: % ally heal potency lost during self-heal
        utility_actions: Number of GCDs allocated to utility per phase
        cc_stage: Highest CC stage available (0-3)
        cc_cd: CC ability cooldown in seconds
        cc_is_ogcd: If True, CC doesn't cost a GCD
        escape_cd: Escape tool cooldown (0=no escape)
        escape_cost: "free", "charge", or "gcd"
        slow_on_enemies: % slow on enemies near healer (0.0 to 1.0)

    Returns:
        dict with keys: label, rank, duration, total_gcds, pct_damage,
        pct_heal, pct_utility, pct_payoff, survival_clock,
        healer_survives, tank_survives, verdict, gcd_heals,
        utility_gcds, damage_gcds, potency_per_second, incoming_on_healer
    """
    # Rank scaling
    rank_mult = {1: 1.0, 2: 1.2, 3: 1.4}[rank]
    incoming_on_tank *= rank_mult
    incoming_on_healer *= rank_mult

    total_gcds = duration_s / gcd

    # === AXIS 2: Healing requirement ===
    tank_total_damage = incoming_on_tank * duration_s
    free_healing_total = free_hps_allies * duration_s
    healing_deficit = max(0, tank_total_damage - free_healing_total)
    gcd_heals_needed = healing_deficit / gcd_heal_amount if gcd_heal_amount > 0 else 0

    # === SURVIVAL CLOCK (healer under pressure) ===
    if incoming_on_healer > 0:
        effective_incoming = incoming_on_healer * (1 - healer_dr)
        if slow_on_enemies > 0:
            effective_incoming *= (1 - slow_on_enemies * 0.5)

        total_self_sustain = free_hps_self
        if gcd_self_heal > 0:
            self_heal_gcds_per_second = 0.3 / gcd
            total_self_sustain += self_heal_gcds_per_second * gcd_self_heal

        net_incoming = effective_incoming - total_self_sustain

        if net_incoming > 0:
            base_survival = healer_hp / net_incoming
        else:
            base_survival = float('inf')

        # CC extends survival
        if cc_stage >= 2 and cc_cd > 0:
            cc_uses = duration_s / cc_cd
            stun_time_per_use = [0, 0.5, 1.5, 2.5][min(cc_stage, 3)]
            cc_survival_bonus = cc_uses * stun_time_per_use
        else:
            cc_survival_bonus = 0

        # Escape tool
        escape_bonus = 0
        if escape_cd > 0:
            escape_uses = max(1, duration_s / escape_cd)
            escape_bonus = escape_uses * 2.5

        survival_clock = base_survival + cc_survival_bonus + escape_bonus
    else:
        survival_clock = float('inf')

    # === AXIS 3: Utility GCDs ===
    utility_gcds = utility_actions

    # === AXIS 1: Damage (remaining GCDs) ===
    payoff_procs = int(gcd_heals_needed / payoff_every_n) if payoff_every_n > 0 else 0
    payoff_gcds = payoff_procs

    damage_gcds = total_gcds - gcd_heals_needed - utility_gcds - payoff_gcds
    damage_gcds = max(0, damage_gcds)

    # Potency
    filler_potency_total = damage_gcds * filler_potency
    burst_uses = duration_s / burst_cd if burst_cd > 0 else 0
    burst_potency_total = burst_uses * burst_potency
    payoff_potency_total = payoff_procs * payoff_potency
    total_potency = filler_potency_total + burst_potency_total + payoff_potency_total

    # Percentages
    pct_damage = damage_gcds / total_gcds * 100 if total_gcds > 0 else 0
    pct_heal = gcd_heals_needed / total_gcds * 100 if total_gcds > 0 else 0
    pct_utility = utility_gcds / total_gcds * 100 if total_gcds > 0 else 0
    pct_payoff = payoff_gcds / total_gcds * 100 if total_gcds > 0 else 0

    # Kit functionality assessment
    tank_survives = (free_healing_total + gcd_heals_needed * gcd_heal_amount) >= tank_total_damage
    healer_survives = survival_clock > duration_s or incoming_on_healer == 0

    if tank_survives and healer_survives:
        verdict = "FUNCTIONAL"
    elif tank_survives and not healer_survives:
        verdict = f"HEALER DIES ({survival_clock:.1f}s clock)"
    elif not tank_survives:
        verdict = "TANK DIES (insufficient healing)"
    else:
        verdict = "BOTH DIE"

    return {
        "label": label,
        "rank": rank,
        "duration": duration_s,
        "total_gcds": total_gcds,
        "pct_damage": pct_damage,
        "pct_heal": pct_heal,
        "pct_utility": pct_utility,
        "pct_payoff": pct_payoff,
        "survival_clock": survival_clock,
        "healer_survives": healer_survives,
        "tank_survives": tank_survives,
        "verdict": verdict,
        "gcd_heals": gcd_heals_needed,
        "utility_gcds": utility_gcds,
        "damage_gcds": damage_gcds,
        "potency_per_second": total_potency / duration_s if duration_s > 0 else 0,
        "incoming_on_healer": incoming_on_healer,
    }


def run_reference_comparison(incoming_on_tank=150, incoming_on_healer=105, duration_s=22, rank=1):
    """Run WHM + ToS + Wavecaller comparisons at same incoming DPS.

    Returns list of results for side-by-side comparison.
    """
    results = []

    # FFXIV WHM (GCD healer reference)
    results.append(simulate_healer_combat(
        label="FFXIV WHM",
        duration_s=duration_s, incoming_on_tank=incoming_on_tank,
        incoming_on_healer=incoming_on_healer,
        rank=rank,
        healer_hp=1200, healer_dr=0.0, gcd=2.5,
        free_hps_allies=100, free_hps_self=50,
        filler_potency=310,
        gcd_heal_amount=500, gcd_self_heal=500,
        utility_actions=1,
        cc_stage=3, cc_cd=10, cc_is_ogcd=False,
        escape_cd=120,
        slow_on_enemies=0,
    ))

    # ToS Priest
    results.append(simulate_healer_combat(
        label="ToS Priest",
        duration_s=duration_s, incoming_on_tank=incoming_on_tank,
        incoming_on_healer=incoming_on_healer,
        rank=rank,
        healer_hp=1000, healer_dr=0.0, gcd=1.0,
        free_hps_allies=30, free_hps_self=30,
        filler_potency=50,
        gcd_heal_amount=400, gcd_self_heal=400,
        utility_actions=2,
        cc_stage=0, cc_cd=0,
        escape_cd=25,
        slow_on_enemies=0,
    ))

    return results


def format_results_table(results):
    """Format a list of simulation results as a printable table."""
    header = f"{'Label':<30} {'Rank':>4} {'Dmg%':>5} {'Heal%':>6} {'Util%':>6} {'Clock':>7} {'Verdict'}"
    sep = f"{'-'*30} {'-'*4} {'-'*5} {'-'*6} {'-'*6} {'-'*7} {'-'*30}"
    rows = [header, sep]
    for r in results:
        clock = f"{r['survival_clock']:.1f}s" if r['survival_clock'] < 1000 else "inf"
        rows.append(
            f"{r['label']:<30} {'R'+str(r['rank']):>4} "
            f"{r['pct_damage']:>4.0f}% {r['pct_heal']:>5.0f}% "
            f"{r['pct_utility']:>5.0f}% {clock:>7} {r['verdict']}"
        )
    return '\n'.join(rows)
