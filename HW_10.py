from collections import UserDict

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, criteria):
        results = []
        for record in self.data.values():
            if record.matches_criteria(criteria):
                results.append(record)
        return results


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def remove_field(self, field):
        self.fields.remove(field)

    def edit_field(self, field, new_value):
        field.value = new_value

    def matches_criteria(self, criteria):
        for field in self.fields:
            if field.matches_criteria(criteria):
                return True
        return False


class Field:
    def __init__(self, value):
        self.value = value

    def matches_criteria(self, criteria):
        return str(self.value).lower() == str(criteria).lower()


class Name(Field):
    pass


class Phone(Field):
    pass


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input. Please enter name and phone number separated by a space."
        except IndexError:
            return "Invalid input. Please enter name and phone number separated by a space."

    return inner


address_book = AddressBook()


@input_error
def add_contact(contact_info):
    name, phone = contact_info.split(' ')
    record = Record(name)
    phone_field = Phone(phone)
    record.add_field(phone_field)
    address_book.add_record(record)
    return "Contact added successfully."


@input_error
def change_phone(contact_info):
    name, phone = contact_info.split(' ')
    record = address_book.data.get(name)
    if record:
        phone_field = record.fields[0]
        record.edit_field(phone_field, phone)
        return "Phone number updated successfully."
    else:
        raise KeyError


@input_error
def show_phone(name):
    record = address_book.data.get(name)
    if record:
        phone_field = record.fields[0]
        return phone_field.value
    else:
        raise KeyError


def show_all_contacts():
    if len(address_book.data) == 0:
        return "No contacts found."
    else:
        return "\n".join([f"{name}: {record.fields[0].value}" for name, record in address_book.data.items()])


def command_parser(command):
    command = command.strip()

    if command == "hello":
        return "How can I help you?"
    elif command.startswith("add"):
        contact_info = command[4:]
        return add_contact(contact_info)
    elif command.startswith("change"):
        contact_info = command[7:]
        return change_phone(contact_info)
    elif command.startswith("phone"):
        name = command[6:]
        return show_phone(name)
    elif command == "show all":
        return show_all_contacts()
    else:
        return "Invalid command. Please try again."


def process_command(command):
    if command in ["good bye", "close", "exit"]:
        print("Good bye!")
        return False

    result = command_parser(command)
    print(result)
    return True


def main():
    print("How can I help you?")

    while True:
        command = input("> ").lower()

        if not process_command(command):
            break


if __name__ == "__main__":
    main()