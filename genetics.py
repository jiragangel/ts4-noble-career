import services # type: ignore
from career_service import add_noble_career_to_sim, getCareerInstance
from tuning_ids import Constants
from utils import get_full_name, write_to_log
from collections import defaultdict
from sims.sim_info_types import Species # type: ignore
from sims4.resources import Types # type: ignore

def list_all_regions():
    # 1. Access the Region Manager
    # This manager contains the data for every world (Willow Creek, etc.)
    region_manager = services.get_instance_manager(sims4.resources.Types.REGION)

    for region in region_manager.types.values():
        write_to_log(region)

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
