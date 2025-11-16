"""Game mechanics such as battles and actions."""

from __future__ import annotations

import random
from typing import Callable, Optional

from .models import Enemy, Player


def calculate_damage(attacker: Player | Enemy, defender: Player | Enemy, rng: Optional[random.Random] = None) -> int:
    rng = rng or random.Random()
    base = attacker.attack - defender.defense // 2
    variance = rng.randint(-2, 2)
    damage = max(1, base + variance)
    return damage


def perform_attack(attacker: Player | Enemy, defender: Player | Enemy, rng: Optional[random.Random] = None) -> int:
    damage = calculate_damage(attacker, defender, rng)
    defender.take_damage(damage)
    return damage


def use_potion(player: Player) -> str:
    if player.potions <= 0:
        return "ポーションを持っていない。"
    player.potions -= 1
    healed = player.heal(12)
    return f"ポーションを使った。HPを{healed}回復。"


def award_loot(player: Player, enemy: Enemy) -> str:
    loot_text = ""
    if enemy.loot:
        player.inventory.append(enemy.loot)
        loot_text = f" {enemy.loot}を手に入れた。"
    return loot_text


def resolve_victory(player: Player, enemy: Enemy) -> str:
    player.gain_experience(enemy.reward_exp)
    leveled = player.level_up()
    loot_text = award_loot(player, enemy)
    if leveled:
        level_text = f" レベル{player.level}に上がった！"
    else:
        level_text = ""
    return f"{enemy.name}を倒した！経験値{enemy.reward_exp}を得た。{loot_text}{level_text}".strip()


class BattleResult(Exception):
    """Raised to escape nested loops when the battle ends."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def battle(player: Player, enemy: Enemy, input_func: Callable[[str], str] = input, rng: Optional[random.Random] = None) -> str:
    rng = rng or random.Random()
    print(f"{enemy.name}との戦闘が始まった！")
    while player.is_alive and enemy.is_alive:
        print(f"\n{player.name} HP:{player.hp}/{player.max_hp}  Lv:{player.level}  ポーション:{player.potions}")
        print(f"{enemy.name} HP:{enemy.hp}/{enemy.max_hp}")
        command = input_func("行動を選択 [attack/skill/potion/run]: ").strip().lower()
        if command in {"attack", "a"}:
            damage = perform_attack(player, enemy, rng)
            print(f"{player.name}の攻撃！{enemy.name}に{damage}のダメージ。")
        elif command in {"skill", "s"}:
            damage = perform_attack(player, enemy, rng) + 2
            enemy.take_damage(2)
            print(f"スキル発動！追加ダメージを与え、合計{damage}のダメージ。")
        elif command in {"potion", "p"}:
            print(use_potion(player))
        elif command in {"run", "r"}:
            if rng.random() < 0.5:
                print("逃げることに成功した！")
                raise BattleResult("戦闘から離脱した。")
            print("逃げられなかった！")
        else:
            print("不明なコマンド。")
            continue

        if not enemy.is_alive:
            message = resolve_victory(player, enemy)
            raise BattleResult(message)

        damage = perform_attack(enemy, player, rng)
        print(f"{enemy.name}の攻撃！{player.name}は{damage}のダメージを受けた。")
        if not player.is_alive:
            raise BattleResult("力尽きてしまった……。ゲームオーバー。")

    return ""
