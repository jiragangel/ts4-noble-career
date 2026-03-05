import inspect
import services # type: ignore

def display_all_attributes(object, f):
    all_members = inspect.getmembers(object)

    for name, value in all_members:
        print(f"{name}: {value}", file=f)

def get_full_name(sim_info):
    return f"{sim_info.first_name} {sim_info.last_name}"

def get_children_of_sim(sim_info):
    """Returns a list of SimInfo objects for all biological/legal children."""
    
    file_path = "C:/Users/jiraa/Downloads/jira_mod/output.txt"

    if sim_info is None or sim_info.genealogy is None:
        return []
    
    with open(file_path, "w") as f:
        display_all_attributes(sim_info.genealogy, f)
    
    # The genealogy tracker returns a list of Sim IDs
    children_ids = sim_info.genealogy.get_children_sim_ids_gen()
    sim_info_manager = services.sim_info_manager()
    
    children_sim_infos = []
    for sim_id in children_ids:
        child_info = sim_info_manager.get(sim_id)
        if child_info is not None:
            children_sim_infos.append(child_info)
            
    return children_sim_infos