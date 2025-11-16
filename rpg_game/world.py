"""Game world and helpers."""

from __future__ import annotations

from typing import Dict

from .models import Enemy, Item, Location, Player


def potion_effect(player: Player) -> str:
    healed = player.heal(10)
    return f"HPを{healed}回復した！"


WORLD: Dict[str, Location] = {
    "village": Location(
        key="village",
        name="静かな村",
        description="小さな村。南には古い森が広がっている。",
        neighbors={"south": "forest", "east": "lake"},
        item=Item("回復薬", "HPを10回復する", potion_effect),
    ),
    "forest": Location(
        key="forest",
        name="霧の森",
        description="木々の間に奇妙な囁きが聞こえる。",
        neighbors={"north": "village", "east": "ruins"},
        enemy=Enemy("ゴブリン", max_hp=12, attack=4, defense=1, reward_exp=6, loot="ゴブリンの牙"),
    ),
    "lake": Location(
        key="lake",
        name="月光の湖",
        description="水面が月光を跳ね返し幻想的に輝いている。",
        neighbors={"west": "village", "south": "ruins"},
    ),
    "ruins": Location(
        key="ruins",
        name="古代遺跡",
        description="崩れた石柱と古い碑文が残る。強い魔物の気配がする。",
        neighbors={"west": "forest", "north": "lake"},
        enemy=Enemy("影の騎士", max_hp=18, attack=6, defense=3, reward_exp=12, loot="古代の護符"),
    ),
}


def describe_location(location_key: str) -> str:
    location = WORLD[location_key]
    location.visited = True
    description = f"\n== {location.name} ==\n{location.description}\n"
    actions = []
    if location.item:
        actions.append(f"地面に{location.item.name}が落ちている。拾うには 'take' を入力。")
    if location.enemy and location.enemy.is_alive:
        actions.append(f"{location.enemy.name} が現れた！")
    if not actions:
        actions.append("特に何も起こらない。")
    return description + "\n".join(actions)


def pickup_item(player: Player, location_key: str) -> str:
    location = WORLD[location_key]
    if location.item is None:
        return "拾える物はない。"
    item = location.item
    location.item = None
    player.inventory.append(item.name)
    if item.name == "回復薬":
        player.potions += 1
    return f"{item.name}を手に入れた！ {item.description}"
