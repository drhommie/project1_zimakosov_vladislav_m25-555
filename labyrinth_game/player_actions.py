from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room

def show_inventory(game_state):
    inventory = game_state["player_inventory"]

    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    current = game_state['current_room']
    exits = ROOMS[current]['exits']

    if direction in exits:
        game_state['current_room'] = exits[direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    room = game_state['current_room']
    if item_name in ROOMS[room]['items']:
        game_state['player_inventory'].append(item_name)
        ROOMS[room]['items'].remove(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
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
