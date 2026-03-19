import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants
import random
from sims.sim_info_types import Species # type: ignore

def add_random_career(output_func):
    instance_manager = services.get_instance_manager(Types.CAREER)

    for sim_info in services.sim_info_manager().get_all():
        if (sim_info.is_young_adult or sim_info.is_adult) and sim_info.species == Species.HUMAN:
            tracker = sim_info.career_tracker
            if tracker is None:
                return None
            
            output_func(f"{sim_info.first_name} {sim_info.last_name} has {len(tracker.careers.values())} career")

            if (len(tracker.careers.values()) == 0):
                # Instantiate and add career
                career_tuning = instance_manager.get(random.choice([Constants.BUSINESS, Constants.CULINARY, Constants.ENTERTAINER]))
                new_career_instance = career_tuning(sim_info)
                sim_info.career_tracker.add_career(new_career_instance)
                output_func(f"Added career to {sim_info.first_name} {sim_info.last_name}")

def add_noble_career_to_sim(full_name: str, output_func):
    search_full_name = full_name.strip().lower()
    noble_career_id = Constants.NOBLE
    instance_manager = services.get_instance_manager(Types.CAREER)
    noble_career_tuning = instance_manager.get(noble_career_id)

    for sim_info in services.sim_info_manager().get_all():
        if (search_full_name in f"{sim_info.first_name.lower()} {sim_info.last_name.lower()}" and sim_info.is_teen_or_older) or (not search_full_name and sim_info.is_teen_or_older):
            # Instantiate and add career
            new_career_instance = noble_career_tuning(sim_info)
            sim_info.career_tracker.add_career(new_career_instance)
            output_func(f"Added Noble career to {sim_info.first_name} {sim_info.last_name}")
            
            kingdom_manager = services.kingdom_service()
            kingdom_manager.add_noble_career(sim_info.id)
            instance_manager = services.get_instance_manager(Types.CAREER)
            noble_career_tuning = instance_manager.get(Constants.NOBLE)
            sim_info.career_tracker.add_career(noble_career_tuning(sim_info))

def getNobleCareerInstance(sim_info):
    career_manager = services.get_instance_manager(Types.CAREER)
    Career_noble = career_manager.get(Constants.NOBLE) 
    if not sim_info.is_teen_or_older:
        return None

    tracker = sim_info.career_tracker
    if tracker is None:
        return None

    for career_instance in tracker.careers.values():
        if isinstance(career_instance, Career_noble):
            return career_instance
    
    return None
