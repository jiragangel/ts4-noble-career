import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants

def find_and_marry_partner(first_name: str, last_name: str, output_func):
    sim_manager = services.sim_info_manager()
    target_sim = next((s for s in sim_manager.get_all() if s.first_name.lower() == first_name.lower() and s.last_name.lower() == last_name.lower()), None)
    
    if not target_sim:
        output_func("Target Sim not found.")
        return

    match_sim = None
    for sim in sim_manager.get_all():
        if sim.sim_id != target_sim.sim_id and sim.age == target_sim.age and sim.gender != target_sim.gender:
            # Check for existing partner bit (15825)
            if not any(bit.guid64 == Constants.PARTNER for bit in sim.relationship_tracker.get_all_bits()):
                match_sim = sim
                break

    if match_sim:
        bit_manager = services.get_instance_manager(Types.RELATIONSHIP_BIT)
        stat_manager = services.get_instance_manager(Types.STATISTIC)
        
        # Add Bits and Scores
        target_sim.relationship_tracker.add_relationship_bit(match_sim.sim_id, bit_manager.get(Constants.PARTNER)) # Married
        target_sim.relationship_tracker.add_relationship_bit(match_sim.sim_id, bit_manager.get(Constants.HAS_MET)) # Has Met
        target_sim.relationship_tracker.set_relationship_score(match_sim.sim_id, 100, stat_manager.get(Constants.FRIENDSHIP)) # Friendship
        target_sim.relationship_tracker.set_relationship_score(match_sim.sim_id, 100, stat_manager.get(Constants.ROMANCE)) # Romance
        output_func(f"Matched {target_sim.first_name} with {match_sim.first_name}")