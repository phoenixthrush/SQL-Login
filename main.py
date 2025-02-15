import sqlite3
from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)


def verify_password(hash, password):
    try:
        return ph.verify(hash, password)
    except:
        return False


def register(con, cur):
    while True:
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        hashed_password = hash_password(password)
        print()

        try:
            cur.execute(
                "INSERT INTO Login (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            con.commit()
            print(f"User with username '{username}' created.\n")
            break
        except sqlite3.IntegrityError:
            print(f"Could not create user with username '{username}'.")
            print("Please try again or choose another username.\n")


def login(cur):
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    print()

    result = cur.execute(
        "SELECT password FROM Login WHERE username=?",
        (username,)
    ).fetchone()

    if result and verify_password(result[0], password):
        print("WELCOME!")
    else:
        print("Wrong credentials or not registered.")


def get_users(cur):
    result = cur.execute("SELECT username FROM Login").fetchall()
    if result:
        print("Registered Users:")
        print("\n".join(user[0] for user in result))
        print()
    else:
        print("No registered users.\n")


def drop_table(con, cur):
    cur.execute("DROP TABLE IF EXISTS Login")
    con.commit()
    init_table(cur)


def init_table(cur):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Login (username TEXT UNIQUE, password TEXT)"
    )


def main():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    init_table(cur)

    while True:
        print("=================================")
        print("What are you planning to do?")
        print("1 -> Register")
        print("2 -> Login")
        print("3 -> List Users")
        print("4 -> Reset")
        print("5 -> Quit")
        print("=================================")
        choice = input("$ ")
        print()

        match choice:
            case '1':
                register(con, cur)
            case '2':
                login(cur)
            case '3':
                get_users(cur)
            case '4':
                drop_table(con, cur)
            case '5':
                break

    con.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
