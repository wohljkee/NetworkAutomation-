def show_menu():
    print("1. Sandwich              ...8lei")
    print("2. Cafea                 ...4lei")
    print("3. Cola                  ...5lei")
    print("4. Apa                   ...3lei")
    print("5. Snack                 ...5lei")
    print("6. Meniu sandwich +cola  ...11lei")

valid_mony = [1,5,10,50,100]
while True:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == 'x':
        break

    try:
        selection = int(choice)
    except ValueError:
        print("Invalid choice, please try again")
        continue

    money = input("Give money: ")
    try:
        money = int(money)
    except ValueError:
        print("\nIncorrect money, please try again")
        continue
    if money in valid_mony:
        pass