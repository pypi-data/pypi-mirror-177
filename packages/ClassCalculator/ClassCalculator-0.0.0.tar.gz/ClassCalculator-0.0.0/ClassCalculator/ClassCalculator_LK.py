class Calculator:
    """ Simple calculator model performing
   addition, subtraction, multiplication, division and Nth root.
   every calculation result is kept in memory for next calculation
    """

    def __init__(self, number1):

        self.__memory = number1

    def add(self, number2):
        return self.__memory + number2

    def subtract(self, number2):
        return self.__memory - number2

    def multiply(self, number2):
        return self.__memory * number2

    def divide(self, number2):
        return self.__memory / number2

    def root(self, number2):
        return self.__memory ** (1 / number2)

    def action(self, operator, number2):
        """ Gets string naming selected operator
        initiates calculation after
        returns float
        keeps float in memory until next iteration
        FIXME move memory from each statement to shorten script
        """
        if operator == "+":
            k = self.add(number2)
            self.__memory = k
            return k
        elif operator == "-":
            k = self.subtract(number2)
            self.__memory = k
            return k
        elif operator == "*":
            k = self.multiply(number2)
            self.__memory = k
            return k
        elif operator == "/":
            k = self.divide(number2)
            self.__memory = k
            return k
        elif operator == "root":
            k = self.root(number2)
            self.__memory = k
            return k
        else:
            """ Prints warning invalid operator input
            initiates next iteration
            """
            print("Operator invalid")


calculation = input("Please input two number and operator between them: ")
calculation = calculation.strip().split(" ")
""" Input requires float, string and another float with white spaces between them.
Exact sequence and type required otherwise program crashes.
FIXME self-check function prevent program from crash"""
user_number1 = float(calculation[0])
user_number2 = float(calculation[2])
action = calculation[1]

calc = Calculator(user_number1)
result = calc.action(action, user_number2)
print("Result:", result)

while True:
    """ Requires input string to initiate another calculation
    either stops program and resets calculation accumulated result
    """
    another_calculation = input("another calculation?: ")

    if another_calculation.lower()[0] == "y":
        next_step = input("enter operator and number ")
        next_step = next_step.strip().split(" ")
        user_numberX = float(next_step[1])
        next_action = next_step[0]

        next_result = calc.action(next_action, user_numberX)
        print("next result:", next_result)

    else:
        print("Calculation ended.")
        break
