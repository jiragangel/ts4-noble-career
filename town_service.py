from career_service import getNobleCareerInstance
import services  # type: ignore
import traceback
from sims4.resources import Types # type: ignore

from tuning_ids import Constants

def safe_iterate_town_households(output):
    # Recommended: Use a dynamic path or ensure this folder exists!
    file_path = "C:/Users/jiraa/Downloads/jira_mod/output.txt"
    regions = []
    
    with open(file_path, "w") as f:
        print("Starting Town/Household Iteration...", file=f)
        try:
            # Retrieve all world data
            household_manager = services.household_manager()

            for hh in household_manager.get_all():
                region = hh.get_home_region()
                home_world_id = hh.get_home_world_id()
                # utils.display_all_attributes(hh, f)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f)
                print(hh.name, file=f)
                print(home_world_id, file=f)
                print(region, file=f)

                if not region in regions and home_world_id != 0:
                    regions.append(region)

                    sims_at_home = hh.get_sims_at_home()

                    for sim_id in sims_at_home:
                        sim_info_manager = services.sim_info_manager()
    
                        if sim_info_manager is None:
                            return None

                        # Retrieve SimInfo by ID
                        sim_info = sim_info_manager.get(sim_id)
                        if sim_info.is_teen_or_older:
                            career_instance = getNobleCareerInstance(sim_info, output)

                            if not career_instance is None:
                                for _ in range(10):
                                    career_instance.promote()
                            else:
                                instance_manager = services.get_instance_manager(Types.CAREER)
                                noble_career_tuning = instance_manager.get(Constants.NOBLE)
                                sim_info.career_tracker.add_career(noble_career_tuning(sim_info))

                            break
                            
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        except Exception as global_err:
            print(f"Critical script failure: {global_err}", file=f)
            print(traceback.format_exc(), file=f)