from math import floor, sin

from labyrinth_game.constants import (
    COMMANDS,
    DEFAULT_SCORE,
    DEFAULT_STEPS,
    EVENT_FIND,
    EVENT_NOISE,
    EVENT_PROBABILITY,
    EVENT_TRAP,
    HELP_PAD,
    PUZZLE_REWARD,
    RANDOM_EVENT_OFFSET,
    RANDOM_EVENT_TYPES,
    ROOMS,
    TRAP_DEATH_THRESHOLD,
)


def describe_current_room(game_state):
    """Печатает название, описание, предметы и выходы текущей комнаты."""
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    print(f"== {current_room.upper()} ==")
    print(room_data["description"])

    if room_data["items"]:
        print("Заметные предметы:", ", ".join(room_data["items"]))

    print("Выходы:", ", ".join(room_data["exits"].keys()))

    if room_data["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Задаёт загадку комнаты и обрабатывает ответ; при успехе выдаёт награду."""
    room_id = game_state["current_room"]
    puzzle = ROOMS[room_id]["puzzle"]

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    print(question)

    user_answer = input("Ваш ответ: ").strip().lower()
    correct = str(answer).strip().lower()

    acceptable = {correct}
    if correct == "10":
        acceptable.add("десять")

    if user_answer in acceptable:
        print("Верно!")
        ROOMS[room_id]["puzzle"] = None
        reward = PUZZLE_REWARD
        if room_id == "library":
            reward = PUZZLE_REWARD * 2
        game_state["score"] = game_state.get("score", DEFAULT_SCORE) + reward
    else:
        print("Неверно. Попробуйте снова.")
        if room_id == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Пробует открыть сундук ключом или кодом; при успехе завершает игру победой."""
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

    question, correct_answer = puzzle
    print(question)
    user_code = input("Ваш ответ: ").strip().lower()

    if user_code == str(correct_answer).lower():
        print("Замок щёлкнул. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код.")


def show_help(commands=COMMANDS):
    """Печатает список доступных команд и их краткое описание."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd.ljust(HELP_PAD)} - {desc}")


def pseudo_random(seed, modulo):
    """Детерминированный псевдослучайный генератор: int в диапазоне [0, modulo)."""
    x = sin(seed * 12.9898) * 43758.5453
    frac = x - floor(x)
    return floor(frac * modulo)


def trigger_trap(game_state):
    """Срабатывание ловушки: потеря предмета или риск поражения без инвентаря."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        seed = game_state.get("steps_taken", DEFAULT_STEPS)
        idx = pseudo_random(seed, len(inventory))
        lost_item = inventory.pop(idx)
        print("Вы потеряли:", lost_item)
        return

    seed = game_state.get("steps_taken", DEFAULT_STEPS)
    roll = pseudo_random(seed, EVENT_PROBABILITY)
    if roll < TRAP_DEATH_THRESHOLD:
        print("Поражение. Игра окончена.")
        game_state["game_over"] = True
    else:
        print("Вы уцелели.")


def random_event(game_state):
    """С низкой вероятностью запускает одно из случайных событий при перемещении."""
    seed = game_state.get("steps_taken", DEFAULT_STEPS)

    if pseudo_random(seed, EVENT_PROBABILITY) != 0:
        return

    event_type = pseudo_random(seed + RANDOM_EVENT_OFFSET, RANDOM_EVENT_TYPES)

    current_room = game_state["current_room"]
    inventory = game_state["player_inventory"]

    if event_type == EVENT_FIND:
        print("Вы находите на полу монетку.")
        ROOMS[current_room]["items"].append("coin")

    elif event_type == EVENT_NOISE:
        print("Вы слышите шорох.")
        if "sword" in inventory:
            print("Вы достали меч — он отпугнул существо.")

    elif event_type == EVENT_TRAP:
        if current_room == "trap_room" and "torch" not in inventory:
            print("Здесь опасно.")
            trigger_trap(game_state)
