# DESIGN_OVERRIDE_OTHER_ROLES.md
# ═══════════════════════════════════════════════════════════════════════════════
# DPS SUBCATEGORY TAXONOMY — TODO
# ═══════════════════════════════════════════════════════════════════════════════
#
# Authority: This file is authoritative for DPS role subcategories once defined.
# Mirrors: DESIGN_OVERRIDE_FRONTLINE.md (frontliners), DESIGN_OVERRIDE_HEALER.md (healers)
# Last updated: 2026-07-16
# Status: PLACEHOLDER — awaiting discovery sessions
# ═══════════════════════════════════════════════════════════════════════════════

## Status: PENDING DISCOVERY

The frontliner taxonomy (DESIGN_OVERRIDE_FRONTLINE.md) proved that defining race-agnostic
mechanical subcategories BEFORE writing class files prevents identity drift. The healer
taxonomy has been split to its own file (DESIGN_OVERRIDE_HEALER.md). This file covers DPS only.

## Problem Statement

Current DPS class files have:
- Too much emphasis on specific abilities with functional cross-references
- Not enough filtering to define what their GOALS ARE IN COMBAT
- The same hollow-identity pattern frontliners had before taxonomy work

The fix is the same: define race-agnostic mechanical subcategories FIRST, then place
classes into those fields.

## DPS Subcategories (TBD — needs discovery session)

What are the mechanical BEHAVIORS a DPS can express?
Possible axes (DO NOT ASSUME THESE ARE CORRECT — listed as starting points only):
- Burst vs sustained vs DoT vs setup?
- Ranged vs melee vs hybrid?
- Solo-target vs AoE vs cleave?
- Committed (can't disengage) vs flexible (can reposition freely)?
- Pursuit-locked (Reaver) vs opportunistic vs zone-denial?

Current DPS files lean on ability lists and game-character references instead of
mechanical behavior definitions. The question is NOT "what does this class DO" but
"what is this class's GOAL in combat and how does the party BENEFIT from its presence?"

## Priority

Define the fields → audit existing classes against them → rewrite as needed.
Same workflow as frontliners:
1. Discovery session (human defines the contract and mechanical behaviors)
2. Taxonomy file written (this file, expanded)
3. Class files audited and rewritten where hollow

## Authority

This file: pending. Once DPS taxonomies are defined, this file becomes authoritative
for DPS roles in the same way DESIGN_OVERRIDE_FRONTLINE.md is authoritative for
frontliner subcategories.
