from utils import check_bit_on_sim, display_all_attributes, get_full_name
import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants
from sims.sim_info_types import Species # type: ignore

def get_partner(target_sim, output_func):
    sim_manager = services.sim_info_manager()
    bit_manager = services.get_instance_manager(Types.RELATIONSHIP_BIT)
    match_sim = None
    for sim in sim_manager.get_all():
        if sim.sim_id != target_sim.sim_id and sim.age == target_sim.age and sim.gender != target_sim.gender and not check_bit_on_sim(sim, target_sim, bit_manager.get(Constants.BROKEN_UP)):
            # Check for existing partner bit (15825)
            if not any((bit.guid64 == Constants.PARTNER or bit.guid64 == Constants.SECRET_LOVER) for bit in sim.relationship_tracker.get_all_bits()) and get_full_name(sim) != 'Grim Reaper':
                match_sim = sim
                break
            else:
                output_func(f"Not a match {get_full_name(sim)} for {get_full_name(target_sim)}")

    if match_sim:
        stat_manager = services.get_instance_manager(Types.STATISTIC)

        relationship_bit = bit_manager.get(Constants.PARTNER);
        if any((bit.guid64 == Constants.PARTNER or bit.guid64 == Constants.MARRIED) for bit in target_sim.relationship_tracker.get_all_bits()):
            relationship_bit = bit_manager.get(Constants.SECRET_LOVER);
        
        # Add Bits and Scores
        target_sim.relationship_tracker.add_relationship_bit(match_sim.sim_id, relationship_bit) # Married
        target_sim.relationship_tracker.add_relationship_bit(match_sim.sim_id, bit_manager.get(Constants.HAS_MET)) # Has Met
        target_sim.relationship_tracker.set_relationship_score(match_sim.sim_id, 100, stat_manager.get(Constants.FRIENDSHIP)) # Friendship
        target_sim.relationship_tracker.set_relationship_score(match_sim.sim_id, 100, stat_manager.get(Constants.ROMANCE)) # Romance
        output_func(f"Matched {get_full_name(target_sim)} with {get_full_name(match_sim)}")
    else:
        output_func(f"No match found for {get_full_name(target_sim)}")

def find_and_marry_partner(first_name: str, last_name: str, output_func):
    try:
        sim_manager = services.sim_info_manager()
        target_sim = next((s for s in sim_manager.get_all() if s.first_name.lower() == first_name.lower() and s.last_name.lower() == last_name.lower()), None)
        
        if not target_sim:
            output_func("Target Sim not found. Will iterate all teens")
            for sim_info in services.sim_info_manager().get_all():
                if sim_info.is_teen and sim_info.species == Species.HUMAN and not any((bit.guid64 == Constants.PARTNER) for bit in sim_info.relationship_tracker.get_all_bits()):
                    get_partner(sim_info, output_func)
        else:
            get_partner(target_sim, output_func)

        
    except Exception as e:
        output_func(f"Error {e}")
