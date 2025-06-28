import sqlite3
import re


def sanitize_phone(phone):
    """Очищает номер телефона от лишних символов"""
    return re.sub(r'[^\d+]', '', phone)


def check_user_exists(phone):
    """Проверяет, есть ли пользователь в бд"""
    clean_phone = sanitize_phone(phone)

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT phone FROM user WHERE phone = ?
    ''', (clean_phone,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)


def add_user(name, phone):
    """Добавление пользователя в бд"""
    clean_phone = sanitize_phone(phone)

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO user (name, phone)
    VALUES (?, ?)
    ON CONFLICT(phone) DO UPDATE SET name=excluded.name
    ''', (name, clean_phone))
    conn.commit()
    conn.close()

def add_sign_up(user_id, salon_id, service_id, price, datetime):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sign_up (user, salon , service, price, datetime)
        VALUES (?, ?, ?, ?)
        ''', (user_id, salon_id, service_id, price, datetime))
    conn.commit()
    conn.close()

def get_salons():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM salons")
    salons = cursor.fetchall()
    conn.close()
    return salons

def get_services():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()
    return services