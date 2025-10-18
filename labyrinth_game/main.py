#!/usr/bin/env python3

from labyrinth_game import player_actions, utils

from labyrinth_game.constants import ROOMS

from labyrinth_game.utils import (
    describe_current_room, 
    solve_puzzle, 
    attempt_open_treasure,
)

from labyrinth_game.player_actions import (
    get_input,
    show_inventory,
    move_player,
    take_item,
    use_item,
)

def process_command(game_state, command):
    parts = command.split()
    verb = parts[0].lower() if parts else ""
    arg = parts[1] if len(parts) > 1 else ""

    if verb in ('north','south','east','west'):
        move_player(game_state, verb)
        return   

    match verb:
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "go":
            move_player(game_state, arg)
        case "take":
            take_item(game_state, arg)
        case "use":
            use_item(game_state, arg)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            game_state["game_over"] = True
        case _:
             print('Неизвестная команда.')

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
        process_command(game_state, command)

if __name__ == "__main__":
    main()

