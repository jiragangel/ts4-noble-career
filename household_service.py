import services # type: ignore
from sims.sim_info_types import Gender # type: ignore
import random
import lists
from tuning_ids import Constants
from utils import get_children_of_sim
from sims4.resources import Types # type: ignore

def update_all_household_funds(amount: int, output_func):
    household_manager = services.household_manager()
    count = 0
    for household in household_manager.get_all():
        try:
            household.funds.add(amount, 1)
            count += 1
        except Exception as e:
            output_func(f"Error updating household: {e}")
    output_func(f"Updated {count} households.")

def get_spouse_info_by_id(sim_id):
    """
    Core function to safely retrieve a spouse's SimInfo object.
    """
    sim_info_manager = services.sim_info_manager()
    sim_info = sim_info_manager.get(sim_id)
    
    if sim_info is None:
        return None

    # Use the built-in spouse_sim_id property
    # This returns 0 if they are not married
    spouse_id = sim_info.spouse_sim_id
    
    if spouse_id:
        return sim_info_manager.get(spouse_id)
    
    return None

def get_name(sim_info):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    
    if sim_info.has_trait(trait_manager.get(Constants.FAIRY)):
        if sim_info.gender == Gender.FEMALE:
            return random.choice(lists.female_fairy_names)
        else:
            return random.choice(lists.male_fairy_names)
    
    if sim_info.has_trait(trait_manager.get(Constants.MERMAID)):
        if sim_info.gender == Gender.FEMALE:
            return random.choice(lists.female_mermaid_names)
        else:
            return random.choice(lists.male_mermaid_names)
    
    if sim_info.has_trait(trait_manager.get(Constants.WEREWOLF)):
        if sim_info.gender == Gender.FEMALE:
            return random.choice(lists.female_werewolf_names)
        else:
            return random.choice(lists.male_werewolf_names)
    
    if sim_info.has_trait(trait_manager.get(Constants.VAMPIRE)):
        if sim_info.gender == Gender.FEMALE:
            return random.choice(lists.female_vampire_names)
        else:
            return random.choice(lists.male_vampire_names)
        
    if sim_info.gender == Gender.FEMALE:
        return random.choice(lists.female_names)
    else:
        return random.choice(lists.male_names)

def get_surname(sim_info):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    
    if sim_info.has_trait(trait_manager.get(Constants.MERMAID)):
        return random.choice(lists.get_mermaid_surnames())
    
    if sim_info.has_trait(trait_manager.get(Constants.FAIRY)):
        return random.choice(lists.fairy_surnames)
    
    if sim_info.has_trait(trait_manager.get(Constants.WEREWOLF)):
        return random.choice(lists.werewolf_surnames)
    
    if sim_info.has_trait(trait_manager.get(Constants.WITCH)):
        return random.choice(lists.get_spellcaster_surnames())
      
    return random.choice(lists.surnames)

def randomize_townie_marriage_names(output):
    try:
        processed_sim_ids = []
        count = 0
        error_count = 0

        all_sims = list(services.sim_info_manager().get_all())

        for sim_info in all_sims:
            if sim_info is None or not hasattr(sim_info, 'sim_id'):
                continue

            if sim_info.last_name in lists.get_exempted_surnames():
                continue

            if sim_info.sim_id in processed_sim_ids:
                continue

            if sim_info.gender != Gender.FEMALE: 
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    new_surname = get_surname(sim_info)

                    old_names = f"{sim_info.first_name} {sim_info.last_name} & {spouse_info.first_name} {spouse_info.last_name}"
                    
                    sim_info.first_name = get_name(sim_info)
                    sim_info.last_name = new_surname
                    spouse_info.first_name = get_name(spouse_info)
                    spouse_info.last_name = new_surname
                    
                    processed_sim_ids.append(sim_info.sim_id)
                    processed_sim_ids.append(spouse_info.sim_id)
                    
                    count += 1
                    log_msg = f"SUCCESS: {old_names} -> {sim_info.first_name} & {spouse_info.first_name} {new_surname}"
                    output(log_msg)

                    children_info = get_children_of_sim(sim_info)

                    output(f"{new_surname} has {len(children_info)} kids")

                    for child in children_info:
                        child_spouse_info = get_spouse_info_by_id(child.sim_id)
                        
                        if not child_spouse_info:
                            child.last_name = new_surname
                            child.first_name = get_name(child)
                            processed_sim_ids.append(child.sim_id)
                    
                    log_msg = f"SUCCESS: {new_surname} family"
                    output(log_msg)

            except Exception as e:
                output(f"ERR Sim {sim_info.sim_id}: {str(e)}")
                error_count += 1

        final_msg = f"Completed. Updated {count} couples. Errors: {error_count}"
        output(final_msg)
        return True

    except Exception as e:
        output(f"Crash: {str(e)}")
        return False

def randomize_townie_unmarried(output):
    try:
        active_household_id = services.active_household_id()
        
        count = 0
        error_count = 0

        all_sims = list(services.sim_info_manager().get_all())

        for sim_info in all_sims:
            if sim_info is None or not hasattr(sim_info, 'sim_id'):
                continue

            if sim_info.household_id == active_household_id:
                continue

            if sim_info.last_name in lists.get_exempted_surnames():
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    output(f'{sim_info.first_name} {sim_info.last_name} has spouse')
                    continue

                new_surname = get_surname(sim_info)
                new_firstname = get_name(sim_info)
                    
                old_names = f"{sim_info.first_name} {sim_info.last_name}"
                
                sim_info.first_name = new_firstname
                sim_info.last_name = new_surname
                
                count += 1
                log_msg = f"SUCCESS: {old_names} -> {new_firstname} {new_surname}"
                output(log_msg)

            except Exception as e:
                output(f"ERR Sim {sim_info.sim_id}: {str(e)}")
                error_count += 1

        final_msg = f"Completed. Updated {count} couples. Errors: {error_count}"
        output(final_msg)
        return True

    except Exception as e:
        output(f"Crash: {str(e)}")
        return False
    