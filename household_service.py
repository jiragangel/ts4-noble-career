from career_service import getCareerInstance
import services # type: ignore
from sims.sim_info_types import Gender # type: ignore
import random
import lists
from tuning_ids import Constants
from utils import display_all_attributes, get_children_of_sim
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

def homeless_to_homes(output_func):
    try:
        display_all_attributes(services);
        household_manager = services.household_manager()
        persistence_service = services.get_persistence_service()
        venue_service = services.venue_service()
        if household_manager is None or persistence_service is None or venue_service is None:
            output_func("Household, persistence, or venue service not found.")
            return False

        households = list(household_manager.get_all())
        occupied_zone_ids = {
            household.home_zone_id
            for household in households
            if household is not None and household.home_zone_id
        }
        homeless_households = [
            household
            for household in households
            if household is not None
            and household.household_size > 0
            and not household.home_zone_id
            # MAY DELETE IF INCORRECTLY IDENTIFIED
            and not any(sim_info.is_ghost for sim_info in household.sim_info_gen())
        ]
        vacant_lots = []
        for lot in persistence_service.get_lots_proto_buff_gen():
            zone_id = lot.zone_instance_id
            if not zone_id or zone_id in occupied_zone_ids:
                continue

            venue = venue_service.get_venue_tuning(zone_id)
            if venue is not None and venue.is_residential:
                vacant_lots.append(zone_id)

        moved_households = 0
        housed_sims = 0
        for household, zone_id in zip(homeless_households, vacant_lots):
            try:
                household.set_household_lot_ownership(zone_id=zone_id)
                moved_households += 1
                housed_sims += household.household_size
                output_func(
                    f"Moved {household.name} ({household.household_size} Sims) "
                    f"to residential lot {zone_id}."
                )
            except Exception as e:
                output_func(f"Error moving household {household.name}: {e}")

        remaining_households = len(homeless_households) - moved_households
        output_func(
            f"Housed {housed_sims} Sims in {moved_households} households. "
            f"{remaining_households} homeless households remain."
        )
        return True
    except Exception as e:
        output_func(f"Error moving homeless households into homes: {e}")
        return False

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

def get_name(sim_info, is_royal = False):
    if is_royal:
        if sim_info.gender == Gender.FEMALE:
            return random.choice(lists.get_royal_female_names())
        else:
            return random.choice(lists.get_royal_male_names())
    else:
        if sim_info.gender == Gender.FEMALE:
            return random.choice(lists.female_names)
        else:
            return random.choice(lists.male_names)

def get_surname(is_royal = False):
    if is_royal:
        return random.choice(lists.get_royal_surnames())
      
    return random.choice(lists.surnames)

def rename_married_sims(output):
    try:
        processed_sim_ids = []
        count = 0
        error_count = 0

        all_sims = list(services.sim_info_manager().get_all())

        for sim_info in all_sims:
            if sim_info.last_name in lists.get_exempted_surnames():
                continue

            if sim_info.sim_id in processed_sim_ids:
                continue

            sim_info_ci = getCareerInstance(sim_info)

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    spouse_info_ci = getCareerInstance(spouse_info)
                    is_royal = (not sim_info_ci is None) or (not spouse_info_ci is None)

                    children_info = get_children_of_sim(sim_info)

                    for child in children_info:
                        child_info_ci = getCareerInstance(child)
                        if not child_info_ci is None:
                            is_royal = True
                            break

                    new_surname = get_surname(is_royal)
                    
                    sim_info.first_name = get_name(sim_info, is_royal)
                    sim_info.last_name = new_surname
                    spouse_info.first_name = get_name(spouse_info, is_royal)
                    spouse_info.last_name = new_surname
                    
                    processed_sim_ids.append(sim_info.sim_id)
                    processed_sim_ids.append(spouse_info.sim_id)
                    
                    count += 1

                    for child in children_info:
                        child_spouse_info = get_spouse_info_by_id(child.sim_id)
                        
                        if not child_spouse_info:
                            child.last_name = new_surname
                            child.first_name = get_name(child, is_royal)
                            processed_sim_ids.append(child.sim_id)
                    
                    log_msg = f"SUCCESS: {new_surname} family"

                    sim_info.household.name = new_surname
                    output(log_msg)

            except Exception as e:
                output(f"ERR Sim {sim_info.sim_id}: {str(e)}")
                error_count += 1
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

            if sim_info.last_name in lists.get_exempted_surnames():
                continue

            if not sim_info.is_teen_or_older:
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    continue
                
                sim_info_ci = getCareerInstance(sim_info)
                new_surname = get_surname((not sim_info_ci is None))
                new_firstname = get_name(sim_info, (not sim_info_ci is None))
                    
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
    