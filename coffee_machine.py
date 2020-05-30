# Write your code here
class CoffeeMachine:
    def __init__(self):
        self.water_base = 400
        self.milk_base = 540
        self.beans_base = 120
        self.tare_base = 9
        self.money_base = 550
        self.states = ['choosing an action', 'choosing a type of coffee']
        self.cur_state = 'choosing an action'

    def do_this(self, what):
        if self.cur_state == 'choosing an action':
            if what == 'buy': self.cur_state = 'choosing a type of coffee'
            elif what == 'fill': self.fill()
            elif what == 'remaining': self.print_remaining()
            elif what == 'take': self.take()
            elif what == 'exit': exit()
        elif self.cur_state == 'choosing a type of coffee':
            if what.isnumeric():
                drink = int(what)
                if drink == 1: self.brew(250, 0, 16, 1, 4)
                if drink == 2: self.brew(350, 75, 20, 1, 7)
                if drink == 3: self.brew(200, 100, 12, 1, 6)
            elif what == 'back': self.cur_state = 'choosing an action'

    def brew(self, w, m, b, t, d):
        can_brew = True
        resources = []
        if self.water_base - w < 0:
            resources.append('water')
            can_brew = False
        if self.milk_base - m < 0:
            resources.append('milk')
            can_brew = False
        if self.beans_base - b < 0:
            resources.append('coffee beans')
            can_brew = False
        if self.tare_base - t < 0:
            resources.append('disposable cups')
            can_brew = False

        if can_brew:
            print('I have enough resources, making you a coffee!')
            self.water_base -= w
            self.milk_base -= m
            self.beans_base -= b
            self.tare_base -= t
            self.money_base += d
        else:
            print(f'Sorry, not enough {", ".join(resources)}!')
        self.cur_state = 'choosing an action'

    def fill(self):
        self.water_base += int(input('Write how many ml of water do you want to add:\n'))
        self.milk_base += int(input('Write how many ml of milk do you want to add:\n'))
        self.beans_base += int(input('Write how many grams of coffee beans do you want to add:\n'))
        self.tare_base += int(input('Write how many disposable cups of coffee do you want to add:\n'))

    def print_remaining(self):
        print(f'The coffee machine has:\n'
              f'{self.water_base} of water\n'
              f'{self.milk_base} of milk\n'
              f'{self.beans_base} of coffee beans\n'
              f'{self.tare_base} of disposable cups\n'
              f'{self.money_base} of money\n')

    def take(self):
        print(f'I gave you ${self.money_base}\n')
        self.money_base = 0


my_CM = CoffeeMachine()
while True:
    action = input('Write action (buy, fill, take, remaining, exit):\n' if my_CM.cur_state == 'choosing an action'
                   else 'What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n')
    my_CM.do_this(action)
