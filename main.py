import sims4.commands  # type: ignore
# Import our new modules
from celebrity_service import increase_fame_for_nobles
import career_service
import social_service
import services # type: ignore
import household_service
import occult_service
import genetics
import utils
from utils import get_dynasty, get_full_name

with open("C:/Users/jiraa/Documents/Electronic Arts/The Sims 4/Mods/jira_mod/output.txt", "w") as f:
    print("File cleared")

@sims4.commands.Command('increase_fame_for_nobles', command_type=sims4.commands.CommandType.Live)
def _increase_fame_for_nobles(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    increase_fame_for_nobles(output)

@sims4.commands.Command('randomize_nobles', command_type=sims4.commands.CommandType.Live)
def _randomize_nobles(name: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    career_service.randomize_nobles(name, output)

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
    output('increase_fame_for_nobles')
    output('randomize_nobles')
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
    output('rename_dynasty_members')

@sims4.commands.Command('hellow', command_type=sims4.commands.CommandType.Live)
def _say_hello(_connection=None):
    sims4.commands.CheatOutput(_connection)('Hello World')

@sims4.commands.Command('rename_married_sims', command_type=sims4.commands.CommandType.Live)
def _randomize_townie_marriage_names(_connection=None):
    household_service.rename_married_sims(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('rename_unmarried_sims', command_type=sims4.commands.CommandType.Live)
def _rename_unmarried_sims(_connection=None):
    household_service.randomize_townie_unmarried(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('remove_aliens', command_type=sims4.commands.CommandType.Live)
def _remove_aliens(_connection=None):
    occult_service.remove_aliens(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('set_occult_per_family', command_type=sims4.commands.CommandType.Live)
def _set_occult_per_family(_connection=None):
    occult_service.set_occult_per_family(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('cleanup_hustler', command_type=sims4.commands.CommandType.Live)
def _cleanup_hustler():
    utils.cleanup_hustler()

@sims4.commands.Command('rename_dynasty_members', command_type=sims4.commands.CommandType.Live)
def _rename_dynasty_members(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info_manager = services.sim_info_manager()

    for sim_info in sim_info_manager.get_all():
        dynasty = get_dynasty(sim_info)

        if not dynasty is None:
            output(f"Dynasty found for {get_full_name(sim_info)}: {dynasty}")
            sim_info.last_name = dynasty

@sims4.commands.Command('iterate_sims_on_active_lot', command_type=sims4.commands.CommandType.Live)
def _iterate_sims_on_active_lot(_connection=None):
    career_service.iterate_sims_on_active_lot(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('promote_to_queen_king', command_type=sims4.commands.CommandType.Live)
def _promote_to_queen_king(_connection=None):
    genetics.promote_to_queen_king(sims4.commands.CheatOutput(_connection))

@sims4.commands.Command('count_households', command_type=sims4.commands.CommandType.Live)
def count_households_command(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    
    # Access the household manager service
    household_manager = services.household_manager()
    if household_manager is None:
        output("Household manager not found.")
        return

    # Get all households (returns a list/generator of Household objects)
    households = household_manager.get_all()
    
    output(f"Total Households: {len(households)}")
    
    for household in households:
        # household.name gives the household name
        # household.member_count gives the total Sims count in the household
        name = household.name
        size = household.household_size

        if size >= 8:
            output(f"Household: {name} | Size: {size}")
            utils.write_to_log(f"Household: {name} | Size: {size}")