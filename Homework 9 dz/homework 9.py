def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)  # Повернення повідомлення про помилку користувачеві
    return inner

contacts = {} # Словник для зберігання контактів

@input_error
def add_contact(name, phone):
    contacts[name] = phone  # Додавання контакту до словника
    return "Contact added successfully"  # Повернення підтвердження

@input_error
def change_phone(name, phone):
    if name in contacts:
        contacts[name] = phone  # Зміна номера телефону для існуючого контакту
        return "Phone number updated successfully"  # Повернення підтвердження
    else:
        return "Contact not found"  # Повернення повідомлення, якщо контакт не знайдено
    
@input_error
def show_phone(name):
    if name in contacts:
        return contacts[name]  # Повернення номера телефону
    else:
        return "Contact not found"  # Повернення повідомлення, якщо контакт не знайдено

def show_all_contacts():
    if contacts:
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    else:
        print("No contacts found")

def main():
    contacts = {}  # Словник для збереження контактів

    while True:
        command = input("Enter a command: ")

        if command.lower() == "hello":
            print("How can I help you?")
        elif command.lower().startswith("add"):
            # Розбиття рядка команди на ім'я та номер телефону
            name, phone = command[4:].split()
            result = add_contact(name, phone)
            print(result)
        elif command.lower().startswith("change"):
            # Розбиття рядка команди на ім'я та номер телефону
            name, phone = command[7:].split()
            result = change_phone(name, phone)
            print(result)
        elif command.lower().startswith("phone"):
            name = command[6:]
            result = show_phone(name)
            print(result)
        elif command.lower() == "show all":
            show_all_contacts()
        elif command.lower() in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
