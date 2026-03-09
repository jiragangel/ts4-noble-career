import services # type: ignore
from career_service import add_noble_career_to_sim, getNobleCareerInstance
from utils import get_full_name, write_to_log

def inherit_nobility(output_func):
    try:
        sim_manager = services.sim_info_manager()
        for parent_info in sim_manager.get_all():
            parent_career = getNobleCareerInstance(parent_info)

            if not parent_career == None:
                children_info = parent_info.genealogy.get_child_sim_infos_gen()

                hierarchy = parent_career.level - 1
                for child_info in children_info:
                    if child_info.is_teen_or_older:
                        child_career = getNobleCareerInstance(child_info)

                        if child_career is None:
                            add_noble_career_to_sim(f"{get_full_name(child_info)}", output_func)
                            
                        child_career = getNobleCareerInstance(child_info)

                        if not child_career is None and hierarchy - child_career.level > 0:
                            child_career.promote(hierarchy - child_career.level)
                            
                        write_to_log(f"{get_full_name(child_info)}({child_career.user_level}) is now a noble. Inherited from {get_full_name(parent_info)}({parent_career.user_level})")

                    hierarchy = hierarchy - 1

    except Exception as e:
        output_func(f"Error: {e}")