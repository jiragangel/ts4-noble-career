import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants
import random
from sims.sim_info_types import Species
from utils import get_full_name # type: ignore

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
                random_career_id = random.choice([Constants.BUSINESS, Constants.CULINARY, Constants.ENTERTAINER, Constants.DOCTOR])
                career_tuning = instance_manager.get(random_career_id)
                new_career_instance = career_tuning(sim_info)
                sim_info.career_tracker.add_career(new_career_instance)

                career_instance = getCareerInstance(sim_info, random_career_id)
                promotion_count = random.randint(1, 9)
                career_instance.promote(promotion_count)
                output_func(f"Added career to {sim_info.first_name} {sim_info.last_name} and promoted {promotion_count} times.")

def add_noble_career_to_sim(output_func, sim_info, target_career_level = random.randint(1, 6)):
    noble_career_id = Constants.NOBLE
    instance_manager = services.get_instance_manager(Types.CAREER)
    noble_career_tuning = instance_manager.get(noble_career_id)

    # Instantiate and add career
    new_career_instance = noble_career_tuning(sim_info)
    sim_info.career_tracker.add_career(new_career_instance)
    
    kingdom_manager = services.kingdom_service()
    kingdom_manager.add_noble_career(sim_info.id)
    instance_manager = services.get_instance_manager(Types.CAREER)
    noble_career_tuning = instance_manager.get(Constants.NOBLE)
    sim_info.career_tracker.add_career(noble_career_tuning(sim_info))

    career_instance = getCareerInstance(sim_info, Constants.NOBLE)
    if target_career_level > career_instance.level:
        career_instance.promote(target_career_level - career_instance.level)
    output_func(f"Added Noble career ({target_career_level}) to {sim_info.first_name} {sim_info.last_name}")

def randomize_nobles(output_func):
    for sim_info in services.sim_info_manager().get_all():
        if sim_info.is_teen and random.randint(1, 4) == 1 and sim_info.species == Species.HUMAN:
           add_noble_career_to_sim(output_func, sim_info)


def getCareerInstance(sim_info, career_id = Constants.NOBLE):
    career_manager = services.get_instance_manager(Types.CAREER)
    career_target = career_manager.get(career_id) 
    if not sim_info.is_teen_or_older:
        return None

    tracker = sim_info.career_tracker
    if tracker is None:
        return None

    for career_instance in tracker.careers.values():
        if isinstance(career_instance, career_target):
            return career_instance
    
    return None

def isValidForCareer(sim_info):
    if not sim_info.is_teen_or_older:
        return False

    tracker = sim_info.career_tracker
    if tracker is None:
        return True

    if len(tracker.careers.values()) > 0:
        return False
    
    return True