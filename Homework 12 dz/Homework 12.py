from collections import UserDict
from datetime import date
import re
import pickle


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


class Phone:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def is_valid_phone(phone):
        if re.match(r"^\+\d{1,3}\d{9}$", phone):
            return True
        return False


class Birthday:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def is_valid_birthday(birthday):
        if re.match(r"^\d{2}\.\d{2}\.\d{4}$", birthday):
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


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def search_records(self, search_string):
        results = []
        for record in self.data.values():
            if re.search(search_string, record.name.value, re.IGNORECASE):
                results.append(str(record))
            else:
                for phone in record.phones:
                    if re.search(search_string, phone.value):
                        results.append(str(record))
                        break
        return results

    def save(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load(self, filename):
        try:
            with open(filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass


contacts = AddressBook()


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


def change_phone_in_addressbook(name, new_phone):
    if name in contacts:
        if Phone.is_valid_phone(new_phone):
            record = contacts[name]
            record.edit_phone(new_phone)
            return "Номер телефону змінено успішно"
        else:
            return "Некоректний формат номера телефону. Використовуйте формат +XXXXXXXXXXX"
    else:
        return "Контакт не знайдено"


def get_phone_from_addressbook(name):
    if name in contacts:
        record = contacts[name]
        if record.phones:
            return record.phones[0].value
        else:
            return "У контакта немає номера телефону"
    else:
        return "Контакт не знайдено"


def search_addressbook(query):
    results = contacts.search_records(query)
    if results:
        return "\n\n".join(results)
    else:
        return "Нічого не знайдено"


def save_addressbook(filename):
    contacts.save(filename)
    return "Адресну книгу збережено"


def load_addressbook(filename):
    contacts.load(filename)
    return "Адресну книгу завантажено"


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
            return "\n\n".join(str(record) for record in contacts.values())
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

    elif command.startswith("search"):
        query = command[7:].strip()
        return search_addressbook(query)

    elif command.startswith("save"):
        filename = command[5:].strip()
        return save_addressbook(filename)

    elif command.startswith("load"):
        filename = command[5:].strip()
        return load_addressbook(filename)

    elif command.lower() in ["good bye", "close", "exit"]:
        return "Good bye!"

    else:
        return "Некоректна команда. Спробуйте ще раз."


if __name__ == "__main__":
    main()
