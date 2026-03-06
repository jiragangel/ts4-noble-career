import services # type: ignore
from sims4.resources import Types # type: ignore
from career_service import add_noble_career_to_sim, getNobleCareerInstance
from sims.sim_info_types import Age

def inherit_nobility(output_func):
    try:
        sim_manager = services.sim_info_manager()
        for sim_info in sim_manager.get_all():
            if (sim_info.age == Age.TEEN):
                parents_info = sim_info.genealogy.get_parent_sim_infos_gen()

                for parent in parents_info:
                    nobility = getNobleCareerInstance(parent)

                    if not nobility == None:
                        add_noble_career_to_sim(f"{sim_info.first_name} {sim_info.last_name}", output_func)
    except Exception as e:
        output_func(f"Error: {e}")