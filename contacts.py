from typing import Tuple, Callable
from input.menu import Menu
from input.menu_item import MenuItem
from input.textual_menu import TextualMenu
from models.address import Address
from models.contact import Contact
from renderers.contact_renderer import ContactRenderer
from renderers.text_contact_renderer import TextContactRenderer
from repositories.contacts_repository import ContactsRepository
from repositories.json_contacts_repository import JsonContactsRepository
from validators import is_valid_naming, is_valid_email, is_valid_zipcode, is_valid_phone_number

def build_main_menu() -> Menu:
    main_menu_options = [
        MenuItem(1, "search", "Search", handle_search_contact),
        MenuItem(2, "export", "Export", handle_export_contacts),
        MenuItem(3, "add", "Add", handle_add_contact),
        MenuItem(4, "remove", "Remove", handle_remove_contact),
        MenuItem(5, "exit", "Exit", handle_exit)
    ]
    return TextualMenu(main_menu_options)

def input_address() -> Address:
    print("\n--- Address ---")
    state = valid_input("State", False, is_valid_naming)
    city = valid_input("Town/City", False, is_valid_naming)
    street_location = valid_input("Street", False, is_valid_naming)
    zipcode = valid_input("zipcode", False, is_valid_zipcode)
    return Address(street_location, city, state, zipcode)

def input_tuple(prompt: str, validator) -> Tuple[str]:
    print(f"\n--- {prompt} ---")
    items = []
    while True:
        # item = input("Add a value (empty to skip): ")
        item = valid_input("Add a value", False, validator)
        if item == "":
            break
        items.append(item)
    return tuple(items)

def handle_export_contacts(repository: ContactsRepository, renderer: ContactRenderer):
    print("\n=== Export Contacts ===")
    filepath = input("File path: ")
    repository.export(filepath)

def handle_add_contact(repository: ContactsRepository, renderer: ContactRenderer):
    print("\n=== Add a new contact ===")
    first_name = valid_input("First name", True, is_valid_naming)
    last_name = valid_input("Last name", True, is_valid_naming)
    email = valid_input("E-mail", False, is_valid_email)
    address = input_address()
    phone_numbers = input_tuple("Telephone numbers: ", is_valid_phone_number)
    tags = input_tuple("Tags: ", is_valid_naming)
    contact = Contact(first_name, last_name, email, address, phone_numbers, tags)
    repository.upsert(contact)

def valid_input(description: str, mandatory: bool, validator: Callable[[str], bool]):

    prompt = description

    if not mandatory:
        prompt += " (or ENTER to skip): "
    else:
        prompt += ": "

    value = input(prompt)

    if not mandatory and value.strip() == "":
        return ""

    if validator(value):
        return value
    else:
        print("⚠️ Input not valid. Try again.")
        return valid_input(description, mandatory, validator)

def handle_search_contact(repository: ContactsRepository, renderer: ContactRenderer):
    print("\n=== Search Contacts ===")
    first_name = input("First name (press ENTER to exclude it from the search): ")
    last_name = input("Last name (press ENTER to exclude it from the search): ")

    output_str = "\nSearching "
    if first_name == "":
        first_name = None
    else:
        output_str+= f"First name = '{first_name}' "
    if last_name == "":
        last_name = None
    else:
        output_str+= f"Last name = '{last_name}'"

    if first_name is None and last_name is None:
        output_str+= "all the contacts"

    print(f"{output_str}...\n")

    contacts = repository.search(first_name, last_name)

    if len(contacts) == 0:
        print("No contacts found.")
    else:
        renderer.display_many(contacts)

def handle_remove_contact(repository: ContactsRepository, renderer: ContactRenderer):
    print("\n=== Remove Contacts ===")
    first_name = input("First name of contact to delete (press ENTER to skip): ")
    last_name = input("Last name of the contact to delete (press ENTER to skip): ")
    if first_name == "" and last_name == "":
        print("Please enter at least the first name or the last name.")
        handle_remove_contact(repository, renderer)
        return None
    else:
        if first_name == "": first_name = None
        if last_name == "": last_name = None

        contacts = repository.search(first_name, last_name)

        if len(contacts) == 0:
            print("No contacts found: no deletion will be performed.")
            return None
        else:
            for i, c in enumerate(contacts):
                print(f"{i + 1}. {c.first_name} {c.last_name}")
            selected_index = input("Please select a contact (insert the number) or press ENTER to cancel: ")

            if selected_index == "":
                return None

            selected_contact = contacts[int(selected_index) - 1]
            repository.delete(selected_contact.first_name.lower(), selected_contact.last_name.lower())
            print(f"'{selected_contact.first_name} {selected_contact.last_name}' has been deleted from contacts.")
            return None

def handle_exit(repository: ContactsRepository, renderer: ContactRenderer) -> None:
    repository = None
    renderer = None
    print("Exiting...\nGoodbye!")

def main():
    renderer = TextContactRenderer()
    repository = JsonContactsRepository()
    print("Welcome to py-contacts!")

    while True:
        print("\n-----------------")
        print("Select an option:")
        main_menu = build_main_menu()
        main_menu.display()
        choose = input("> ")

        try:
            choose_int = int(choose)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        selection = next((item for item in main_menu.items if item.key == choose_int), None)

        if selection is None:
            print("Invalid option. Please select a valid menu item.")
            continue

        print(f"You selected: {selection.code}")

        if selection.action:
            selection.action(repository, renderer)

        if selection.code == "exit":
            break

if __name__ == "__main__":
    main()