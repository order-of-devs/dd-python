from enum import Enum
from dataclasses import dataclass

from src.smartschedule.shared.capability import Capability


class SelectingPolicy(Enum):
    ALL_SIMULTANEOUSLY = 1
    ONE_OF_ALL = 2


@dataclass(frozen=True)
class CapabilitySelector:
    capabilities: Capability.Capabilities
    selecting_policy: SelectingPolicy

    @staticmethod
    def can_perform_all_at_the_time(capabilities: Capability.Capabilities):
        return CapabilitySelector(capabilities, SelectingPolicy.ALL_SIMULTANEOUSLY)

    @staticmethod
    def can_perform_one_of(capabilities: Capability.Capabilities):
        return CapabilitySelector(capabilities, SelectingPolicy.ONE_OF_ALL)

    @staticmethod
    def can_just_perform(capability: Capability):
        return CapabilitySelector({capability}, SelectingPolicy.ONE_OF_ALL)

    def can_perform(self, capabilities: Capability.Capabilities):
        if len(capabilities) == 1:
            return capabilities.issubset(self.capabilities)
        return self.selecting_policy == SelectingPolicy.ALL_SIMULTANEOUSLY and \
            capabilities.issubset(self.capabilities)
