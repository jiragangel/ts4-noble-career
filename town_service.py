from career_service import getNobleCareerInstance
import services  # type: ignore
import traceback
from sims.sim_info_types import Species # type: ignore
from sims4.resources import Types # type: ignore

from tuning_ids import Constants
from utils import get_full_name, write_to_log

def create_noble_per_town(output):
    regions = []
    
    write_to_log("Starting Town/Household Iteration...")
    try:
        # Retrieve all world data
        household_manager = services.household_manager()

        for hh in household_manager.get_all():
            region = hh.get_home_region()
            home_world_id = hh.get_home_world_id()

            if not region in regions and home_world_id != 0:
                regions.append(region)

                sims_at_home = hh.get_sims_at_home()

                for sim_id in sims_at_home:
                    sim_info_manager = services.sim_info_manager()

                    if sim_info_manager is None:
                        return None

                    # Retrieve SimInfo by ID
                    sim_info = sim_info_manager.get(sim_id)
                    if sim_info.is_teen_or_older and sim_info.species == Species.HUMAN:
                        career_instance = getNobleCareerInstance(sim_info)

                        if career_instance is None:
                            kingdom_manager = services.kingdom_service()
                            kingdom_manager.add_noble_career(sim_id)
                            instance_manager = services.get_instance_manager(Types.CAREER)
                            noble_career_tuning = instance_manager.get(Constants.NOBLE)
                            sim_info.career_tracker.add_career(noble_career_tuning(sim_info))
                                
                            write_to_log(f"{get_full_name(sim_info)} processed")

                        break
                        
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    except Exception as global_err:
        write_to_log(f"Critical script failure: {global_err}")
        write_to_log(traceback.format_exc())