import services # type: ignore
from sims4.resources import Types # type: ignore
from career_service import add_noble_career_to_sim, getNobleCareerInstance
from sims.sim_info_types import Age
from utils import display_all_attributes, get_full_name, write_to_log

def inherit_nobility(output_func):
    try:
        sim_manager = services.sim_info_manager()
        for sim_info in sim_manager.get_all():
            
            if (sim_info.age == Age.YOUNG_ADULT):
                parents_info = sim_info.genealogy.get_parent_sim_infos_gen()
                display_all_attributes(sim_info.genealogy)

                for parent in parents_info:
                    nobility = getNobleCareerInstance(parent)

                    if not nobility == None:
                        add_noble_career_to_sim(f"{sim_info.first_name} {sim_info.last_name}", output_func)

                        career_instance = getNobleCareerInstance(sim_info)

                        if not career_instance is None:
                            career_instance.promote(nobility.level - 1 - career_instance.level)
                            
                            write_to_log(f"{get_full_name(sim_info)} is now a noble. Inherited from {get_full_name(parent)} level {nobility.user_level}")
    except Exception as e:
        output_func(f"Error: {e}")