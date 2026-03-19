import inspect
import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants # type: ignore

LOG_FILE_PATH = 'C:/Users/jiraa/Downloads/jira_mod/output.txt'

def write_to_log(message):
    """Simple helper to append lines to our custom text file."""
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")

def display_all_attributes(object):
    all_members = inspect.getmembers(object)

    for name, value in all_members:
        write_to_log(f"~~~~~~~~~~~~~~~~~~~~~~~~~{name}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        try:
            sig = inspect.signature(value)

            write_to_log("Parameter type hints:")

            for name, parameter in sig.parameters.items():
                if parameter.annotation is not inspect.Parameter.empty:
                    write_to_log(f"* {name}: {parameter.annotation}")
                else:
                    write_to_log(f"* {name}: No type hint")
            
            write_to_log(f"Returns {value.__annotations__['return']}")

        except Exception as e:
            write_to_log(f"{name}: {value}")

def get_full_name(sim_info):
    return f"{sim_info.first_name} {sim_info.last_name}"

def get_children_of_sim(sim_info):
    """Returns a list of SimInfo objects for all biological/legal children."""

    if sim_info is None or sim_info.genealogy is None:
        return []
    
    # The genealogy tracker returns a list of Sim IDs
    children_ids = sim_info.genealogy.get_children_sim_ids_gen()
    sim_info_manager = services.sim_info_manager()
    
    children_sim_infos = []
    for sim_id in children_ids:
        child_info = sim_info_manager.get(sim_id)
        if child_info is not None:
            children_sim_infos.append(child_info)
            
    return children_sim_infos

def cleanup_hustler():
    trait_manager = services.get_instance_manager(Types.TRAIT)
    sim_manager = services.sim_info_manager()
    for sim_info in sim_manager.get_all():
        sim_info.remove_trait(trait_manager.get(Constants.NOBLE_HUSTLER))