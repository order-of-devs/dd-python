from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    name: str
    type: str
    type Capabilities = set[Capability]

    @staticmethod
    def skill(name: str) -> Capability:
        return Capability(name, "SKILL")

    @staticmethod
    def permission(name: str) -> Capability:
        return Capability(name, "PERMISSION")

    @staticmethod
    def asset(asset: str) -> Capability:
        return Capability(asset, "ASSET")

    @staticmethod
    def skills(skills: str) -> Capabilities:
        return {Capability.skill(s) for s in skills}

    @staticmethod
    def assets(assets: str) -> Capabilities:
        return {Capability.asset(a) for a in assets}

    @staticmethod
    def permissions(permissions: str) -> Capabilities:
        return {Capability.permission(p) for p in permissions}

    def is_of_type(self, _type: str) -> bool:
        return self.type == _type
