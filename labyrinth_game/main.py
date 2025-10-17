#!/usr/bin/env python3

from labyrinth_game import player_actions, utils

from labyrinth_game.constants import ROOMS

from labyrinth_game.utils import describe_current_room

def main():
    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = input("> ")

if __name__ == "__main__":
    main()

