import random

print("H A N G M A N")

answer = ""

while answer != "exit":
    answer = input('Type "play" to play the game, "exit" to quit: \n')
    if answer == "play":
        words = ['python', 'java', 'kotlin', 'javascript']
        test = random.choice(words)
        lines = ["-" for part in range(len(test))]
        lives = 8
        repeated = []

        while lives > 0:
            print("".join(lines))
            attemp = input("input a letter: ")
            if attemp in repeated:
                print("You already typed this letter\n")
                continue
            elif len(attemp) != 1:
                print("You should input a single letter\n")
                continue
            elif (attemp.isupper()) or (attemp.isalpha() == False):
                print("It is not an ASCII lowercase letter\n")
                continue
            if attemp in test:
                for count, letter in enumerate(list(test)):
                    if letter == attemp:
                        lines[count] = attemp
            else:
                print("No such letter in the word")
                lives = lives - 1
            if ("".join(lines)) == test:
                print(f"You guessed the word {''.join(lines)}!\nYou survived!")
                break
            if lives == 0:
                print("You are hanged!")
                break
            repeated.append(attemp)
            print()

    elif (answer != "play") and (answer != "exit"):
        continue
