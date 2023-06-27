from collections import UserDict
from datetime import date
import re


class Field:
    def __init__(self, value=None):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass

# Клас Phone має статичний метод для перевірки валідності номера телефону
class Phone:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def is_valid_phone(phone):
        # Перевірка валідності формату номера телефону
        # Наприклад, формат: +380XXXXXXXXX
        if phone.startswith("+380") and len(phone) == 13:
            return True
        return False


class Birthday:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def is_valid_birthday(birthday):
        # Перевірка валідності формату дати народження
        # Наприклад, формат: DD.MM.YYYY
        parts = birthday.split(".")
        if len(parts) == 3:
            day, month, year = parts
            if len(day) == 2 and len(month) == 2 and len(year) == 4:
                return True
        return False


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, new_phone):
        if self.phones:
            self.phones[0] = Phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return (next_birthday - today).days
        return None

    def __str__(self):
        phones_str = "\n".join(phone.value for phone in self.phones)
        if self.birthday:
            return f"Name: {self.name}\nPhones:\n{phones_str}\nBirthday: {self.birthday.value}"
        else:
            return f"Name: {self.name}\nPhones:\n{phones_str}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def __contains__(self, name):
        return name in self.data

    def __iter__(self):
        return iter(self.data.values())

    def iterator(self):
        for i in range(0, len(self.data), self.n):
            yield list(self.data.values())[i:i + self.n]

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


# Функція для додавання контакту до адресної книги
def add_contact_to_addressbook(name, phone):
    if name in contacts:
        record = contacts[name]
        record.add_phone(phone)
        return "Номер телефону додано успішно"
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        return "Контакт додано успішно"


# Функція для додавання дати народження до контакту в адресній книзі
def add_birthday_to_addressbook(name, birthday):
    if name in contacts:
        record = contacts[name]
        if Birthday.is_valid_birthday(birthday):
            record.add_birthday(birthday)
            return "Дата народження додана успішно"
        else:
            return "Некоректний формат дати народження. Використовуйте формат DD.MM.YYYY"
    else:
        return "Контакт не знайдено"


# Функція для зміни номера телефону контакту в адресній книзі
def change_phone_in_addressbook(name, new_phone):
    if name in contacts:
        if Phone.is_valid_phone(new_phone):
            record = contacts[name]
            record.edit_phone(new_phone)
            return "Номер телефону змінено успішно"
        else:
            return "Некоректний формат номера телефону. Використовуйте формат +380XXXXXXXXX"
    else:
        return "Контакт не знайдено"


# Функція для отримання номера телефону за ім'ям контакту
def get_phone_from_addressbook(name):
    if name in contacts:
        record = contacts[name]
        if record.phones:
            return record.phones[0].value
        else:
            return "У контакта немає номера телефону"
    else:
        return "Контакт не знайдено"


def main():
    print("Привіт! Я твій помічник у керуванні адресною книгою.")

    while True:
        command = input("Введіть команду: ")
        output = process_command(command)
        print(output)
        if output == "Good bye!":
            break


def process_command(command):
    if command.lower() == "hello":
        return "Привіт! Я твій помічник у керуванні адресною книгою."

    elif command.lower() == "show all":
        if contacts:
            return "\n\n".join(str(record) for record in contacts)
        else:
            return "Адресна книга порожня"

    elif command.startswith("add"):
        params = command[4:].strip().split(" ")
        if len(params) >= 2:
            name = params[0]
            phone = params[1]
            birthday = None
            if len(params) == 3:
                birthday = params[2]
            if Birthday.is_valid_birthday(birthday):
                return add_birthday_to_addressbook(name, birthday)
            else:
                return add_contact_to_addressbook(name, phone)
        else:
            return "Некоректна команда. Введіть 'add', ім'я контакту та номер телефону."

    elif command.startswith("change"):
        params = command[7:].strip().split(" ")
        if len(params) == 2:
            name = params[0]
            new_phone = params[1]
            if Phone.is_valid_phone(new_phone):
                return change_phone_in_addressbook(name, new_phone)
            else:
                return "Некоректна команда. Використовуйте формат 'change', ім'я контакту та новий номер телефону."
        else:
            return "Некоректна команда. Використовуйте формат 'change', ім'я контакту та новий номер телефону."

    elif command.startswith("phone"):
        params = command[6:].strip().split(" ")
        if len(params) == 1:
            name = params[0]
            return get_phone_from_addressbook(name)
        else:
            return "Некоректна команда. Використовуйте формат 'phone' і ім'я контакту."

    elif command.lower() in ["good bye", "close", "exit"]:
        return "Good bye!"

    else:
        return "Некоректна команда. Спробуйте ще раз."


if __name__ == "__main__":
    main()
