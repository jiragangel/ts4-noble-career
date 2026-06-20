import services # type: ignore
from career_service import add_noble_career_to_sim, getCareerInstance
from tuning_ids import Constants
from utils import write_to_log
from collections import defaultdict
from sims.sim_info_types import Species # type: ignore
from sims4.resources import Types # type: ignore

def list_all_regions():
    # 1. Access the Region Manager
    # This manager contains the data for every world (Willow Creek, etc.)
    region_manager = services.get_instance_manager(sims4.resources.Types.REGION)

    for region in region_manager.types.values():
        write_to_log(region)
