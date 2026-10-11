import random

import services # type: ignore
from career_service import add_noble_career_to_sim, getCareerInstance
from tuning_ids import Constants
from utils import get_full_name, write_to_log
from collections import defaultdict
from sims.sim_info_types import Gender, Species # type: ignore
from sims4.resources import Types # type: ignore

def list_all_regions():
    # 1. Access the Region Manager
    # This manager contains the data for every world (Willow Creek, etc.)
    region_manager = services.get_instance_manager(sims4.resources.Types.REGION)

    for region in region_manager.types.values():
        write_to_log(region)

def randomize_married_monarchs(output_func):
    try:
        sim_info_manager = services.sim_info_manager()
        if sim_info_manager is None:
            output_func("Sim info manager not found.")
            return False

        candidates_by_region = defaultdict(list)
        regions_with_monarchs = set()
        for sim_info in sim_info_manager.get_all():
            if sim_info is None or sim_info.household is None:
                continue

            region = sim_info.household.get_home_region()
            career_instance = getCareerInstance(sim_info)
            if career_instance is not None and career_instance.level == 9:
                regions_with_monarchs.add(region)

            if (
                sim_info.species != Species.HUMAN
                or sim_info.gender not in (Gender.FEMALE, Gender.MALE)
                or not sim_info.is_teen_or_older
                or not sim_info.spouse_sim_id
                or sim_info_manager.get(sim_info.spouse_sim_id) is None
            ):
                continue

            if region is not None:
                candidates_by_region[region].append(sim_info)

        if not candidates_by_region:
            output_func("No eligible married Sims were found.")
            return True

        promoted_count = 0
        error_count = 0
        for region, candidates in candidates_by_region.items():
            if region in regions_with_monarchs:
                output_func(f"Skipping {region}: a king or queen already exists.")
                continue

            sim_info = random.choice(candidates)
            try:
                career_instance = getCareerInstance(sim_info)
                if career_instance is None:
                    add_noble_career_to_sim(output_func, sim_info, 9)
                    career_instance = getCareerInstance(sim_info)
                elif career_instance.level < 9:
                    career_instance.promote(9 - career_instance.level)

                if career_instance is None or career_instance.level < 9:
                    raise RuntimeError("The Sim did not reach Noble career level 9.")

                output_func(
                    f"{get_full_name(sim_info)} was made "
                    f"{'queen' if sim_info.gender == Gender.FEMALE else 'king'} "
                    f"of {region}."
                )
                promoted_count += 1
            except Exception as e:
                error_count += 1
                output_func(
                    f"Error making {get_full_name(sim_info)} monarch of {region}: {e}"
                )

        output_func(
            f"Made {promoted_count} married Sims monarchs. Errors: {error_count}."
        )
        return error_count == 0
    except Exception as e:
        output_func(f"Error selecting married monarchs: {e}")
        return False

def promote_to_queen_king(output_func):
    groups = defaultdict(list)

    for sim_info in services.sim_info_manager().get_all():
        career_instance = getCareerInstance(sim_info)

        if not career_instance is None:
            sim_dict = dict({ 'sim_info': sim_info,  'level': career_instance.level })
            groups[sim_info.household.get_home_region()].append(sim_dict)

    for [region, royals] in groups.items():
        write_to_log(region)

        has_king_or_queen = False
        for royal in royals:
            full_name = get_full_name(royal.get("sim_info"))
            level = royal.get("level")
            write_to_log(f"{full_name} {level}")
            if level == 9:
                has_king_or_queen = True

        if not has_king_or_queen:
            write_to_log("no monarchy")
            # get highest
            max_entry = max(royals, key=lambda entry: entry.get("level"))

            sim_career = getCareerInstance(max_entry.get("sim_info"))

            if not sim_career is None and 9 - sim_career.level > 0:
                full_name = get_full_name(max_entry.get("sim_info"))
                output_func(f"{full_name} is promoted by {9 - sim_career.level} levels")
                sim_career.promote(9 - sim_career.level)
