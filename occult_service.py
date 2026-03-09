from household_service import get_spouse_info_by_id
import services # type: ignore
import random
from sims4.resources import Types # type: ignore
from tuning_ids import Constants
from sims.sim_info_types import Gender # type: ignore
from utils import get_children_of_sim, get_full_name, write_to_log # type: ignore

OCCULT_TRAITS = {
    'Fairy': Constants.FAIRY, 
    'Mermaid': Constants.MERMAID, 
    'Witch': Constants.WITCH, 
    'Werewolf': Constants.WEREWOLF, 
    'Vampire': Constants.VAMPIRE
}

VALID_OCCULT_TRAITS = ['Witch', 'Werewolf', 'Mermaid', 'Fairy']

def set_occult_per_family(output):
    try:
        trait_manager = services.get_instance_manager(Types.TRAIT)
        active_household_id = services.active_household_id()
        
        count = 0
        error_count = 0

        all_sims = list(services.sim_info_manager().get_all())

        for sim_info in all_sims:
            if sim_info is None or not hasattr(sim_info, 'sim_id'):
                continue

            if sim_info.household_id == active_household_id:
                continue

            if sim_info.gender != Gender.FEMALE: 
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    write_to_log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    write_to_log(f"{sim_info.last_name} family")
                    count += 1

                    children_info = get_children_of_sim(sim_info)

                    # set occult of couple
                    family_occult_trait = Constants.MERMAID
                    for occult_id in OCCULT_TRAITS.values():
                        if sim_info.has_trait(trait_manager.get(occult_id)):
                            family_occult_trait = occult_id
                            break

                    remove_all_occult(sim_info)
                    remove_all_occult(spouse_info)

                    add_occult_to_sim(sim_info, family_occult_trait)
                    add_occult_to_sim(spouse_info, family_occult_trait)

                    for child in children_info:
                        child_spouse_info = get_spouse_info_by_id(child.sim_id)
                        
                        # child is not yet married
                        if not child_spouse_info:
                            remove_all_occult(child)
                            add_occult_to_sim(child, family_occult_trait)

                    

            except Exception as e:
                output(f"ERR Sim {sim_info.sim_id}: {str(e)}")
                error_count += 1

        final_msg = f"Completed. Updated {count} families. Errors: {error_count}"
        output(final_msg)
        return True

    except Exception as e:
        output(f"Crash: {str(e)}")
        return False

def add_occult_to_sim(sim_info, occult_id):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    occult = trait_manager.get(occult_id)
    
    write_to_log(f"Adding {occult} to {get_full_name(sim_info)}")

    sim_info.add_trait(occult)
    if occult_id == Constants.FAIRY:
        sim_info.add_trait(trait_manager.get(Constants.FAIRY_FYAE))

def remove_all_occult(sim_info):
    write_to_log(f"Removing all occults from {get_full_name(sim_info)}")
    trait_manager = services.get_instance_manager(Types.TRAIT)
    
    for occult_id in OCCULT_TRAITS.values():
        sim_info.remove_trait(trait_manager.get(occult_id))
    
    sim_info.remove_trait(trait_manager.get(Constants.FAIRY_FYAE))

def remove_aliens(output):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    all_sims = services.sim_info_manager().get_all()
    
    for sim_info in all_sims:
        alien_trait = trait_manager.get(Constants.ALIEN)
        if sim_info.has_trait(alien_trait):
            sim_info.remove_trait(alien_trait)
            output(f"Cleaned {sim_info.first_name} {sim_info.last_name}")

def randomize_occults(output_func):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    all_sims = services.sim_info_manager().get_all()
    
    for sim_info in all_sims:
        if sim_info.is_child_or_younger: continue
        
        is_occult = any(sim_info.has_trait(trait_manager.get(tid)) for tid in OCCULT_TRAITS.values() if trait_manager.get(tid))
        
        if not is_occult and random.random() > -1:
            choice_name = random.choice(VALID_OCCULT_TRAITS)
            trait = trait_manager.get(OCCULT_TRAITS[choice_name])
            if trait:
                sim_info.add_trait(trait)
                if OCCULT_TRAITS[choice_name] == Constants.FAIRY:
                    sim_info.add_trait(trait_manager.get(Constants.FAIRY_FYAE))
                output_func(f"Converted {get_full_name(sim_info)} to {choice_name}")



def cleanup_hybrids(output_func):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    all_sims = services.sim_info_manager().get_all()
    
    for sim_info in all_sims:
        occults = []
        for tid in OCCULT_TRAITS.values():
            if trait_manager.get(tid) and sim_info.has_trait(trait_manager.get(tid)):
                occults.append(trait_manager.get(tid))
        
        if len(occults) > 1:
            output_func(f"{sim_info.first_name} {sim_info.last_name} has {len(occults)} occults")
            occults.pop()
            for occult in occults:
                sim_info.remove_trait(occult)
            output_func(f"Cleaned {sim_info.first_name} {sim_info.last_name}")