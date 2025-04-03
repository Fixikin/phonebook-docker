import psycopg2
from psycopg2 import sql
import sys

# Параметры подключения к БД
DB_CONFIG = {
    "dbname": "phonebook_db",
    "user": "phonebook",
    "password": "secret",
    "host": "db"
}

def create_connection():
    """Создает соединение с БД"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        sys.exit(1)

def print_menu():
    """Выводит меню"""
    print("\nТелефонная книга")
    print("1. Показать все контакты")
    print("2. Добавить контакт")
    print("3. Изменить контакт")
    print("4. Удалить контакт")
    print("5. Поиск контакта")
    print("0. Выход")

def show_all_contacts(conn):
    """Показывает все контакты"""
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM contacts ORDER BY last_name, first_name")
            contacts = cursor.fetchall()
            if not contacts:
                print("Телефонная книга пуста.")
                return
            print("\nСписок контактов:")
            print("-" * 70)
            print("{:<3} {:<20} {:<15} {:<20} {:<10}".format(
                "ID", "ФИО", "Телефон", "Заметка", ""))
            print("-" * 70)
            for contact in contacts:
                full_name = f"{contact[1]} {contact[2]} {contact[3]}" if contact[3] else f"{contact[1]} {contact[2]}"
                print("{:<3} {:<20} {:<15} {:<20}".format(
                    contact[0], full_name[:20], contact[4], contact[5][:20] if contact[5] else ""))
    except psycopg2.Error as e:
        print(f"Ошибка при получении контактов: {e}")

def add_contact(conn):
    """Добавляет новый контакт"""
    print("\nДобавление нового контакта")
    last_name = input("Фамилия: ").strip()
    first_name = input("Имя: ").strip()
    middle_name = input("Отчество (если есть): ").strip() or None
    phone_number = input("Телефон: ").strip()
    note = input("Заметка (если есть): ").strip() or None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO contacts (last_name, first_name, middle_name, phone_number, note) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (last_name, first_name, middle_name, phone_number, note)
            )
            contact_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Контакт успешно добавлен с ID: {contact_id}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при добавлении контакта: {e}")

def update_contact(conn):
    """Изменяет существующий контакт"""
    show_all_contacts(conn)
    contact_id = input("\nВведите ID контакта для изменения: ").strip()
    if not contact_id.isdigit():
        print("Некорректный ID контакта")
        return
    # Получаем текущие данные контакта
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM contacts WHERE id = %s", (contact_id,))
            contact = cursor.fetchone()
            if not contact:
                print("Контакт с таким ID не найден")
                return
            print("\nТекущие данные контакта:")
            print(f"1. Фамилия: {contact[1]}")
            print(f"2. Имя: {contact[2]}")
            print(f"3. Отчество: {contact[3]}")
            print(f"4. Телефон: {contact[4]}")
            print(f"5. Заметка: {contact[5]}")
            # Запрашиваем новые данные
            print("\nВведите новые данные (оставьте пустым, чтобы не изменять):")
            last_name = input(f"Фамилия [{contact[1]}]: ").strip() or contact[1]
            first_name = input(f"Имя [{contact[2]}]: ").strip() or contact[2]
            middle_name = input(f"Отчество [{contact[3] or ''}]: ").strip() or contact[3]
            phone_number = input(f"Телефон [{contact[4]}]: ").strip() or contact[4]
            note = input(f"Заметка [{contact[5] or ''}]: ").strip() or contact[5]
	    #Обновляем контакт
            cursor.execute(
                "UPDATE contacts SET last_name = %s, first_name = %s, middle_name = %s, "
                "phone_number = %s, note = %s WHERE id = %s",
                (last_name, first_name, middle_name, phone_number, note, contact_id)
            )
            conn.commit()
            print("Контакт успешно обновлен")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при обновлении контакта: {e}")

def delete_contact(conn):
    """Удаляет контакт"""
    show_all_contacts(conn)
    contact_id = input("\nВведите ID контакта для удаления: ").strip()
    if not contact_id.isdigit():
        print("Некорректный ID контакта")
        return
    confirm = input(f"Вы уверены, что хотите удалить контакт с ID {contact_id}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Удаление отменено")
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
            print("Контакт успешно удален")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при удалении контакта: {e}")

def search_contact(conn):
    """Ищет контакты по имени или телефону"""
    search_term = input("\nВведите имя, фамилию или номер телефона для поиска: ").strip()
    if not search_term:
        print("Поисковый запрос не может быть пустым")
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM contacts WHERE "
                "last_name ILIKE %s OR "
                "first_name ILIKE %s OR "
                "phone_number LIKE %s "
                "ORDER BY last_name, first_name",
                (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            )
            contacts = cursor.fetchall()
            if not contacts:
                print("Контакты не найдены.")
                return
            print("\nРезультаты поиска:")
            print("-" * 70)
            print("{:<3} {:<20} {:<15} {:<20}".format(
                "ID", "ФИО", "Телефон", "Заметка"))
            print("-" * 70)
            for contact in contacts:
                full_name = f"{contact[1]} {contact[2]} {contact[3]}" if contact[3] else f"{contact[1]} {contact[2]}"
                print("{:<3} {:<20} {:<15} {:<20}".format(
                    contact[0], full_name[:20], contact[4], contact[5][:20] if contact[5] else ""))
    except psycopg2.Error as e:
        print(f"Ошибка при поиске контактов: {e}")

def main():
    conn = create_connection()
    while True:
        try:
            print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                show_all_contacts(conn)
            elif choice == "2":
                add_contact(conn)
            elif choice == "3":
                update_contact(conn)
            elif choice == "4":
                delete_contact(conn)
            elif choice == "5":
                search_contact(conn)
            elif choice == "0":
                print("Выход из программы")
                break
            else:
                print("Некорректный выбор. Попробуйте снова.")
        except EOFError:
            print("\nЗавершение работы...")
            break
        except KeyboardInterrupt:
            print("\nПриложение завершено")
            break
        input("\nНажмите Enter для продолжения...")
    conn.close()

if __name__ == "__main__":
    main()
