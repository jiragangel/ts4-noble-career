import sims4.commands  # type: ignore
# Import our new modules
from celebrity_service import increase_sim_celebrity
import career_service
import social_service
import household_service
import occult_service

@sims4.commands.Command('increase_celebrity_by_lastname', command_type=sims4.commands.CommandType.Live)
def _increase_celebrity_by_lastname(last_name: str = '',  fame_points: int = 1000, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    increase_sim_celebrity(last_name, fame_points, output)

@sims4.commands.Command('add_noble_career', command_type=sims4.commands.CommandType.Live)
def _add_noble_career(last_name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    career_service.add_noble_career_to_sim(last_name, output)

@sims4.commands.Command('find_partner', command_type=sims4.commands.CommandType.Live)
def _find_partner(first_name: str = '', last_name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    social_service.find_and_marry_partner(first_name, last_name, output)

@sims4.commands.Command('set_all_household_funds', command_type=sims4.commands.CommandType.Cheat)
def _set_all_household_funds(amount: int = 100000, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    household_service.update_all_household_funds(amount, output)

@sims4.commands.Command('randomize_new_occults', command_type=sims4.commands.CommandType.Live)
def _randomize_new_occults(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    occult_service.randomize_occults(output)

@sims4.commands.Command('cleanup_hybrids', command_type=sims4.commands.CommandType.Live)
def _cleanup_hybrids(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    occult_service.cleanup_hybrids(output)

@sims4.commands.Command('jira.help', command_type=sims4.commands.CommandType.Cheat)
def _jira_help(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("Commands: increase_celebrity_by_lastname, add_noble_career, find_partner, set_all_household_funds, randomize_new_occults, promote_all_nobles")

@sims4.commands.Command('promote_all_nobles', command_type=sims4.commands.CommandType.Live)
def _promote_all_nobles(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    career_service.promote_noble_dynasty(output)

@sims4.commands.Command('hellow', command_type=sims4.commands.CommandType.Live)
def _say_hello(_connection=None):
    sims4.commands.CheatOutput(_connection)('Hello World')

@sims4.commands.Command('rename_married_sims', command_type=sims4.commands.CommandType.Live)
def _randomize_townie_marriage_names(_connection=None):
    household_service.randomize_townie_marriage_names(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('rename_unmarried_sims', command_type=sims4.commands.CommandType.Live)
def _rename_unmarried_sims(_connection=None):
    household_service.randomize_townie_unmarried(sims4.commands.CheatOutput(_connection))