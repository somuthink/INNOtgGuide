__all__ = ["generate_map"]


def generate_map(user_campus, finish_campus):
    campuses = ["0 🟩", "1 🟩" ,"2 🟧", "3 🟪", "4 🟩"]

    campuses_copy = campuses

    int_user_campus = int(user_campus[:2])

    int_finish_campus = int(finish_campus[:2])

    dif = int_user_campus - int_finish_campus

    def list_process(campus):
        if campus == user_campus:
            return f"*{campus}*"
        elif campus == finish_campus:
            return f"__{campus}__"
        else:
            return str(campus)

    if dif == 0:
        return f"Вы уже находитесь в нужном кампусе"
    elif dif > 0:
        way = campuses_copy[int_finish_campus:int_user_campus + 1]
        way = "   ⏪   ".join(map(list_process, way))
        return way
    elif dif < 0:
        way = campuses_copy[int_user_campus:int_finish_campus + 1]
        way = "   ⏩   ".join(map(list_process, way))
        return way
