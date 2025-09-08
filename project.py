import os, cowsay, sqlite3

class User:
    def __init__(self, name):
        self.name = name

    def get_infos(self):
        self.name = input('What is your name? ').capitalize()


# --- Database Functions ---

def connect_sql():
    """Connects to the database and returns the connection and cursor."""
    database = sqlite3.connect('database.db')
    cursor = database.cursor()
    return database, cursor


def create_table(cursor):
    """Creates the table for the secrets, if it doesn't exist."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dragon_secrets(
            name TEXT,
            secret TEXT
        )
    ''')


def insert_value(database, cursor, player):
    """Inserts the player's name and secret into the table."""
    secret = input('Tell me your secret... ')

    # The table has 2 columns (name, secret), so we need to insert 2 values.
    cursor.execute(
        'INSERT INTO dragon_secrets (name, secret) VALUES (?, ?)',
        (player.name, secret)
    )
    database.commit()
    print(cowsay.get_output_string('dragon', f'I will keep your secret safe.'))


def get_secret(database, cursor):
    try:
        second_player = input('Tell me with person you want to know about? ').capitalize()

        cursor.execute(
            'SELECT secret FROM dragon_secrets WHERE name = ? ORDER BY RANDOM() LIMIT 1',
            (second_player,)
        )
        secret = cursor.fetchone()[0]

        print(f'{second_player}: "{secret}"')

    except sqlite3.OperationalError:
        print("I know nothing about this person...")
    except ValueError:
        print("I don't know what you sayed")


def update_player_secret(database, cursor, player):
    """Allows a player to choose and update one of their secrets."""
    cursor.execute(
        'SELECT secret FROM dragon_secrets WHERE name = ?',
        (player.name,)
    )
    results = cursor.fetchall()

    if not results:
        print(f"I don't have any secrets from you '{player.name}'.")
        return

    secrets_list = [item[0] for item in results]

    print("\nWith secret do you want me to update?")
    for index, secret in enumerate(secrets_list):
        print(f"{index + 1}. {secret}")

    # Initializes the variable as an invalid number. It's a good practice.
    chosen_index = -1

    # Loop to ensure the choice is valid
    while True:
        try:
            choice = int(input("\nTell me which one: "))
            if 1 <= choice <= len(secrets_list):
                chosen_index = choice - 1  # Adjusts for the list index (which starts at 0)
                break
            else:
                print(f"Invalid input. Please, enter a number between 1 and {len(secrets_list)}.")
        except ValueError:
            print("Invalid input. Please, Enter a number.")

    # Gets the original secret's value that will be updated
    secret_to_update = secrets_list[chosen_index]

    # Ask for the new value
    new_secret = input(f"Tell me the updates '{secret_to_update}': ")

    # Execute the UPDATE on the database
    try:
        cursor.execute(
            'UPDATE dragon_secrets SET secret = ? WHERE name = ? AND secret = ?',
            (new_secret, player.name, secret_to_update)
        )
        database.commit()
        print(cowsay.get_output_string('dragon', f'I See, that is a really good secret...'))

    except Exception as e:
        print(f"\nI didn't understand... {e}")
        database.rollback()

def delete_secret(database, cursor, player):
    """Allows a player to choose and delete one of their secrets."""
    cursor.execute(
        'SELECT secret FROM dragon_secrets WHERE name = ?',
        (player.name,)
    )
    results = cursor.fetchall()

    if not results:
        print(f"Nothing was told yet '{player.name}'.")
        return

    secrets_list = [item[0] for item in results]

    print("\nWith secret do you want me to forget? :")
    for index, secret in enumerate(secrets_list):
        print(f"{index + 1}. {secret}")

    # Initializes the variable as an invalid number. It's a good practice.
    chosen_index = -1

    while True:
        try:
            choice = int(input("\nTell me which one... "))
            if 1 <= choice <= len(secrets_list):
                chosen_index = choice - 1  # Adjusts for the list index (which starts at 0)
                break
            else:
                print(f"Invalid input. Please, enter a number between 1 and {len(secrets_list)}.")
        except ValueError:
            print("Invalid input. Please, Enter a number.")

    # Gets the original secret's value that will be deleted
    secret_to_delete = secrets_list[chosen_index]

    # Execute the DELETE on the database
    try:
        cursor.execute(
            'DELETE FROM dragon_secrets WHERE name = ? AND secret = ?',
            (player.name, secret_to_delete)
        )
        database.commit()
        print(cowsay.get_output_string('dragon', f"\nI dont remember the secret: '{secret_to_delete}' anymore..."))

    except Exception as e:
        print(f"\nI didn't understand... {e}")
        database.rollback()


# --- Main Interface ---

def interface(database, cursor):
    """Manages the interaction with the user."""
    # 1. Create a user object
    player = User(None)
    # 2. Asks for their name and stores it in the object
    player.get_infos()

    print(cowsay.get_output_string('dragon', f'Welcome to Dragon Cave, Traveler {player.name}.'))
    print('...Choose wisely one of the options: ')
    print('[1] - Tell the Dragon one of your secrets')
    print('[2] - Ask for someone secret')
    print('[3] - Ask the Dragon to update a secret')
    print('[4] - Ask the Dragon to forget a secret')
    print('[5] - Quit')

    while True:
        try:
            choice = int(input("Your choice: "))
            match choice:
                case 1:
                    insert_value(database, cursor, player)
                    break
                case 2:
                    get_secret(database, cursor)
                    break
                case 3:
                    update_player_secret(database, cursor, player)
                    break
                case 4:
                    delete_secret(database, cursor, player)
                    break
                case 5:
                    break
                case _:
                    print("I doesn't understand that option.")

        except ValueError:
            print("Please enter a number.")

def main():
    # Clears the screen
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

    # 1. Connects to the DB and STORES the connection and cursor in variables
    db_connection, db_cursor = connect_sql()

    # 2. Passes the cursor to create the table
    create_table(db_cursor)

    # 3. Passes the connection and cursor to the main interface
    interface(db_connection, db_cursor)

    # 4. Closes the connection at the end of the program
    db_connection.close()


if __name__ == "__main__":
    main()

