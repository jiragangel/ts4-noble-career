import services # type: ignore
from career_service import add_noble_career_to_sim, getCareerInstance
from tuning_ids import Constants
from utils import get_full_name, write_to_log
from collections import defaultdict
from sims.sim_info_types import Species # type: ignore
from sims4.resources import Types # type: ignore

def inherit_nobility(output_func):
    try:
        sim_manager = services.sim_info_manager()
        for parent_info in sim_manager.get_all():
            parent_career = getCareerInstance(parent_info)

            if not parent_career == None:
                children_info = parent_info.genealogy.get_child_sim_infos_gen()

                hierarchy = parent_career.level
                for child_info in children_info:
                    hierarchy = hierarchy - 2
                    if child_info.is_teen_or_older and child_info.household.get_home_region() == parent_info.household.get_home_region():
                        child_career = getCareerInstance(child_info)

                        if child_career is None:
                            add_noble_career_to_sim(output_func, child_info, hierarchy)
                            
                            output_func(f"{get_full_name(child_info)} is now a noble from {parent_info.household.get_home_region()}")


    except Exception as e:
        output_func(f"Error: {e}")

def list_all_regions():
    # 1. Access the Region Manager
    # This manager contains the data for every world (Willow Creek, etc.)
    region_manager = services.get_instance_manager(sims4.resources.Types.REGION)

    for region in region_manager.types.values():
        write_to_log(region)
