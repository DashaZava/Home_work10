import unittest
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Невірний формат номера телефону")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
                break
        if not found:
            raise ValueError("Номер телефону не знайдено")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phone_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

class TestAddressBook(unittest.TestCase):
    def test_add_record(self):
        book = AddressBook()
        john_record = Record("John")
        book.add_record(john_record)
        self.assertEqual(book.find("John"), john_record)

    def test_delete_record(self):
        book = AddressBook()
        john_record = Record("John")
        book.add_record(john_record)
        book.delete("John")
        self.assertIsNone(book.find("John"))

class TestRecord(unittest.TestCase):
    def test_add_phone(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")
        self.assertEqual(john_record.phones[0].value, "1234567890")

    def test_remove_phone(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.remove_phone("1234567890")
        self.assertEqual(john_record.phones, [])

    def test_edit_phone(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.edit_phone("1234567890", "4444444444")
        self.assertEqual(john_record.phones[0].value, "4444444444")

    def test_find_phone(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")
        phone = john_record.find_phone("1234567890")
        self.assertEqual(phone.value, "1234567890")

if __name__ == '__main__':
    unittest.main()
