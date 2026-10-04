import inspect
import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants # type: ignore

LOG_FILE_PATH = 'C:/Users/jiraa/Documents/Electronic Arts/The Sims 4/Mods/jira_mod/output.txt'

def check_bit_on_sim(sim_info_a, sim_info_b, bit_instance):
    try:
        # sim_info_a.relationship_tracker is the RelationshipTracker
        return sim_info_a.relationship_tracker.has_bit(sim_info_b.sim_id, bit_instance)
    except Exception as e:
        write_to_log(f"Unexpected error in check_bit_on_sim: {e}")

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

def get_dynasty(sim_info):
    if sim_info is None:
        return None

    # Get sim ID
    sim_id = getattr(sim_info, 'sim_id', None) or getattr(sim_info, 'id', None)

    dynasty_service = services.dynasty_service()

    dynasty = dynasty_service.get_sim_dynasty(sim_id)

    if dynasty is not None:
        dynasty_name = dynasty.name
        return dynasty_name

    return None

def iterate_over_clubs(output):
    club_service = services.get_club_service()

    while len(club_service.clubs) > 0:
        club = next(iter(club_service.clubs))

        display_all_attributes(club)
        output(f"Club: {club.name}")

        club_service.remove_club(club)


def iterate_over_dynasties(output):
    dynasty_service = services.dynasty_service()

    translations = [
        {
            "name": "Montez",
            "description": "After generations of drama and conflict with the Caputo family, the Montez family is ready to rise from the ashes and reclaim their power."
        },
        {
            "name": "Alto",
            "description": "Passion, love, and toxicity... These are the hallmarks of the Alto family."
        },
        {
            "name": "Caputo",
            "description": "Everyone in Bellacorde admires the Caputo family and its motto: Honor Sets Us Apart. They belong to an illustrious Dynasty known by many as romantic, gallant, and proud. However, some also describe them as presumptuous, elitist, and melodramatic."
        },
        {
            "name": "Darongue",
            "description": "The Darongue family belongs to a philanthropic Dynasty that has worked for generations to lead Dambele into a golden age of art and prosperity. The family's motto is known throughout Dambele: Strength Lies in Unity."
        },
        {
            "name": "Tebas",
            "description": "Strong as the tides, fierce as the sea, the Tebas family is known for its motto, We Face the Storm. This Dynasty takes great pride in its adventures and the treasures it has collected, while boasting a mixed lineage of princesses and pirates."
        },
        {
            "name": "Abrantes",
            "description": "The Abrantes family has risen through the ranks and is now known as the most refined Dynasty in Verdemar. But don't let appearances deceive you—they always get what they want."
        },
        {
            "name": "Straud",
            "description": "Vladislaus, a vampire over 200 years old, is the founder of Forgotten Hollow. There is a statue in the town square that Sims believe depicts his great-grandfather, but the vampires know the truth: the sculpture represents Vlad himself, still alive in the shadows of the town."
        },
        {
            "name": "Villareal",
            "description": "The ancient Villareal family dynasty rules its lands with prestige and mystery. Between noble alliances and ancient secrets, their legacy spans generations and keeps the Villareal family's influence alive."
        },
        {
            "name": "Caixão",
            "description": "The Caixão family is an aristocratic family with a somewhat dark aura and many hidden secrets. Perhaps their proximity to death is what fuels this deep passion?"
        },
        {
            "name": "Quero-Tudo-Que-É-Seu",
            "description": "The Quero-Tudo-Que-É-Seu family seems perfect: wealthy, educated, and brilliant. Yet beneath their elegant exterior, they conceal internal conflicts and ruthless intentions."
        },
        {
            "name": "Tebas-Laurent",
            "description": "The Thebe-Laurent Dynasty has shaped the life of the village for generations. Guardians of the local traditional wedding venue, they have not only turned celebrations into a legacy but also helped drive the local cuisine and marketplace."
        },
        {
            "name": "Feng",
            "description": "The ancient Feng Dynasty thrives in the shadows of San Myshuno. Victor dominates politics with calculated elegance, while Lílian runs financial empires while concealing cruel and sinister ambitions."
        }
    ]

    for dynasty in dynasty_service.get_all_dynasties():
        details = dynasty_service.get_dynasty(dynasty)
        details.set_name_and_description(details.name, next((item for item in translations if item["name"] == details.name), None).get("description", "No description available."))



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