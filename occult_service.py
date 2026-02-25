import services # type: ignore
import random
from sims4.resources import Types # type: ignore
from tuning_ids import Constants

OCCULT_TRAITS = {'Fairy': Constants.FAIRY, 'Mermaid': Constants.MERMAID, 'Witch': Constants.WITCH, 'Werewolf': Constants.WEREWOLF, 'Vampire': Constants.VAMPIRE}

def randomize_occults(output_func):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    all_sims = services.sim_info_manager().get_all()
    
    for sim_info in all_sims:
        if sim_info.is_child_or_younger: continue
        
        is_occult = any(sim_info.has_trait(trait_manager.get(tid)) for tid in OCCULT_TRAITS.values() if trait_manager.get(tid))
        
        if not is_occult and random.random() > 0.5:
            choice_name = random.choice(list(OCCULT_TRAITS.keys()))
            trait = trait_manager.get(OCCULT_TRAITS[choice_name])
            if trait:
                sim_info.add_trait(trait)
                if OCCULT_TRAITS[choice_name] == Constants.FAIRY:
                    sim_info.add_trait(trait_manager.get(Constants.FAIRY_FYAE))
                output_func(f"Converted {sim_info.first_name} to {choice_name}")