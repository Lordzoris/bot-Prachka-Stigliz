import sqlite3
from _datetime import *
import datetime
from typing import Union


async def reg_connect(tid, name, number):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, name, number) VALUES (?, ?, ?);", (tid, name, number)
    )
    conn.commit()
    conn.close()


async def reg_test(tid):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    select_id = cursor.execute("SELECT id FROM users;").fetchall()
    conn.close()
    for user in select_id:
        if user[0] == str(tid):
            return True
    return False


async def get_count():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(time) FROM zapis;")
    conn.close()


async def add_record_tomorrow(time, tid) -> Union[bool, int]:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    select_id = cursor.execute(
        "SELECT id FROM zapis where id like ?;", (tid,)
    ).fetchall()
    if not select_id:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        day = str(tomorrow.day).zfill(2)  # добавляем нуль, если день меньше 10
        month = str(tomorrow.month).zfill(2)  # добавляем нуль, если месяц меньше 10
        date_str = f"{day}.{month}"
        cursor.execute(
            "INSERT INTO zapis (time, date, id) VALUES (?, ?, ?);",
            (time, date_str, tid),
        )
        conn.commit()
        conn.close()
        return 1
    for id in select_id:
        if id[0] == str(tid):
            conn.close()
            return 2
        else:
            counts = cursor.execute(
                "SELECT COUNT(*) FROM zapis WHERE time LIKE ?;", (time,)
            ).fetchone()
            if counts[0] >= 5:
                conn.close()
                return 0
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            day = str(tomorrow.day).zfill(2)  # добавляем нуль, если день меньше 10
            month = str(tomorrow.month).zfill(2)  # добавляем нуль, если месяц меньше 10
            date_str = f"{day}.{month}"
            cursor.execute(
                "INSERT INTO zapis (time, date, id) VALUES (?, ?, ?);",
                (time, date_str, tid),
            )
            conn.commit()
            conn.close()
            return 1


async def add_record_today(time, tid) -> Union[bool, int]:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    select_id = cursor.execute(
        "SELECT id FROM zapis where id like ?;", (tid,)
    ).fetchall()
    if not select_id:
        today = datetime.date.today()
        day = str(today.day).zfill(2)  # добавляем нуль, если день меньше 10
        month = str(today.month).zfill(2)  # добавляем нуль, если месяц меньше 10
        date_str = f"{day}.{month}"
        cursor.execute(
            "INSERT INTO zapis (time, date, id) VALUES (?, ?, ?);",
            (time, date_str, tid),
        )
        conn.commit()
        conn.close()
        return 1
    for id in select_id:
        if id[0] == str(tid):
            conn.close()
            return 2
        else:
            counts = cursor.execute(
                "SELECT COUNT(*) FROM zapis WHERE time LIKE ?;", (time,)
            ).fetchone()
            if counts[0] >= 5:
                conn.close()
                return 0
            today = datetime.date.today()
            day = str(today.day).zfill(2)  # добавляем нуль, если день меньше 10
            month = str(today.month).zfill(2)  # добавляем нуль, если месяц меньше 10
            date_str = f"{day}.{month}"
            cursor.execute(
                "INSERT INTO zapis (time, date, id) VALUES (?, ?, ?);",
                (time, date_str, tid),
            )
            conn.commit()
            conn.close()
            return 1


async def check_record_user(tid):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    select_count = cursor.execute(
        "SELECT COUNT(*) FROM zapis WHERE id LIKE ?;", (tid,)
    ).fetchone()
    check = ""
    for selects in select_count:
        if str(selects) == "0":
            conn.close()
            return False
        if str(selects) == "1":
            select = cursor.execute(
                "SELECT time, id FROM zapis WHERE id like ?;", (tid,)
            ).fetchall()
            conn.close()
            for id in select:
                if id[1] == str(tid):
                    check = id[0]
                return check


async def delete_record(tid):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM zapis WHERE id = ?;", (tid,))
    conn.commit()
    conn.close()


async def list_wash():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    select = cursor.execute(
        "SELECT name, number, time, date FROM users, zapis WHERE users.id = zapis.id ORDER BY time ASC;"
    ).fetchall()
    conn.close()
    schedule = {}
    if not select:
        return "Нет записей"
    for item in select:
        name, num, interval, date = item
        if date not in schedule:
            schedule[date] = {}
        if interval not in schedule[date]:
            schedule[date][interval] = []
        schedule[date][interval].append((name, num))

    result = ""
    for date in sorted(schedule.keys()):
        result += f"\n{date}\n"
        for time in sorted(schedule[date].keys()):
            result += f"В {time} записаны:\n"
            for name, num in schedule[date][time]:
                result += f"{name} {num}\n"
    return result


async def change_number(tid, number):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET number = ?  WHERE id LIKE ?;", (number, tid,)
    )
    conn.commit()
    conn.close()


async def delete_old_record():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    date_of_deletion = datetime.date.today()
    formated_date = str(date_of_deletion.day).zfill(2)
    formated_mounth = str(date_of_deletion.month).zfill(2)
    date_formated = f'{formated_date},{formated_mounth}'
    cursor.execute(
        "DELETE FROM zapis WHERE date < ?;",
        (date_formated,)
    )
    conn.commit()
    conn.close()
