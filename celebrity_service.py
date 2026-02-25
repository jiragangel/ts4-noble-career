import services # type: ignore
from sims4.resources import Types # type: ignore
from tuning_ids import Constants

def increase_sim_celebrity(last_name: str, fame_points: int, output_func):
    try:
        sim_manager = services.sim_info_manager()
        for sim_info in sim_manager.get_all():
            if (sim_info.last_name.lower() == last_name.lower() and sim_info.is_teen_or_older) or (last_name == '' and sim_info.is_teen_or_older):
                commodity_manager = services.get_instance_manager(Types.STATISTIC)
                fame_commodity = commodity_manager.get(Constants.FAME) # Fame ID

                if fame_commodity is None:
                    output_func("Fame commodity not found. Is Get Famous installed?")
                    return

                commodity_tracker = sim_info.commodity_tracker
                if commodity_tracker is not None:
                    commodity_tracker.add_value(fame_commodity, fame_points)
                    output_func(f"{sim_info.first_name} {sim_info.last_name}'s celebrity increased!")
    except Exception as e:
        output_func(f"Error: {e}")