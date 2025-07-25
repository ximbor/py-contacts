from typing import Tuple
from input.menu import Menu
from input.menu_item import MenuItem
from input.textual_menu import TextualMenu
from models.address import Address
from models.contact import Contact
from renderers.contact_renderer import ContactRenderer
from renderers.text_contact_renderer import TextContactRenderer
from repositories.contacts_repository import ContactsRepository
from repositories.json_contacts_repository import JsonContactsRepository

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
    state = input("State: ")
    city = input("Town/City: ")
    street_location = input("Street: ") # Use street_location
    zipcode = input("zipcode: ") # Use zipcode
    return Address(street_location=street_location, city=city, state=state, zipcode=zipcode) # Pass arguments by keyword

def input_list(prompt: str) -> Tuple[str]:
    print(f"\n--- {prompt} ---")
    items = []
    while True:
        item = input("Add a value (empty to skip): ")
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
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("E-mail: ")
    address = input_address()
    phone_numbers = input_list("Telephone numbers: ")
    tags = input_list("Tags: ")
    contact = Contact(first_name, last_name, email, address, phone_numbers, tags)
    repository.upsert(contact)

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
            print(f"The contact {selected_contact.first_name} {selected_contact.last_name} has been deleted.")
            return None


def handle_exit(repository: ContactsRepository, renderer: ContactRenderer) -> None:
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