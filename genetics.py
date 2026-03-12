import services # type: ignore
from career_service import add_noble_career_to_sim, getNobleCareerInstance
from utils import get_full_name, write_to_log
from collections import defaultdict

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
                    if child_info.is_teen_or_older:
                        child_career = getNobleCareerInstance(child_info)

                        if child_career is None:
                            add_noble_career_to_sim(f"{get_full_name(child_info)}", output_func)
                            
                        child_career = getNobleCareerInstance(child_info)

                        if not child_career is None and hierarchy - child_career.level > 0:
                            child_career.promote(hierarchy - child_career.level)
                            
                        write_to_log(f"{get_full_name(child_info)}({child_career.user_level}) is now a noble. Inherited from {get_full_name(parent_info)}({parent_career.user_level})")


    except Exception as e:
        output_func(f"Error: {e}")

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
