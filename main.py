import services # type: ignore
import sims4.commands # type: ignore
from sims.sim_info_types import Gender # type: ignore

@sims4.commands.Command('increase_celebrity_by_lastname', command_type=sims4.commands.CommandType.Live)
def increase_celebrity_by_lastname(last_name: str, fame_points: int = 1000, _connection=None):
    output = sims4.commands.CheatOutput(_connection)

    try:
        sim_manager = services.sim_info_manager()
        target_sim = None

        # Find sim by last name
        for sim_info in sim_manager.get_all():
            if sim_info.last_name.lower() == last_name.lower():
                target_sim = sim_info

                # Get Fame commodity from Commodity Manager
                commodity_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
                fame_commodity = commodity_manager.get(188229)

                if fame_commodity is None:
                    output("Fame commodity not found. Is Get Famous installed?")
                    return

                commodity_tracker = target_sim.commodity_tracker
                if commodity_tracker is None:
                    output("Sim has no commodity tracker.")
                    return

                # Increase fame
                commodity_tracker.add_value(fame_commodity, fame_points)

                output(f"{target_sim.first_name} {target_sim.last_name}'s celebrity level increased by {fame_points} points!")

    except Exception as e:
        output("An unexpected error occurred while increasing celebrity level.")
        sims4.log.exception("CelebrityCheat", "Error in increase_celebrity_by_lastname", exc=e)

@sims4.commands.Command('add_noble_career', command_type=sims4.commands.CommandType.Live)
def _add_noble_career(last_name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)

    try:
        # 1. Find the Sim
        search_last = last_name.strip().lower()

        for sim in services.sim_info_manager().get_all():
            if (sim.last_name.lower() == search_last and sim.is_teen_or_older) or (not last_name and sim.is_teen_or_older):
                sim_info = sim

                output(f"Processing {sim.first_name} {sim.last_name}")

                # 2. Get the Career Tuning
                noble_career_id = 466304
                instance_manager = services.get_instance_manager(sims4.resources.Types.CAREER)
                noble_career_tuning = instance_manager.get(noble_career_id)

                # 3. Final Execution (The fix for the 'self' error)
                # We manually instantiate the career object to provide 'self'
                # and add it directly to the tracker, skipping the 'has_career' check.
                new_career_instance = noble_career_tuning(sim_info)
                sim_info.career_tracker.add_career(new_career_instance)
                
                output(f"Success! {sim.first_name} {sim.last_name} has been added to the Noble career.")
        
        for sim in services.sim_info_manager().get_all():
            if (sim.last_name.lower() == search_last and sim.is_teen_or_older) or (not last_name and sim.is_teen_or_older):
                try:
                    sim_info = sim
                    output(f"Promote {sim_info.first_name} {sim_info.last_name}")
                    next(iter((sim_info.career_tracker.careers.values()))).promote()
                    output(f"Succesful promote {sim_info.first_name} {sim_info.last_name} 1")
                except Exception as e:
                    output('error')

        return True

    except Exception as e:
        output(f"Script Error: {str(e)}")
        return False

@sims4.commands.Command('hellow', command_type=sims4.commands.CommandType.Live)
def sayhello(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Hello World')

@sims4.commands.Command('find_partner', command_type=sims4.commands.CommandType.Live)
def _find_partner(first_name: str = '', last_name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    
    if not first_name or not last_name:
        output("Usage: find_partner [First] [Last]")
        return False

    try:
        # 1. Find the Target Sim
        target_sim = None
        for sim in services.sim_info_manager().get_all():
            if sim.first_name.lower() == first_name.lower() and sim.last_name.lower() == last_name.lower():
                target_sim = sim
                break
                
        if target_sim is None:
            output(f"Error: Target Sim {first_name} {last_name} not found.")
            return False

        # 2. Match Criteria
        target_age = target_sim.age
        target_gender = target_sim.gender
        match_sim = None

        # 3. Search for a Match
        for sim in services.sim_info_manager().get_all():
            if sim.sim_id == target_sim.sim_id:
                continue
            if sim.age == target_age and sim.gender != target_gender:
                # NEW: Check if this Sim already has a partner bit with ANYONE
                has_partner = False
                for bit in sim.relationship_tracker.get_all_bits():
                    if bit.guid64 == 15825:
                        has_partner = True
                        break
                
                if not has_partner:
                    match_sim = sim
                    break

        if match_sim is None:
            output(f"Could not find a matching Sim of age {target_age} and opposite sex.")
            return False

        # 4. Get Managers (Using STATISTIC for the tracks)
        bit_manager = services.get_instance_manager(sims4.resources.Types.RELATIONSHIP_BIT)
        # FIX: Relationship Tracks are found in the STATISTIC manager
        stat_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)

        # 5. Define Tuning IDs
        partner_bit_id = 15825 # Married
        has_met_bit_id = 15803
        friend_track_id = 16650 # Friendship
        romance_track_id = 16651 # Romance

        partner_bit = bit_manager.get(partner_bit_id)
        has_met_bit = bit_manager.get(has_met_bit_id)
        friend_track = stat_manager.get(friend_track_id)
        romance_track = stat_manager.get(romance_track_id)

        if not all([partner_bit, friend_track, romance_track]):
            output("Error: Could not load Relationship Bit or Statistic Tracks.")
            return False

        # 6. Apply Relationship Bit and Max Scores (100)
        # This creates the relationship connection
        target_sim.relationship_tracker.add_relationship_bit(match_sim.sim_id, partner_bit)
        target_sim.relationship_tracker.add_relationship_bit(match_sim.sim_id, has_met_bit)
        
        # This fills the bars
        target_sim.relationship_tracker.set_relationship_score(match_sim.sim_id, 100, friend_track)
        target_sim.relationship_tracker.set_relationship_score(match_sim.sim_id, 100, romance_track)

        output(f"Success! {target_sim.first_name} and {match_sim.first_name} are now a Power Couple.")
        return True

    except Exception as e:
        output(f"Script Error: {str(e)}")
        return False

@sims4.commands.Command('set_all_household_funds', command_type=sims4.commands.CommandType.Cheat)
def set_all_household_funds(amount: int = 100000, _connection=None):
    output = sims4.commands.CheatOutput(_connection)

    output("Command started...")  # debug line

    try:
        household_manager = services.household_manager()

        if household_manager is None:
            output("Error: Household manager not found.")
            return

        count = 0

        for household in household_manager.get_all():
            try:
                if household is None:
                    continue

                output(f"Current fund {household.funds.money}")
                
                # for attr in dir(household.funds):
                #     try:
                #         value = getattr(household.funds, attr)
                #         output(f"{attr}: {type(value)}")
                #     except Exception as e:
                #         output(f"{attr}: <error reading> {e}")
                household.funds.add(1000000, 1)
                output(f"New fund {household.funds.money}")
                count += 1

            except Exception as e:
                output(f"Failed for one household: {e}")

        output(f"Done! Updated {count} households to {amount} simoleons.")

    except Exception as e:
        output(f"Critical error: {e}")

@sims4.commands.Command('jira.help', command_type=sims4.commands.CommandType.Cheat)
def set_all_household_funds(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("def increase_celebrity_by_lastname(last_name: str, fame_points: int = 1000, _connection=None)")
    output("def _add_noble_career(last_name: str = '', _connection=None)")
    output("def sayhello(_connection=None)")
    output("def _find_partner(first_name: str = '', last_name: str = '', _connection=None)")
    output("def set_all_household_funds(amount: int = 100000, _connection=None)")

