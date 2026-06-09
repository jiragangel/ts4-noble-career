import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants
from career_service import getCareerInstance
from utils import display_all_attributes

def compute_fame_points(career_level: int):
    if career_level > 7:
        return 5262
    
    if career_level > 5:
        return 4177
    
    if career_level > 3:
        return 2625
    
    if career_level > 1:
        return 1377

    return 499

def increase_fame_for_nobles(output_func):
    try:
        sim_manager = services.sim_info_manager()
        for sim_info in sim_manager.get_all():
            ci = getCareerInstance(sim_info)
            if not ci:
                continue

            output_func(f"{sim_info.first_name} {sim_info.last_name} is a noble. Process")
            commodity_manager = services.get_instance_manager(Types.STATISTIC)
            fame_commodity = commodity_manager.get(Constants.FAME) # Fame ID

            commodity_tracker = sim_info.commodity_tracker
            if commodity_tracker is not None:
                fame_points = compute_fame_points(ci.level)
                commodity_tracker.set_value(fame_commodity, fame_points)
                output_func(f"{sim_info.first_name} {sim_info.last_name}'s celebrity is set to {fame_points}!")

    except Exception as e:
        output_func(f"Error: {e}")