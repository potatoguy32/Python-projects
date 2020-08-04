import random
import sqlite3


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def create_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS
                card(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                number TEXT, pin TEXT, balance INTEGER DEFAULT 0)""")
    conn.commit()


def add_card(number, pin):
    cur.execute('INSERT INTO card (number, pin)'
                ' VALUES(?, ?)', (number, pin))
    conn.commit()


def select_cards():
    cur.execute('SELECT number, pin FROM card')
    return cur.fetchall()


def search_card(card_number, pin):
    cur.execute("""SELECT number, pin FROM card
     WHERE (number = ?) & (pin = ?)""", (card_number, pin))
    return cur.fetchone()


def check_balance(card_number, pin):
    cur.execute("""SELECT balance FROM card
                WHERE (number = ?) & (pin = ?)""", (card_number, pin))
    return cur.fetchone()[0]


def add_income(income, card_number):
    cur.execute("""UPDATE card SET balance = balance + ? WHERE number = ?""",
                (income, card_number))
    conn.commit()


def substract_income(income, card_number):
    cur.execute("""UPDATE card SET balance = balance - ? WHERE number = ?""",
                (income, card_number))
    conn.commit()


def search_number(card_number):
    cur.execute("""SELECT * FROM card WHERE number = ?""", [card_number])
    return cur.fetchone()


def update_balances(money_sent, receiving_account, sending_account):
    add_income(money_sent, receiving_account)
    substract_income(money_sent, sending_account)
    print('Success\n')


def delete_account(card_number):
    cur.execute("""DELETE FROM card WHERE number = ?""", [card_number])
    conn.commit()
    print('The account has been closed!\n')


def luhn_algorithm(card):
    check_sum = 0
    for index, digit in enumerate(card, start=1):
        if index % 2 != 0:
            digit = str(int(digit) * 2)
        if int(digit) > 9:
            digit = str(int(digit) - 9)
        check_sum += int(digit)
    if check_sum % 10 == 0:
        card += '0'
    else:
        for i in range(1, 10):
            if (check_sum + i) % 10 == 0:
                card += str(i)
                break
    return card


def check_luhn(card_number):
    check_sum = 0
    for index, digit in enumerate(card_number, start=1):
        if index % 2 != 0:
            digit = str(int(digit) * 2)
        if int(digit) > 9:
            digit = str(int(digit) - 9)
        check_sum += int(digit)
    return check_sum


def create_card():
    card_number = str(random.randint(400000000000000, 400000999999999))
    card_number = luhn_algorithm(card_number)
    pin = str(random.randint(1111, 9999))
    while (card_number, pin) in card_list:
        card_number = str(random.randint(400000000000000, 400000999999999))
        card_number = luhn_algorithm(card_number)
    return [card_number, pin]


create_db()

selection = ''

while selection != 0:
    selection = int(input('1. Create an account\n2. Log into an account'
                          '\n0. Exit\n'))
    card_list = select_cards()

    if selection == 1:
        new_card = create_card()
        add_card(new_card[0], new_card[1])
        print('\nYour card has been created')
        print(f"Your card number:\n{new_card[0]}\nYour card PIN:\n{new_card[1]}\n")

    elif selection == 2:
        print(card_list)
        card_input = input('\nEnter your card number:\n')
        pin_input = input('Enter your PIN:\n')
        query = search_card(card_input, pin_input)

        if query is not None:
            print('\nYou have successfully logged in!')

            while selection != 0:
                selection = int(input('\n1. Balance\n2. Add income'
                                      '\n3. Do transfer\n4. Close account'
                                      '\n5. Log out\n0. Exit\n'))

                if selection == 1:
                    print('\nBalance: {}\n'.format(
                        check_balance(card_input, pin_input)))

                elif selection == 2:
                    income_input = input('Enter income:\n')
                    add_income(income_input, card_input)
                    print('Income was added!\n')

                elif selection == 3:
                    transfer_number = input('Transfer\nEnter card number:\n')
                    if check_luhn(transfer_number) % 10 != 0:
                        print('Probably you made a mistake in the card'
                              ' number. Try again!')
                        continue
                    query = search_number(transfer_number)

                    if query is not None:
                        account_money = check_balance(card_input, pin_input)
                        transfer_input = input('Enter how much money you want to transfer:\n')

                        if int(transfer_input) > int(account_money):
                            print('Not enough money\n')
                            continue

                        else:
                            update_balances(transfer_input, transfer_number, card_input)

                    else:
                        print('Such card does not exist!')
                        continue

                elif selection == 4:
                    delete_account(card_input)
                    break

                elif selection == 5:
                    print("You have successfully logged out!\n")
                    break

                elif selection == 0:
                    print("Bye!")
                    selection = 0
                    break
        else:
            print('Wrong card number or PIN!')

    elif selection == 0:
        print('\nBye!')
