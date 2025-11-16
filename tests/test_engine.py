from rpg_game import engine
from rpg_game.models import Enemy, Player


def test_calculate_damage_respects_defense():
    player = Player(name="hero", max_hp=20, attack=5, defense=3)
    enemy = Enemy(name="slime", max_hp=10, attack=4, defense=6)
    rng = __import__("random").Random(0)
    damage = engine.calculate_damage(player, enemy, rng)
    assert damage >= 1


def test_player_levels_up_after_gain():
    player = Player(name="hero", max_hp=20, attack=5, defense=2)
    player.gain_experience(10)
    leveled = player.level_up()
    assert leveled is True
    assert player.level == 2
    assert player.max_hp == 25
