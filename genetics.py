import services # type: ignore
from career_service import add_noble_career_to_sim, getNobleCareerInstance
from tuning_ids import Constants
from utils import get_full_name, write_to_log
from collections import defaultdict
import sims4.commands  # type: ignore
from sims.sim_info_types import Species # type: ignore
from sims4.resources import Types # type: ignore

def inherit_nobility(output_func):
    try:
        sim_manager = services.sim_info_manager()
        for parent_info in sim_manager.get_all():
            parent_career = getNobleCareerInstance(parent_info)

            if not parent_career == None:
                children_info = parent_info.genealogy.get_child_sim_infos_gen()

                hierarchy = parent_career.level
                for child_info in children_info:
                    hierarchy = hierarchy - 2
                    if child_info.is_teen_or_older and child_info.household.get_home_region() == parent_info.household.get_home_region():
                        child_career = getNobleCareerInstance(child_info)

                        if child_career is None:
                            add_noble_career_to_sim(f"{get_full_name(child_info)}", output_func)
                            
                        child_career = getNobleCareerInstance(child_info)

                        if not child_career is None and hierarchy - child_career.level > 0:
                            child_career.promote(hierarchy - child_career.level)
                            
                        write_to_log(f"{get_full_name(child_info)}({child_career.user_level}) is now a noble. Inherited from {get_full_name(parent_info)}({parent_career.user_level})")


    except Exception as e:
        output_func(f"Error: {e}")

def list_all_regions():
    # 1. Access the Region Manager
    # This manager contains the data for every world (Willow Creek, etc.)
    region_manager = services.get_instance_manager(sims4.resources.Types.REGION)

    for region in region_manager.types.values():
        write_to_log(region)

def promote_to_queen_king():
    groups = defaultdict(list)

    for sim_info in services.sim_info_manager().get_all():
        career_instance = getNobleCareerInstance(sim_info)

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

            sim_career = getNobleCareerInstance(max_entry.get("sim_info"))

            if not sim_career is None and 9 - sim_career.level > 0:
                full_name = get_full_name(max_entry.get("sim_info"))
                write_to_log(f"{full_name} is promoted by {9 - sim_career.level} levels")
                sim_career.promote(9 - sim_career.level) 

    # check if there is a royal in a region
    for region in services.get_instance_manager(sims4.resources.Types.REGION).types.values():
        has_royal = False
        for sim_info in services.sim_info_manager().get_all():
            career_instance = getNobleCareerInstance(sim_info)

            if not career_instance is None and sim_info.household.get_home_region() == region and sim_info.species == Species.HUMAN:
               has_royal = True
        
        if not has_royal:
            write_to_log(f"No royal found for {region}")
            for sim_info in services.sim_info_manager().get_all():
                if sim_info.is_teen_or_older and sim_info.household.get_home_region() == region and sim_info.species == Species.HUMAN:
                    kingdom_manager = services.kingdom_service()
                    kingdom_manager.add_noble_career(sim_info.id)
                    instance_manager = services.get_instance_manager(Types.CAREER)
                    noble_career_tuning = instance_manager.get(Constants.NOBLE)
                    sim_info.career_tracker.add_career(noble_career_tuning(sim_info))
                    write_to_log(f"Added Noble career to {sim_info.first_name} {sim_info.last_name}")

                    break
        else:
            write_to_log(f"Royal found for {region}")