import services
import sims4.commands

@sims4.commands.Command('add_noble_career', command_type=sims4.commands.CommandType.Live)
def _add_noble_career(last_name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    
    if not last_name:
        output("Usage: add_noble_career [Last]")
        return False

    try:
        # 1. Find the Sim
        search_last = last_name.strip().lower()

        for sim in services.sim_info_manager().get_all():
            if sim.last_name.lower() == search_last and sim.is_teen_or_older:
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
            if sim.last_name.lower() == search_last and sim.is_teen_or_older:
                sim_info = sim
                output(f"Promote {sim_info.first_name} {sim_info.last_name} 0")
                next(iter((sim_info.career_tracker.careers.values()))).promote()
                output(f"Promote {sim_info.first_name} {sim_info.last_name} 1")
                next(iter((sim_info.career_tracker.careers.values()))).promote()
                output(f"Promote {sim_info.first_name} {sim_info.last_name} 2")
                next(iter((sim_info.career_tracker.careers.values()))).promote()
                output(f"Promote {sim_info.first_name} {sim_info.last_name} 3")
                next(iter((sim_info.career_tracker.careers.values()))).promote()
                output(f"Promote {sim_info.first_name} {sim_info.last_name} 4")
                next(iter((sim_info.career_tracker.careers.values()))).promote()
                output(f"Promote {sim_info.first_name} {sim_info.last_name} 5")
        
        return True

    except Exception as e:
        output(f"Script Error: {str(e)}")
        return False

@sims4.commands.Command('hellow', command_type=sims4.commands.CommandType.Live)
def sayhello(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Hello World')
