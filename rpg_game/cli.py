"""Command line interface for the RPG game."""

from __future__ import annotations

import random
from typing import Callable

from . import engine
from .models import Enemy, Player
from .world import WORLD, describe_location, pickup_item


HELP_TEXT = """コマンド一覧:
  north/south/east/west: 移動
  take: アイテムを拾う
  status: ステータス確認
  help: このヘルプ
  quit: ゲーム終了
"""


def _choose_enemy(location_key: str) -> Enemy | None:
    location = WORLD[location_key]
    enemy = location.enemy
    if enemy and enemy.is_alive:
        return enemy
    return None


def _move(location_key: str, direction: str) -> str:
    location = WORLD[location_key]
    try:
        return location.neighbors[direction]
    except KeyError as exc:
        raise ValueError("その方向へは進めない。") from exc


def _print_status(player: Player, location_key: str) -> str:
    location = WORLD[location_key]
    return (
        f"{player.name} HP:{player.hp}/{player.max_hp} Lv:{player.level} Exp:{player.experience}\n"
        f"現在地: {location.name}  所持品: {', '.join(player.inventory) if player.inventory else 'なし'}\n"
        f"ポーション: {player.potions}"
    )


def run_game(input_func: Callable[[str], str] = input) -> None:
    print("*** 物語の始まり ***")
    name = input_func("勇者の名前を入力してください: ").strip() or "勇者"
    player = Player(name=name, max_hp=20, attack=5, defense=2)
    location_key = "village"
    rng = random.Random()

    while True:
        print(describe_location(location_key))
        enemy = _choose_enemy(location_key)
        if enemy:
            try:
                engine.battle(player, enemy, input_func=input_func, rng=rng)
            except engine.BattleResult as result:
                print(result.message)
                if not player.is_alive:
                    break
                if "ゲームオーバー" in result.message:
                    break
                if not enemy.is_alive:
                    pass
                if result.message == "戦闘から離脱した。":
                    location_key = "village"
                    print("安全な村へと戻った。")
            if not player.is_alive:
                break

        command = input_func("次の行動は？ (helpで一覧): ").strip().lower()
        if command in {"help", "h"}:
            print(HELP_TEXT)
            continue
        if command in {"status", "st"}:
            print(_print_status(player, location_key))
            continue
        if command in {"take", "t"}:
            print(pickup_item(player, location_key))
            continue
        if command in {"quit", "q"}:
            print("冒険を終えました。またの挑戦を待っています！")
            break

        if command in {"north", "south", "east", "west", "n", "s", "e", "w"}:
            direction = {
                "n": "north",
                "s": "south",
                "e": "east",
                "w": "west",
            }.get(command, command)
            try:
                new_location = _move(location_key, direction)
                location_key = new_location
                continue
            except ValueError as err:
                print(str(err))
                continue

        print("そのコマンドは理解できない。")


if __name__ == "__main__":
    run_game()
