"""Core dataclasses for the RPG game."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class Character:
    """Base character stats."""

    name: str
    max_hp: int
    attack: int
    defense: int
    hp: int = field(init=False)

    def __post_init__(self) -> None:
        self.hp = self.max_hp

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> int:
        actual = max(0, min(self.hp, damage))
        self.hp -= actual
        return actual

    def heal(self, amount: int) -> int:
        healed = max(0, min(self.max_hp - self.hp, amount))
        self.hp += healed
        return healed


@dataclass
class Player(Character):
    """Represents the hero controlled by the user."""

    level: int = 1
    experience: int = 0
    potions: int = 1
    inventory: List[str] = field(default_factory=list)

    def gain_experience(self, amount: int) -> None:
        self.experience += amount

    def level_up(self) -> bool:
        threshold = 10 * self.level
        if self.experience >= threshold:
            self.level += 1
            self.max_hp += 5
            self.attack += 1
            self.defense += 1
            self.hp = self.max_hp
            self.experience = 0
            return True
        return False


@dataclass
class Enemy(Character):
    reward_exp: int = 5
    loot: Optional[str] = None


@dataclass
class Item:
    name: str
    description: str
    effect: Callable[[Player], str]


@dataclass
class Location:
    key: str
    name: str
    description: str
    neighbors: Dict[str, str]
    enemy: Optional[Enemy] = None
    item: Optional[Item] = None
    visited: bool = False
