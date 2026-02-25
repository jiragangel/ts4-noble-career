import services # type: ignore
import sims4.commands # type: ignore
import random
from sims4.resources import Types # pyright: ignore[reportMissingImports]

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

@sims4.commands.Command('randomize_new_occults', command_type=sims4.commands.CommandType.Live)
def _randomize_new_occults(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    
    # Define primary Occult Trait IDs
    OCCULT_TRAITS = {
        'Fairy': 433287,
        'Mermaid': 199043,
        'Witch': 213050,     # Spellcaster
        'Werewolf': 289780,
        'Vampire': 149527,
    }

    try:
        trait_manager = services.get_instance_manager(Types.TRAIT)
        if trait_manager is None:
            output("Error: Could not access Trait Manager. Game state may be unstable.")
            return False

        all_sims = services.sim_info_manager().get_all()
        count = 0
        skipped = 0
        errors = 0
        
        for sim_info in all_sims:
            try:
                output(f"starting for {sim_info.first_name} {sim_info.last_name}")
                # 2. Check if Sim is already an Occult using the Trait list
                # This is the most reliable way to avoid 'No module' errors
                is_already_occult = False
                for tid in OCCULT_TRAITS.values():
                    t_tuning = trait_manager.get(tid)
                    if t_tuning and sim_info.has_trait(t_tuning):
                        is_already_occult = True
                        break

                if is_already_occult:
                    skipped += 1
                    output(f"{sim_info.first_name} {sim_info.last_name} is already an occult")
                    continue

                if sim_info.is_child_or_younger:
                    output(f"{sim_info.first_name} {sim_info.last_name} is a child")
                    continue

                # 3. Randomization Logic (50% chance to convert)
                if random.random() > 0.5:
                    choice_name = random.choice(list(OCCULT_TRAITS.keys()))
                    target_id = OCCULT_TRAITS[choice_name]
                    
                    output(f"{sim_info.first_name} {sim_info.last_name} will have {choice_name}")

                    # 4. Defensive Tuning Check (Handles missing DLC)
                    new_trait = trait_manager.get(target_id)
                    output(f"{sim_info.first_name} {sim_info.last_name} will have trait added")
                    if new_trait is not None:
                        sim_info.add_trait(new_trait)
                        count += 1
                        if new_trait == 433287:
                            sim_info.add_trait(trait_manager.get(414620))
                    else:
                        # This happens if the user doesn't own the specific pack
                        pass 

            except Exception as e:
                # Catch errors for individual Sims so one bad Sim doesn't break the whole loop
                output(f"Failed to process Sim {sim_info.first_name}: {e}")
                errors += 1
                continue

        output(f"Finished! Converted {count} humans. Skipped {skipped} existing occults.")
        if errors > 0:
            output(f"Note: {errors} Sims encountered errors during processing.")
        
        return True

    except Exception as e:
        # Catch major system-level errors
        output(f"Critical Script Error: {str(e)}")
        return False
    