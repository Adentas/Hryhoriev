import datetime

# Створення об'єктів datetime для днів народження користувачів
birthday1 = datetime.date(1990, 5, 15)
birthday2 = datetime.date(1985, 5, 20)
birthday3 = datetime.date(1992, 5, 25)
birthday4 = datetime.date(1990, 5, 16)
birthday5 = datetime.date(1985, 5, 21)
birthday6 = datetime.date(1992, 5, 26)
birthday7 = datetime.date(1990, 5, 17)
birthday8 = datetime.date(1985, 5, 22)
birthday9 = datetime.date(1992, 5, 28)
birthday10 = datetime.date(1992, 5, 23)

# Створення списка користувачів з їх іменами та днями народження
users = [
    {'name': 'John', 'birthday': birthday1},
    {'name': 'Alice', 'birthday': birthday2},
    {'name': 'Michael', 'birthday': birthday3},
    {'name': 'Johnny', 'birthday': birthday4},
    {'name': 'Alex', 'birthday': birthday5},
    {'name': 'Denis', 'birthday': birthday6},
    {'name': 'Illya', 'birthday': birthday7},
    {'name': 'Roman', 'birthday': birthday8},
    {'name': 'Victory', 'birthday': birthday9},
    {'name': 'Jane', 'birthday': birthday10}
]

def get_birthdays_per_week(users):
    today = datetime.datetime.now().date()
    current_week_start = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=0)
    print(current_week_start)
    current_week_end = current_week_start + datetime.timedelta(days=6)
    print(current_week_end)
    
    weekday = None
    
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    birthdays_per_week = {weekday: [] for weekday in weekdays}

    for user in users:
        name = user['name']
        birthday = user['birthday']
        
        birthday = datetime.date(2023, birthday.month, birthday.day)  # Видалення року
        print(birthday)
        
        if current_week_start <= birthday and birthday <= current_week_end:
            print("+")
            if birthday.weekday() >= 5:  # Якщо день народження на вихідних
                weekday = weekdays[0]  # Привітання в понеділок
            else:
                weekday = weekdays[birthday.weekday()]
            birthdays_per_week[weekday].append(name)

    print(birthdays_per_week)
    
    for weekday, birthdays in birthdays_per_week.items():
        if birthdays:
            print(f"{weekday}: {', '.join(birthdays)}")

get_birthdays_per_week(users)
