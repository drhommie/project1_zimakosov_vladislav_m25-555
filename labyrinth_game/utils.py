from labyrinth_game.constants import ROOMS, PUZZLE_REWARD


def describe_current_room(game_state):
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    # Название комнаты
    print(f"== {current_room.upper()} ==")

    # Описание комнаты
    print(room_data["description"])

    # Список видимых предметов
    if room_data["items"]:
        print("Заметные предметы:", ", ".join(room_data["items"]))

    # Доступные выходы
    print("Выходы:", ", ".join(room_data["exits"].keys()))

    # Наличие загадки
    if room_data["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    room_id = game_state["current_room"]
    puzzle = ROOMS[room_id]["puzzle"]

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle

    print(question)

    user_answer = input("Ваш ответ: ").strip()

    if user_answer.lower() == str(answer).lower():

        print("Верно!")

        ROOMS[room_id]["puzzle"] = None

        if "score" not in game_state:
            game_state["score"] = 0
        game_state["score"] += PUZZLE_REWARD
    else:
  
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):

    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if "treasure_chest" not in room["items"]:
        print("Сундук уже открыт.")
        return

    inventory = game_state["player_inventory"]

    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    answer = input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()
    if answer != "да":
        print("Вы отступаете от сундука.")
        return

    puzzle = room.get("puzzle")
    if puzzle is None:
        print("Кода нет.")
        return

    question = puzzle[0]
    correct_answer = puzzle[1]

    print(question)
    user_code = input("Ваш ответ: ").strip().lower()

    if user_code == str(correct_answer).lower():
        print("Замок щёлкнул. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код.")

# labyrinth_game/utils.py
def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
