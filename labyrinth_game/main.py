#!/usr/bin/env python3

from labyrinth_game.constants import INITIAL_STEPS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    """Разбирает введённую строку и выполняет соответствующую команду."""
    line = command.strip()
    if not line:
        return

    parts = line.split(maxsplit=1)
    verb = parts[0].lower() if parts else ""
    arg = parts[1] if len(parts) > 1 else ""

    # Однословные направления (north/south/east/west)
    if verb in {"north", "south", "east", "west"}:
        move_player(game_state, verb)
        return

    match verb:
        case "go":
            if arg:
                move_player(game_state, arg.lower())
            else:
                print("Укажите направление (например: go north).")
        case "look":
            describe_current_room(game_state)
        case "take":
            if arg:
                if arg == "treasure_chest":
                    print("Вы не можете поднять сундук, он слишком тяжелый.")
                else:
                    take_item(game_state, arg)
            else:
                print("Укажите предмет (например: take torch).")
        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет (например: use torch).")
        case "inventory":
            show_inventory(game_state)
        case "solve":
            # В сокровищнице сначала пробуем открыть сундук (ключом или кодом)
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            print("Игра завершена. До встречи!")
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Введите help для списка команд.")


def main():
    """Инициализирует состояние и запускает основной игровой цикл."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": INITIAL_STEPS,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()
