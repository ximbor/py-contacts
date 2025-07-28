import json
import os
import shutil
from dataclasses import asdict
from models.contact import Contact
from typing import List
from pathlib import Path
from repositories.contacts_repository import ContactsRepository

class InvalidJsonRepositoryError(Exception):
    """
    Invalìd JSON repository exception.
    """
    pass

class FailedLoadRepositoryError(Exception):
    """
    Filed load repository exception.
    """
    pass

class JsonContactsRepository(ContactsRepository):
    """"
        JSON ContactsRepository class.
    """
    pass

class InvalidExportRepositoryError(Exception):
    """
    Invalìd Export repository exception.
    """
    pass

class JsonContactsRepository(ContactsRepository):
    """"
    JSON ContactsRepository class.
    """

    def __init__(self, filepath: str = "./data.json", auto_create = True):
        self.contacts = dict
        self.filepath = filepath
        self.auto_create = auto_create
        self.load_all()

    def _clear_cache(self) -> None:
        """
        Clear cache.
        """
        self.contacts = dict

    def _write_all(self) -> None:
        """
        Write all contacts.
        """
        contacts_dicts = [asdict(contact) for contact in self.contacts.values()]
        with open(self.filepath, 'w') as f:
            json.dump(contacts_dicts, f, indent = 4)

    def load_all(self) -> None:
        """
        Load all contacts.
        """

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
        """
        Upsert a contact.
        Args:
              contact (Contact): Contact.
        """

        key = (contact.first_name.lower(), contact.last_name.lower())
        self.contacts.update({key: contact})
        self._write_all()

    def delete(self, first_name, last_name) -> None:
        """
        Delete a contact.
        Args:
             first_name (str): First name.
             last_name (str): Last name.
        """

        key = (first_name, last_name)
        self.contacts.pop(key)
        self._write_all()

    def get_all(self) -> List[Contact]:
        """
        Get all contacts.
        """
        return self.contacts.values()

    def export(self, export_path: str = "./data-export.json") -> None:
        """
        Export all contacts.
        """
        try:
            export_file_path = Path(export_path).expanduser().resolve(strict=False)

            if not export_file_path.parent.exists():
                raise InvalidExportRepositoryError(f"The export path should be in an existing directory.")

            if export_file_path.exists() and export_file_path.is_dir():
                raise InvalidExportRepositoryError(f"The export path should be an actual file, not a directory.")

            repo_file_path = Path(self.filepath).expanduser().resolve(strict=False)
            if export_file_path == repo_file_path:
                raise InvalidExportRepositoryError(f"The export path {export_file_path} must be different from the contacts' repository path {repo_file_path}.")

            shutil.copyfile(self.filepath, export_path)
            return None

        except Exception as e:
            raise InvalidExportRepositoryError(f"Could not export the contacts: {e}.")

    def search(self, first_name = None, last_name = None) -> list[Contact]:
        """
        Search all contacts.

        Args:
             first_name (str): First name.
             last_name (str): Last name.

        Returns:
            List[Contact]: List of contacts.
        """

        print(first_name, last_name)

        filtered_contacts = [
            v for k, v in self.contacts.items() if (first_name is None or k[0] == first_name.lower()) and (last_name is None or k[1] == last_name.lower())
        ]
        return filtered_contacts