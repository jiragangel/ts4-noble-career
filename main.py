import services # type: ignore
import sims4.commands # type: ignore
import random
from sims4.resources import Types # pyright: ignore[reportMissingImports]
from sims.sim_info_types import Gender # type: ignore
import os
from datetime import datetime

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

@sims4.commands.Command('jira.rtmn', command_type=sims4.commands.CommandType.Live)
def _randomize_townie_marriage_names(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    
    # 1. Path Setup
    log_file_path = "REPLACE_PATH_HERE"
    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    except Exception as e:
        output(f"FileSystem Error: {str(e)}")
        return False

    # 2. Name Lists
    surnames = ["Auremont","Valcour","Beauchamp","Montclair","Devereux","Rochefort","Bellamont","Fontainebleau","Charlemont","Villeneuve","Saintclair","D’Aurelle","Lafayette","Montpellier","Argenvale","Marceau","Delacroix","Beauregard","Clairmont","Vallencourt","Montreval","Duvalier","Saint-Roche","Lavellemont","Aurelmont","Belcour","Montferrand","Carlemont","Valenbourg","Rosenwald","Von Albrecht","Von Eisenberg","Von Falkenrath","Von Silvermark","Von Winterfeld","Von Greifen","Hohenberg","Hohenwald","Schwarzenfels","Edelstein","Kronenberg","Lichtenwald","Sturmfels","Adelbrecht","Kaiserwald","Falkenstein","Rosenfeld","Windermark","Goldschmidt","Silbermann","Nordheim","Wolfsberg","Steinmark","Bergwald","Ehrenfels","Grünwald","Himmelreich","Di Laurentis","De Medoria","Bellavigna","Rosenthalis","Montesanti","Valentori","Caravelli","San Aurelio","Marcellini","Altamonte","Venturius","Castiglione","Bellatorre","D’Argento","Serenelli","Lucentio","Vittorani","Fontanelli","De Valois","De Montfort","De Lorraine","De Navarre","De Bourmont","De Rochebrune","De Clairvaux","De Saint-Mer","Von Ravensbruck","Von Nighthelm","Von Solisburg","Von Helmswald","Von Eisenhart"]
    female_royal_names = ["Adelina","Aurelia","Beatrice","Celestine","Charlotte","Clarissa","Clementine","Cordelia","Daphne","Eleanor","Elisabeth","Emmeline","Evangeline","Florence","Genevieve","Helena","Isabella","Josephine","Juliana","Leonora","Lucinda","Marguerite","Matilda","Ophelia","Penelope","Seraphina","Theodora","Valentina","Veronica","Victoria","Arabella","Anastasia","Antonia","Bianca","Camilla","Cassandra","Catalina","Constanza","Dorothea","Elvira","Estella","Francesca","Gabriella","Georgiana","Giselle","Henrietta","Iolanthe","Isolde","Jacqueline","Lavinia","Leontine","Lisette","Magdalena","Marceline","Mirabella","Octavia","Philomena","Rosalind","Sabina","Tatiana","Viola","Wilhelmina","Zenobia","Amalia","Bernadette","Cosima","Delphine","Eudora","Faustina","Imogen","Juliette","Katarina","Lorraine","Marcella","Natalia","Oriana","Persephone","Renata","Solenne","Theresia","Ursula","Violetta","Yvette","Zara","Alessandra","Brigitta","Carolina","Desdemona","Eleanora","Felicity","Guinevere","Honoria","Isabella-Marie","Julianna","Klementina","Lucienne","Margot","Noemi","Odette","Pauline","Querida","Rowena","Sigrid","Tallulah","Ulrika","Viviana","Winifred","Xanthe","Yolanda","Zelina","Auriane","Belladonna","Corinna","Dominique","Euphemia","Fiametta","Griselda","Hortensia","Isadora","Justina","Karolina","Leticia","Monique","Nerissa","Olympia","Prudence","Rosamund","Silvia","Tiberia","Vespera","Wilma","Xenia","Ysaline","Zita","Adrianna","Brunhilda","Cecilia","Delfina","Elodie","Fabienne","Galatea","Helene","Ilona","Jessamine","Katriel","Lucasta","Mireille","Nadine","Ottilie","Petronella","Roxanne","Selena","Thalia","Ursa","Verena","Wisteria","Xylia","Ysadora","Zophia"]
    male_royal_names = ["Adrian","Alaric","Alexander","Ambrose","Anselm","Arthur","Augustus","Benedict","Cassius","Cedric","Constantine","Cornelius","Darius","Dominic","Edmund","Edward","Emilian","Felix","Frederick","Gabriel","Hadrian","Henry","Hugo","Ignatius","Isidore","Jasper","Julius","Laurence","Leopold","Lucian","Magnus","Marcellus","Maximilian","Nathaniel","Octavian","Percival","Quentin","Raphael","Sebastian","Theodore","Valerian","Victor","Wilhelm","Xavier","Zacharias","Aurelian","Bernard","Caius","Demetrius","Elias","Florian","Gareth","Horatio","Ibrahim","Julian","Konrad","Leonard","Matthias","Nicholas","Orlando","Philip","Roderick","Stefan","Tiberius","Ulrich","Vladimir","Wenceslas","Xerxes","Yorick","Zephyr","Alphonse","Balthazar","Casimir","Desmond","Erasmus","Ferdinand","Gregory","Hector","Inigo","Justinian","Karl","Lysander","Marius","Nikolai","Oberon","Pascal","Reinhardt","Silvester","Tristan","Ulysses","Valentino","Wolfgang","Xanthus","Yvain","Zoltan","Anatole","Boris","Clement","Dorian","Emerson","Fabian","Gerard","Havelock","Icarus","Jerome","Kallias","Lorenzo","Mortimer","Nestor","Oswald","Prospero","Rufus","Simeon","Thaddeus","Urban","Virgil","Wallace","Xylon","Yuri","Zeno","Abelard","Bertrand","Cyril","Draven","Evander","Francis","Gustav","Harlan","Ivor","Jacques","Killian","Lucius","Mordecai","Neville","Olivier","Phineas","Remington","Stellan","Titus","Vaughn","Wilfred","Ximeno","Yago","Zoran"]
    
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"\n--- Session Start: {datetime.now()} ---\n")
        
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
                        
                        new_female_fn = random.choice(female_royal_names)
                        new_male_fn = random.choice(male_royal_names)

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
                        log_file.write(log_msg + "\n")

                except Exception as e:
                    log_file.write(f"ERR Sim {sim_info.sim_id}: {str(e)}\n")
                    error_count += 1

            final_msg = f"Completed. Updated {count} couples. Errors: {error_count}"
            output(final_msg)
            log_file.write(final_msg + "\n")
            return True

        except Exception as e:
            output(f"Crash: {str(e)}")
            log_file.write(f"FATAL: {str(e)}\n")
            return False