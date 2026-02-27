import services # type: ignore
from sims.sim_info_types import Gender # type: ignore
import random
from lists import male_names, female_names, surnames

exempted_surnames = ['Everhart', 'Crowmoor', 'Beaumont', 'Salvatore', 'Triton']

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

def randomize_townie_marriage_names(output):
    try:
        active_household_id = services.active_household_id()
        
        processed_sim_ids = set()
        count = 0
        error_count = 0

        all_sims = list(services.sim_info_manager().get_all())

        for sim_info in all_sims:
            if sim_info is None or not hasattr(sim_info, 'sim_id'):
                continue

            if not surnames:
                break

            if sim_info.sim_id in processed_sim_ids or sim_info.household_id == active_household_id:
                continue

            if sim_info.gender != Gender.FEMALE: 
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    new_surname = random.choice(surnames)
                    surnames.remove(new_surname)
                    
                    new_female_fn = random.choice(female_names)
                    new_male_fn = random.choice(male_names)

                    old_names = f"{sim_info.first_name} {sim_info.last_name} & {spouse_info.first_name} {spouse_info.last_name}"
                    
                    sim_info.first_name = new_female_fn
                    sim_info.last_name = new_surname
                    spouse_info.first_name = new_male_fn
                    spouse_info.last_name = new_surname
                    
                    processed_sim_ids.add(sim_info.sim_id)
                    processed_sim_ids.add(spouse_info.sim_id)
                    
                    count += 1
                    log_msg = f"SUCCESS: {old_names} -> {new_female_fn} & {new_male_fn} {new_surname}"
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

            if not surnames:
                break

            if sim_info.household_id == active_household_id:
                continue

            if sim_info.last_name in exempted_surnames:
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    output(f'{sim_info.first_name} {sim_info.last_name} has spouse')
                    continue

                new_surname = random.choice(surnames)
                surnames.remove(new_surname)
                
                new_firstname = ''
                
                if sim_info.gender == Gender.FEMALE:
                    new_firstname = random.choice(female_names)
                else:
                    new_firstname = random.choice(male_names)
                    
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
    