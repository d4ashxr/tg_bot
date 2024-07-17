import psycopg2
from psycopg2 import OperationalError


def clothes_choice(weather_info):
    res_arr = {}
    wind_prot, rain_prot = 0, 0
    temperature, feels_like, condition = weather_info[1], weather_info[2], weather_info[3]

    # Условия для защиты от ветра
    if any(cond in condition.lower() for cond in ["ветренно", "ураган", "буря", "торнадо"]):
        wind_prot = 1

    # Условия для защиты от дождя и снега
    if any(cond in condition.lower() for cond in ["пасмурно", "дожд", "снег", "гроза", "морось"]):
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

        queries = {
            "Верх": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Верх' 
                AND min_temp <= {feels_like}
                AND max_temp >= {feels_like} 
            """,
            "Низ": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Низ' 
                AND min_temp <= {feels_like} 
                AND max_temp >= {feels_like} 
                AND wind_protection >= {wind_prot}
            """,
            "Верхняя одежда": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Верхняя одежда' 
                AND min_temp <= {feels_like} 
                AND max_temp >= {feels_like} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """,
            "Комплект": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Комплект' 
                AND min_temp <= {feels_like} 
                AND max_temp >= {feels_like} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """,
            "Обувь": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Обувь' 
                AND min_temp <= {feels_like} 
                AND max_temp >= {feels_like} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """,
            "Аксессуары": f"""
                SELECT item 
                FROM clothes 
                WHERE item_type = 'Аксессуары' 
                AND min_temp <= {feels_like} 
                AND max_temp >= {feels_like} 
                AND waterproof >= {rain_prot} 
                AND wind_protection >= {wind_prot}
            """
        }

        for key, query in queries.items():
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                res_arr[key] = [row[0] for row in results] if results else ["нет ничего, что могло бы пригодится"]

        print("Рекомендации по одежде успешно получены.")

    except OperationalError as e:
        print(f"Ошибка при работе с базой данных: {e}")

    finally:
        if conn:
            conn.close()
            print("Соединение закрыто.")

    return res_arr


# Тестовые данные
temperature = 14
feels_like = 20
condition = "дождливо"
humidity = 5
pressure = 8
weather_info = [(f"Температура: {temperature}°C\n"
                 f"Ощущается как: {feels_like}°C\n"
                 f"Состояние: {condition}\n"
                 f"Влажность: {humidity}%\n"
                 f"Давление: {pressure} мм рт.ст."), temperature, feels_like, condition, humidity, pressure]

# Печать результата
print(clothes_choice(weather_info))
