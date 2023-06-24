from collections import UserDict
from datetime import date
import re


class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        if self.value:
            try:
                date_parts = self.value.split(".")
                if len(date_parts) == 3:
                    day = int(date_parts[0])
                    month = int(date_parts[1])
                    year = int(date_parts[2])
                    date(year, month, day)
                else:
                    self.value = None
            except ValueError:
                self.value = None


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def remove_phone(self):
        self.phone = None

    def edit_phone(self, new_phone):
        self.phone = Phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        record_str = f"Name: {self.name.value}\n"
        if self.phone.value:
            record_str += f"Phone: {self.phone.value}\n"
        if self.birthday.value:
            record_str += f"Birthday: {self.birthday.value}\n"
        return record_str

    def days_to_birthday(self):
        if self.birthday.value:
            today = date.today()
            birthday_date_parts = self.birthday.value.split(".")
            birthday_day = int(birthday_date_parts[0])
            birthday_month = int(birthday_date_parts[1])
            next_birthday = date(today.year, birthday_month, birthday_day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, birthday_month, birthday_day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None


class AddressBook(UserDict):
    def __init__(self, n=5):
        super().__init__()
        self.n = n

    def iterator(self):
        records = list(self.data.values())
        for i in range(0, len(records), self.n):
            yield records[i:i + self.n]

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def search_records(self, search_params):
        results = []
        for record in self.data.values():
            match = True
            for param_name, param_value in search_params.items():
                field_value = getattr(record, param_name).value
                if field_value != param_value:
                    match = False
                    break
            if match:
                results.append(str(record))
        return results


contacts = AddressBook()


def add_contact_to_addressbook(name, phone):
    if name in contacts:
        record = contacts[name]
        record.add_phone(phone)
        return "Phone number added successfully"
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        return "Contact added successfully"


def add_contact_to_addressbook_with_birthday(name, phone, birthday):
    if name in contacts:
        record = contacts[name]
        record.add_phone(phone)
        record.add_birthday(birthday)
        return "Номер телефону та дата народження успішно додані"
    else:
        record = Record(name)
        record.add_phone(phone)
        record.add_birthday(birthday)
        contacts.add_record(record)
        return "Контакт успішно доданий"


def change_phone_in_addressbook(name, new_phone):
    if name in contacts:
        record = contacts[name]
        record.edit_phone(new_phone)
        return "Phone number updated successfully"
    else:
        return "Contact not found"


def get_phone_from_addressbook(name):
    if name in contacts:
        record = contacts[name]
        return str(record)
    else:
        return "Contact not found"


def show_all_contacts():
    contact_list = []
    if contacts:
        for chunk in contacts.iterator():
            contact_list.append("\n".join(str(record) for record in chunk))
    return contact_list


def is_valid_phone(phone):
    # Шаблон для перевірки номера телефону: +380 та 9 будь-яких цифр
    pattern = r'^\+380\d{9}$'
    return re.match(pattern, phone) is not None


def is_valid_birthday(birthday):
    # Перевірка формату дати (ДД.ММ.РРРР)
    pattern = r"\d{2}\.\d{2}\.\d{4}"
    if not re.match(pattern, birthday):
        return False

    # Розділення дати на день, місяць та рік
    day, month, year = birthday.split(".")

    # Перевірка коректності дня
    if not (1 <= int(day) <= 31):
        return False

    # Перевірка коректності місяця
    if not (1 <= int(month) <= 12):
        return False

    # Перевірка коректності року
    if not (1900 <= int(year) <= 2100):
        return False

    return True


def main():
    while True:
        command = input("Enter a command: ")
        output = process_command(command)
        print(output)
        if output == "Good bye!":
            break


def process_command(command):
    command = command.lower()

    if command == "hello":
        return "How can I help you?"

    if command == "show all":
        return "\n".join(show_all_contacts())

    elif command.startswith("add"):
        args = command[4:].split()
        if len(args) == 2:
            name, phone = args
            if not is_valid_phone(phone):
                return "Некоректний номер телефону. Будь ласка, введіть коректний номер у форматі +380XXXXXXXXX."
            return add_contact_to_addressbook(name, phone)
        elif len(args) == 3:
            name, phone, birthday = args
            if not is_valid_phone(phone):
                return "Некоректний номер телефону. Будь ласка, введіть коректний номер у форматі +380XXXXXXXXX."
            if not is_valid_birthday(birthday):
                return "Некоректна дата народження. Будь ласка, введіть коректну дату у форматі ДД.ММ.РРРР."
            return add_contact_to_addressbook_with_birthday(name, phone, birthday)
        else:
            return "Некоректна команда. Будь ласка, введіть add, ім'я контакту, номер телефону та, за бажанням, дату народження."

    elif command.startswith("change"):
        args = command[7:].split()
        if len(args) == 2:
            name, new_phone = args
            if not is_valid_phone(new_phone):
                return "Некоректний номер телефону. Будь ласка, введіть коректний номер у форматі +380XXXXXXXXX."
            return change_phone_in_addressbook(name, new_phone)
        else:
            return "Некоректна команда. Будь ласка, введіть change, ім'я контакту та новий номер телефону."

    elif command.startswith("phone"):
        name = command[6:].strip()
        return get_phone_from_addressbook(name)

    elif command.startswith("remove"):
        name = command[7:].strip()
        if name in contacts:
            contacts.remove_record(name)
            return "Контакт успішно видалений"
        else:
            return "Контакт не знайдено"

    elif command.startswith("when birthday"):
        name = command[14:].strip()
        if name:
            if name in contacts:
                record = contacts[name]
                days = record.days_to_birthday()
                if days is not None:
                    if days == 0:
                        return "Сьогодні день народження!"
                    else:
                        return f"До наступного дня народження залишилося {days} днів."
                else:
                    return "У цього контакту не вказана дата народження."
            else:
                return "Контакт не знайдено"
        else:
            return "Будь ласка, введіть ім'я контакту після команди 'when birthday'."
        
    elif command == "help":
        return "Доступні команди:\n- hello\n- show all\n- add <ім'я> <номер телефону> [дата народження]\n- change <ім'я> <новий номер телефону>\n- phone <ім'я>\n- remove <ім'я>\n- find <параметри пошуку>\n- help\n- exit"

    elif command.lower() in ["good bye", "close", "exit"]:
        return "Good bye!"

    else:
        return "Некоректна команда. Введіть 'help' для отримання довідки."


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
