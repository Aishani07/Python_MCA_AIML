print("SECURE EMPLOYEE ACCOUNT SYSTEM")

accounts = {}

n = int(input("Enter number of accounts to create: "))

for i in range(n):
    print("\n--- Account", i + 1, "---")

    username = input("Enter username: ")

    while True:
        password = input("Enter password: ")

        upper = False
        lower = False
        digit = False
        special = False
        space = False

        for ch in password:
            if ch.isupper():
                upper = True
            elif ch.islower():
                lower = True
            elif ch.isdigit():
                digit = True
            elif ch == " ":
                space = True
            else:
                special = True

        valid = True

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            valid = False

        if upper == False:
            print("Password must contain an uppercase alphabet.")
            valid = False

        if lower == False:
            print("Password must contain a lowercase alphabet.")
            valid = False

        if digit == False:
            print("Password must contain a digit.")
            valid = False

        if special == False:
            print("Password must contain a special character.")
            valid = False

        if space == True:
            print("Password must not contain spaces.")
            valid = False

        if valid == True:
            break
        else:
            print("Password rejected!")
            print("Please enter the password again.")

    while True:
        confirm = input("Confirm password: ")

        if confirm == password:
            accounts[username] = password
            print("Account created successfully!")
            break
        else:
            print("Passwords do not match. Please enter the confirm password again.")


print("\n EMPLOYEE LOGIN ")

attempts = 5

while attempts > 0:
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in accounts:
        if accounts[username] == password:
            print("Login successful!")
            print("Welcome", username)
            break
        else:
            print("Invalid username or password.")
    else:
        print("Invalid username or password.")

    attempts = attempts - 1

    if attempts > 0:
        print("Attempts remaining:", attempts)
    else:
        print("Access Denied!")
        print("Maximum login attempts exceeded.")
