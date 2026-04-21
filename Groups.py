from typing import Dict, Set

from BaseClasses import ItemClassification

from .Items import (
    MISSION_UNLOCK_NAMES,
    PROGRESSIVE_GUN_ITEM_NAME,
    PROGRESSIVE_GUN_ITEM_NAMES,
    goldeneye_events,
    goldeneye_pool_items,
    goldeneye_unlocks,
    item_table,
)
from .Locations import (
    EXTRA_MISSION_NAMES,
    event_locations,
    goldeneye_locations,
    location_table,
    per_difficulty_clear_locations,
    per_difficulty_objective_locations,
    shared_clear_locations,
    shared_objective_locations,
)


def _build_item_name_groups() -> Dict[str, Set[str]]:
    weapons = {
        name
        for name, data in goldeneye_pool_items.items()
        if data.classification not in (ItemClassification.filler, ItemClassification.trap)
    }
    filler = {
        name for name, data in item_table.items()
        if data.classification == ItemClassification.filler
    }
    traps = {
        name for name, data in item_table.items()
        if data.classification == ItemClassification.trap
    }
    progression = {
        name for name, data in item_table.items()
        if data.classification & ItemClassification.progression
    }
    useful = {
        name for name, data in item_table.items()
        if data.classification & ItemClassification.useful
    }

    return {
        "Mission Unlocks": set(goldeneye_unlocks),
        "Main Mission Unlocks": set(MISSION_UNLOCK_NAMES),
        "Extra Mission Unlocks": set(EXTRA_MISSION_NAMES),
        "Weapons": weapons,
        "Individual Weapons": set(PROGRESSIVE_GUN_ITEM_NAMES),
        "Progressive Weapons": {PROGRESSIVE_GUN_ITEM_NAME},
        "Ammo": {
            "9mm Ammo",
            "Rifle Ammo",
            "Shotgun Shells",
            "Magnum Rounds",
            "Golden Bullets",
            "Grenade Rounds",
            "Rockets",
        },
        "Recovery": {"Health Pack", "Body Armor"},
        "Filler": filler,
        "Traps": traps,
        "Progression": progression,
        "Useful": useful,
        "Events": set(goldeneye_events),
    }


def _is_difficulty_location(name: str, difficulty: str) -> bool:
    return f"({difficulty})" in name or f"- {difficulty} (Clear)" in name


def _build_location_name_groups() -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {
        "Goal": set(goldeneye_locations) | set(event_locations),
        "Mission Clears": set(per_difficulty_clear_locations) | set(shared_clear_locations),
        "Shared Mission Clears": set(shared_clear_locations),
        "Per-Difficulty Mission Clears": set(per_difficulty_clear_locations),
        "Objectives": set(per_difficulty_objective_locations) | set(shared_objective_locations),
        "Shared Objectives": set(shared_objective_locations),
        "Per-Difficulty Objectives": set(per_difficulty_objective_locations),
        "Agent": {name for name in location_table if _is_difficulty_location(name, "Agent")},
        "Secret Agent": {name for name in location_table if _is_difficulty_location(name, "Secret Agent")},
        "Double Agent": {name for name in location_table if _is_difficulty_location(name, "Double Agent")},
        "Extra Missions": {
            name for name, data in location_table.items()
            if data.region in EXTRA_MISSION_NAMES
        },
        "Main Missions": {
            name for name, data in location_table.items()
            if data.region is not None and data.region not in EXTRA_MISSION_NAMES
        },
    }

    for name, data in location_table.items():
        if data.region is not None:
            groups.setdefault(data.region, set()).add(name)

    return groups


item_name_groups = _build_item_name_groups()
location_name_groups = _build_location_name_groups()
