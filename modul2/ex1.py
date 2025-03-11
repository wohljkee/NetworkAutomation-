valid_mony = [1, 5, 10, 50, 100]
beverages = {
    1: {"name": "Sandwich", "price": 8},
    2: {"name": "Cafea", "price": 4},
    3: {"name": "Cola", "price": 5},
    4: {"name": "Apa", "price": 3},
    5: {"name": "Snack", "price": 5},
    6: {"name": "Meniu sandwich +cola", "price": 11},

}


def show_menu():
    print("1. Sandwich              ...8lei")
    print("2. Cafea                 ...4lei")
    print("3. Cola                  ...5lei")
    print("4. Apa                   ...3lei")
    print("5. Snack                 ...5lei")
    print("6. Meniu sandwich +cola  ...11lei")


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

    if money in valid_mony:
        remaining_price = beverages[selection]["price"] - money

        for i in range(3):
            if remaining_price > 0:
                more_money = input("give more money")
                try:
                    more_money = int(more_money)
                except ValueError:
                    print("\nIncorrect money, please try again")
                    continue
                if more_money not in valid_mony:
                    print("\nIncorrect money, please try again")
                    continue
                remaining_price = remaining_price - more_money
            else:
                break
        else:
            print(f'Retuning all money: {beverages[selection]["price"] - remaining_price}')
        if remaining_price < 0:
            print(f'se va returna {-remaining_price}')

        print(f'Returning product: {beverages[selection]["name"]}')
    else:
        print(f'Retuning all money: {money}')
