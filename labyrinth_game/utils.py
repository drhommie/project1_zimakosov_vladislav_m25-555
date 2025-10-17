from labyrinth_game.constants import ROOMS


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

