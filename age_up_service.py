import sims4.log  # type: ignore
from sims.sim_info import SimInfo  # type: ignore

import household_service

logger = sims4.log.Logger("NobleCareerAgeUp")


def _move_young_adult_after_age_up(original, self, *args, **kwargs):
    was_teen = self.is_teen
    result = original(self, *args, **kwargs)

    if was_teen and self.is_young_adult:
        try:
            household_service.move_young_adult_without_noble_parent(
                self,
                lambda message: logger.info("{}", message),
            )
        except Exception as e:
            logger.error(
                "Failed to process young adult age-up for {} {}: {}",
                self.first_name,
                self.last_name,
                e,
            )

    return result


def _install_age_up_hook():
    original = SimInfo.advance_age
    if getattr(original, "_noble_career_age_up_hook", False):
        return

    def wrapped_advance_age(self, *args, **kwargs):
        return _move_young_adult_after_age_up(original, self, *args, **kwargs)

    wrapped_advance_age._noble_career_age_up_hook = True
    SimInfo.advance_age = wrapped_advance_age


_install_age_up_hook()
