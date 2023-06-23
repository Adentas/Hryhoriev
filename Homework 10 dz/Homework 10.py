from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, phone, new_phone):
        for p in self.phones:
            if p.value == phone:
                p.value = new_phone
                break

    def __str__(self):
        record_str = f"Name: {self.name.value}\n"
        if self.phones:
            record_str += "Phones:\n"
            for phone in self.phones:
                record_str += f"- {phone.value}\n"
        return record_str


class AddressBook(UserDict):
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


def change_phone_in_addressbook(name, new_phone):
    if name in contacts:
        record = contacts[name]
        old_phone = record.phones[0].value if record.phones else None
        if old_phone:
            record.edit_phone(old_phone, new_phone)
            return "Phone number updated successfully"
        else:
            return "No phone number found for the contact"
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
        for record in contacts.values():
            contact_list.append(str(record))
    return contact_list


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
        name, phone = command[4:].split()
        return add_contact_to_addressbook(name, phone)

    elif command.startswith("change"):
        args = command.split()[1:]
        if len(args) == 2:
            name, new_phone = args
            return change_phone_in_addressbook(name, new_phone)
        else:
            return "Invalid command. Please provide name and new phone."

    elif command.startswith("phone"):
        name = command[6:]
        return get_phone_from_addressbook(name)

    elif command in ["good bye", "close", "exit"]:
        return "Good bye!"

    else:
        return "Invalid command. Please try again."


if __name__ == "__main__":
    main()
