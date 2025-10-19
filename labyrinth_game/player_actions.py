from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    """Печатает содержимое инвентаря игрока либо сообщает, что он пуст."""
    inventory = game_state["player_inventory"]
    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")


def get_input(prompt="> "):
    """Возвращает строку, введённую пользователем; на Ctrl+C/D возвращает 'quit'."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещает игрока в соседнюю комнату по направлению, если выход существует."""
    current = game_state["current_room"]
    exits = ROOMS[current]["exits"]

    if direction in exits:
        next_room = exits[direction]

        if next_room == "treasure_room":
            if "rusty_key" in game_state["player_inventory"]:
                print(
                    "Вы используете найденный ключ, чтобы открыть путь "
                    "в комнату сокровищ."
                )
                game_state["current_room"] = next_room
                game_state["steps_taken"] += 1
                describe_current_room(game_state)
                random_event(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

        game_state["current_room"] = next_room
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Перемещает игрока в соседнюю комнату по направлению, если выход существует."""
    room = game_state["current_room"]
    if item_name in ROOMS[room]["items"]:
        game_state["player_inventory"].append(item_name)
        ROOMS[room]["items"].remove(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Использует предмет из инвентаря; эффекты зависят от типа предмета."""
    inventory = game_state["player_inventory"]
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return
    if item_name == "torch":
        print("Стало светлее.")
    elif item_name == "sword":
        print("Вы чувствуете уверенность.")
    elif item_name == "bronze_box":
        print("Вы открыли шкатулку.")
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Внутри был ржавый ключ.")
    else:
        print("Вы не знаете, как использовать этот предмет.")
