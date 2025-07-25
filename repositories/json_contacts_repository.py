import json
import os
import shutil
from dataclasses import asdict

from models.contact import Contact
from typing import List

from repositories.contacts_repository import ContactsRepository

class InvalidJsonRepositoryError(Exception):
    pass

class FailedLoadRepositoryError(Exception):
    pass

class JsonContactsRepository(ContactsRepository):

    def __init__(self, filepath: str = "./data.json", auto_create = True):
        self.contacts = dict
        self.filepath = filepath
        self.auto_create = auto_create
        self.load_all()

    def _clear_cache(self) -> None:
        self.contacts = dict

    def _write_all(self) -> None:
        contacts_dicts = [asdict(contact) for contact in self.contacts.values()]
        with open(self.filepath, 'w') as f:
            json.dump(contacts_dicts, f, indent = 4)

    def load_all(self) -> None:

        if self.auto_create and not os.path.exists(self.filepath):
            try:
                os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=4)
            except OSError as e:
                raise FailedLoadRepositoryError(f"Unable to create repository file: {e}")

        try:
            self._clear_cache()
            contacts_dict = json.load(open(self.filepath, "r", encoding="utf-8"))
            self.contacts = { (contact["first_name"].lower(), contact["last_name"].lower()): Contact.from_dict(contact) for contact in contacts_dict }

        except json.JSONDecodeError as e:
            raise FailedLoadRepositoryError(f"Invalid JSON format in repository file: {e}")
        except OSError as e:
            raise FailedLoadRepositoryError(f"Unable to read repository file: {e}")

    def upsert(self, contact: Contact) -> None:
        key = (contact.first_name, contact.last_name)
        self.contacts.update({key: contact})
        self._write_all()

    def delete(self, first_name, last_name) -> None:
        key = (first_name, last_name)
        self.contacts.pop(key)
        self._write_all()

    def get_all(self) -> List[Contact]:
        return self.contacts.values()

    def export(self, export_path: str = "./data-export.json") -> None:
        shutil.copyfile(self.filepath, export_path)

    def search(self, first_name = None, last_name = None) -> list[Contact]:
        filtered_contacts = [
            v for k, v in self.contacts.items() if (first_name is None or k[0] == first_name.lower()) and (last_name is None or k[1] == last_name.lower())
        ]
        return filtered_contacts