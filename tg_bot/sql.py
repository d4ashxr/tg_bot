import psycopg2
from psycopg2 import OperationalError, sql
import sys
from create_table import creating


def daily_clothes_choise(weather_info):
    res_arr = {}
    wind_prot, rain_prot = 0, 0
    maxi_temp, mini_temp, rain_str, max_wind = weather_info[1], weather_info[2], weather_info[3], weather_info[4]
    print(weather_info,max_wind, "NEN")
    if max_wind >= 8:
        wind_prot = 1
    if rain_str != "По прогнозу дождя не будет.":
        rain_prot = 1

    conn = None

    try:
        conn = psycopg2.connect(
            host='localhost',  # Замените на адрес вашего хоста
            user='postgres',  # Замените на пользователя вашей базы данных
            password='6936',  # Замените на пароль вашей базы данных
            database='closhes',  # Замените на название вашей базы данных
            port=5432  # По умолчанию PostgreSQL использует порт 5432
        )
        print("Подключение успешно установлено.")
        if conn == None:
            creating(conn)
        queries = {
            "Верх:": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Верх' 
                AND min_temp <= {maxi_temp} 
                AND max_temp >= {mini_temp} 
            """,
            "Низ:": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Низ' 
                AND min_temp <= {maxi_temp} 
                AND max_temp >= {mini_temp} 
            """,
            "Верхняя одежда:": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Верхняя одежда' 
                AND min_temp <= {maxi_temp} 
                AND max_temp >= {mini_temp} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """,
            "Комплект:": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Комплект' 
                AND min_temp <= {maxi_temp} 
                AND max_temp >= {mini_temp} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """,
            "Обувь:": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Обувь' 
                AND min_temp <= {maxi_temp} 
                AND max_temp >= {mini_temp} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """,
            "Аксессуары:": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Аксессуары' 
                AND min_temp <= {maxi_temp} 
                AND max_temp >= {mini_temp} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """
        }

        for key, query in queries.items():
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                res_arr[key] = [row[0] for row in results] if results else ["нет ничего, что могло бы пригодится"]

    except OperationalError as e:
        print(f"Ошибка при работе с базой данных: {e}")

    finally:
        if conn:
            conn.close()
            print("Соединение закрыто.")
    return res_arr

