import sims4.commands  # type: ignore
# Import our new modules
from celebrity_service import increase_sim_celebrity
import career_service
import social_service
import household_service
import occult_service
import town_service
import genetics
import services
from utils import display_all_attributes # type: ignore

with open("C:/Users/jiraa/Downloads/jira_mod/output.txt", "w") as f:
    print("File cleared")

@sims4.commands.Command('increase_celebrity_by_lastname', command_type=sims4.commands.CommandType.Live)
def _increase_celebrity_by_lastname(last_name: str = '',  fame_points: int = 1000, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    increase_sim_celebrity(last_name, fame_points, output)

@sims4.commands.Command('add_noble_career', command_type=sims4.commands.CommandType.Live)
def _add_noble_career(last_name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    career_service.add_noble_career_to_sim(last_name, output)

@sims4.commands.Command('add_random_career', command_type=sims4.commands.CommandType.Live)
def _add_random_career(last_name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    career_service.add_random_career(output)

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
    output('increase_celebrity_by_lastname')
    output('add_noble_career')
    output('add_random_career')
    output('find_partner')
    output('set_all_household_funds')
    output('randomize_new_occults')
    output('cleanup_hybrids')
    output('jira.help')
    output('promote_all_nobles')
    output('hellow')
    output('rename_married_sims')
    output('rename_unmarried_sims')
    output('create_noble_per_town')
    output('remove_aliens')

@sims4.commands.Command('promote_all_nobles', command_type=sims4.commands.CommandType.Live)
def _promote_noble_dynasty(count: int, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    career_service.promote_noble_dynasty(output, count)

@sims4.commands.Command('hellow', command_type=sims4.commands.CommandType.Live)
def _say_hello(_connection=None):
    sims4.commands.CheatOutput(_connection)('Hello World')

@sims4.commands.Command('rename_married_sims', command_type=sims4.commands.CommandType.Live)
def _randomize_townie_marriage_names(_connection=None):
    household_service.randomize_townie_marriage_names(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('rename_unmarried_sims', command_type=sims4.commands.CommandType.Live)
def _rename_unmarried_sims(_connection=None):
    household_service.randomize_townie_unmarried(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('create_noble_per_town', command_type=sims4.commands.CommandType.Live)
def _create_noble_per_town(_connection=None):
    town_service.create_noble_per_town(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('remove_aliens', command_type=sims4.commands.CommandType.Live)
def _remove_aliens(_connection=None):
    occult_service.remove_aliens(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('cleanup_kingdom_manager', command_type=sims4.commands.CommandType.Live)
def _cleanup_kingdom_manager(_connection=None):
    kingdom_manager = services.kingdom_service()
    display_all_attributes(kingdom_manager)

@sims4.commands.Command('inherit_nobility', command_type=sims4.commands.CommandType.Live)
def _inherit_nobility(_connection=None):
    genetics.inherit_nobility(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('set_occult_per_family', command_type=sims4.commands.CommandType.Live)
def _set_occult_per_family(_connection=None):
    occult_service.set_occult_per_family(sims4.commands.CheatOutput(_connection))