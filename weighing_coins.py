import random
import math
import time

equal_scale = """
 ┎─────◉─────┒
 ┆     ║     ┆
═╧═    ║    ═╧═
       ║   
       ║
       ║
       ║
      ─╨─
""".split("\n")

left_scale = """
       ╱┊
      ╱═╧═
     ╱ 
    ◉
   ╱║
  ╱ ║
 ╱  ║
 ┊  ║
═╧═ ║
    ║
    ╨ 
""".split("\n")

right_scale = """
 ┊╲
═╧═╲
    ╲
     ◉
     ║╲
     ║ ╲
     ║  ╲
     ║  ┊
     ║ ═╧═
     ║ 
     ╨ 
""".split("\n")

MODES = {
    "KNOWN":    0, ## The game lets you know if the odd coin out is heavier or lighter
    "UNKNOWN":  1  ## You have to not only determine whether the odd coin is heavier or lighter
}

class Game:
    def __init__(self, num_coins: int, mode: int = MODES["KNOWN"]):
        self.N = num_coins
        self.MODE = mode

    def setup(self):
        self.left_bucket = []
        self.right_bucket = []
        self.ODD_COIN = random.randrange(0, self.N)
        self.HEAVIER = True if random.random() < 0.5 else False
        self.guess = -1

        if self.MODE == MODES["KNOWN"]:
            self.NUM_WEIGHS = math.ceil(math.log(self.N, 3))
        elif self.MODE == MODES["UNKNOWN"]:
            self.NUM_WEIGHS = math.ceil(math.log(2 * self.N + 1, 3))

    def start(self):
        self.setup()
        self.turn = 1
        finished = False

        print("Starting game...")
        if self.MODE == MODES["UNKNOWN"]:
            info = "different"
        elif self.MODE == MODES["KNOWN"]:
            info = "heavier" if self.HEAVIER else "lighter"
        print(f"You have {self.N} coins! However, one of them is {info}.")
        print(f"All you have is a scale to find the counterfeit coin; try to find it in {self.NUM_WEIGHS} turns on the scale!\n")
        time.sleep(3)

        while not finished:
            print(f"{self.NUM_WEIGHS - self.turn + 1} turn(s) remaining!")

            self.selected_coins = [False] * self.N
            self.printAvailable()
            selected_result = self.handleCoinInput("Select the coins to go in the left bucket: ")
            if selected_result[0]:
                self.left_bucket = selected_result[1]
            else:
                print("Invalid input, try again.")
                continue

            print()

            self.printAvailable()
            selected_result = self.handleCoinInput("Select the coins to go in the right bucket: ")
            if selected_result[0]:
                self.right_bucket = selected_result[1]
            else:
                print("Invalid input, try again.\n")
                continue

            # print(f"Left: {self.left_bucket}, right: {self.right_bucket}")

            self.weigh()
            self.getAnswer()

            if self.guess == self.ODD_COIN:
                print("Correct!\n")
                break
            else:
                print("No correct answer found yet, attempting to continue game...\n")

            if self.turn == self.NUM_WEIGHS:
                print("Out of turns!\n")
                break

            self.turn += 1
        print("Game over.")

    def getAnswer(self):
        raw_input = input(f"It's been {self.turn} turn(s), do you have an answer? (y/n) ")
        if raw_input.lower() in ['y', 'yes']:
            raw_input = input("Answer: ")
            try:
                guess = int(raw_input)
                if not (0 < guess <= self.N):
                    raise ValueError("Invalid range")
                self.guess = guess - 1
            except ValueError:
                print("Invalid input, continuing game.")

    def printAvailable(self):
        available = []
        for i in range(self.N):
            if not self.selected_coins[i]:
                available.append(str(i + 1))
        print("Available coins:", " ".join(available))

    def handleCoinInput(self, msg):
        selected = []
        raw_input = input(msg)
        try:
            for item in raw_input.split():
                coin = int(item)
                if not (0 < coin <= self.N):
                    raise ValueError("Invalid coin range")
                if self.selected_coins[coin - 1]:
                    raise ValueError("Coin already used")
                if not (coin - 1 in selected):
                    selected.append(coin - 1)

            for n in selected:
                self.selected_coins[n] = True
            return (True, selected)
        except ValueError:
            return (False, None)

    def weigh(self):
        left_size = len(self.left_bucket)
        right_size = len(self.right_bucket)
        if left_size > right_size:
            self.drawScale(1)
            print("The left is heavier.")
        elif left_size < right_size:
            self.drawScale(2)
            print("The right is heavier.")
        else:
            if self.ODD_COIN in self.left_bucket:
                if self.HEAVIER:
                    self.drawScale(1)
                    print("Left is heavier.")
                else:
                    self.drawScale(2)
                    print("Right is heavier.")
            elif self.ODD_COIN in self.right_bucket:
                if self.HEAVIER:
                    self.drawScale(2)
                    print("Right is heavier.")
                else:
                    self.drawScale(1)
                    print("Left is heavier.")
            else:
                self.drawScale(0)
                print("Equal.")

    def drawScale(self, state): ## 0: balanced, 1: left heavy, 2: right heavy
        left_bucket_str = " ".join(str(n + 1) for n in self.left_bucket)
        right_bucket_str = " ".join(str(n + 1) for n in self.right_bucket)

        buffer = f" {left_bucket_str} "
        buffer_size = len(buffer)
        if state == 0:
            for i, line in enumerate(equal_scale):
                output = line
                if i == 3:
                    output = buffer + output + f" {right_bucket_str} "
                else:
                    output = " " * buffer_size + output
                print(output)
        elif state == 1:
            for i, line in enumerate(left_scale):
                output = line
                if i == 9:
                    output = buffer + output
                elif i == 2:
                    output = " " * buffer_size + output + f" {right_bucket_str} "
                else:
                    output = " " * buffer_size + output
                print(output)
        elif state == 2:
            for i, line in enumerate(right_scale):
                output = line
                if i == 2:
                    output = buffer + output
                elif i == 9:
                    output = " " * buffer_size + output + f" {right_bucket_str} "
                else:
                    output = " " * buffer_size + output
                print(output)


if __name__ == "__main__":
    while True:
        game = Game(8)
        # game = Game(12, MODES["UNKNOWN"])
        game.start()
        time.sleep(3)
        print("---------------\nRestarting game...\n--------------")

# TODO: Change vim python syntax for multi-line dictionary definitions
# TODO: Vim auto place you at correct indentation when entering from NORMAL mode, python
