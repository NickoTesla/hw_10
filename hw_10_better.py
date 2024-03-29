from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value, label=None):
        super().__init__(value)
        self.label = label

    def __str__(self):
        if self.label:
            return f"{self.label}: {self.value}"
        else:
            return str(self.value)


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def remove_record(self, name):
        del self.data[name.lower()]

    def edit_record(self, name, record):
        self.data[name.lower()] = record


contacts = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Enter name and phone number separated by a space"
        except IndexError:
            return "Enter a contact name"
    return wrapper


@input_error
def add_contact(command):
    name, phone = command.split()
    contacts.add_record(Record(name, phone))
    return f"Contact {name} added"


@input_error
def change_contact(command):
    name, phone = command.split()
    record = contacts.data[name.lower()]
    record.edit_phone(phone)
    contacts.edit_record(name, record)
    return f"Phone number for {name} changed"


@input_error
def get_phone(command):
    name = command.lower()
    record = contacts.data[name]
    phones = ", ".join(str(phone) for phone in record.phones)
    return f"Phone number(s) for {name}: {phones}"


def show_all():
    if not contacts:
        return "No contacts found"
    result = "Contacts:\n"
    for record in contacts.values():
        phones = ", ".join(str(phone) for phone in record.phones)
        result += f"{record.name}: {phones}\n"
    return result


def main():
    while True:
        command = input("Enter command: ")
        command = command.lower()
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            print(add_contact(command[4:].strip()))
        elif command.startswith("change"):
            print(change_contact(command[7:].strip()))
        elif command.startswith("phone"):
            print(get_phone(command[6:].strip()))
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
