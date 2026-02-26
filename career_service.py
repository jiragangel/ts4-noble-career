import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants

def add_noble_career_to_sim(last_name: str, output_func):
    search_last = last_name.strip().lower()
    noble_career_id = Constants.NOBLE
    instance_manager = services.get_instance_manager(Types.CAREER)
    noble_career_tuning = instance_manager.get(noble_career_id)

    for sim_info in services.sim_info_manager().get_all():
        if (sim_info.last_name.lower() == search_last and sim_info.is_teen_or_older) or (not last_name and sim_info.is_teen_or_older):
            # Instantiate and add career
            new_career_instance = noble_career_tuning(sim_info)
            sim_info.career_tracker.add_career(new_career_instance)
            output_func(f"Added Noble career to {sim_info.first_name} {sim_info.last_name}")

def getNobleCareerInstance(sim_info, output_func):
    career_manager = services.get_instance_manager(Types.CAREER)
    Career_noble = career_manager.get(Constants.NOBLE) 
    if not sim_info.is_teen_or_older:
        return None

    tracker = sim_info.career_tracker
    if tracker is None:
        return None

    for career_instance in tracker.careers.values():
        if isinstance(career_instance, Career_noble):
            output_func(f"Processing Noble: {sim_info.first_name} {sim_info.last_name}")
            return career_instance
    
    return None


def promote_noble_dynasty(output_func):
    # 1. Get the Noble Career class from the instance manager
    # Replace 123456789 with your career's Decimal Tuning ID
    career_manager = services.get_instance_manager(Types.CAREER)
    Career_noble = career_manager.get(Constants.NOBLE) 

    if Career_noble is None:
        output_func("ERROR: Career_noble tuning not found. Please check the Tuning ID.")
        return

    output_func(">>> Starting Noble Dynasty Promotion...")
    success_count = 0

    for sim_info in services.sim_info_manager().get_all():
        if not sim_info.is_teen_or_older:
            continue

        tracker = sim_info.career_tracker
        if tracker is None:
            continue

        try:
            career_instance = getNobleCareerInstance(sim_info, output_func)

            if not career_instance is None:
                promotions_given = 0
                for _ in range(5):
                    career_instance.promote()
                    promotions_given += 1
                
                output_func(f"{sim_info.first_name} {sim_info.last_name}  - Successfully promoted {promotions_given} times.")
                success_count += 1
                    
        except Exception as e:
            # Log specific errors without stopping the whole loop
            output_func(f"Error on {sim_info.last_name}: {str(e)}")

    output_func(f">>> Finished. Total Nobles updated: {success_count}")
