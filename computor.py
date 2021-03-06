import sys
import re

""" Class Computor solves polynomials of the second power """


class Computor:

    def __init__(self, equation):
        """ Members """
        self.equation = equation
        self.coeff = [0, 0, 0]
        """ Constants """
        self.CHAR_EQUAL = '='
        self.CHAR_POWER = '^'
        self.CHAR_ASTERIX = '*'
        self.LEFT = 1
        self.RIGHT = -1
        self.POW_2 = 2
        self.POW_1 = 1
        self.POW_0 = 0

    def compute(self):
        self.__check_equation()
        self.__parse_equation()
        self.__calculate()

    def __check_equation(self):
        regex = r"^(-\s)?([0-9]*[.]?[0-9]*\s\*\sX\s\^\s[0-9]*)(\s[-+]\s[0-9]*[.]?[0-9]*\s\*\sX\s\^\s[0-9]*)*\s=\s(-\s)?([0-9]*[.]?[0-9]*\s\*\sX\s\^\s[0-9]*)(\s[-+]\s[0-9]*[.]?[0-9]*\s\*\sX\s\^\s[0-9]*)*$"
        if re.search(regex, eq) is None:
            self.__error_exit("ERROR: Wrong input format")

    def __parse_equation(self):
        pos_equal_sign = self.equation.find(self.CHAR_EQUAL)
        if pos_equal_sign == -1:
            self.__error_exit("ERROR: Wrong format3")
        equation_left_array = self.__split_polynomial(self.equation[:pos_equal_sign - 1])
        equation_right_array = self.__split_polynomial(self.equation[pos_equal_sign + 2:])
        for equation_member in equation_left_array:
            self.__extract_coefficient(equation_member, self.LEFT)
        for equation_member in equation_right_array:
            self.__extract_coefficient(equation_member, self.RIGHT)

        simplified_equation = ""
        simplified_equation += self.__output_member(simplified_equation, self.coeff[2], 2)
        simplified_equation += self.__output_member(simplified_equation, self.coeff[1], 1)
        simplified_equation += self.__output_member(simplified_equation, self.coeff[0], 0)
        print("Reduced form: " + simplified_equation + " = 0")

    def __calculate(self):
        if not self.coeff[2] and self.coeff[1]:
            print("Polynomial degree: 1")
            print("The solution is:")
            result = -1 * self.coeff[0] / self.coeff[1]
            print(result)
        elif not self.coeff[2] and not self.coeff[1]:
            if self.coeff[0] == 0:
                print("All real numbers are solution")
            else:
                print("There are no solutions")
        else:
            discriminant = self.coeff[1] ** 2 - 4 * self.coeff[2] * self.coeff[0]
            if discriminant < 0:
                print("There are no real solutions, but complex are:")
                result1 = str(-1 * self.coeff[1] / (2 * self.coeff[2])) + " + " + str(abs(discriminant**(1.0/2.0)) / (2 * self.coeff[2])) + "i"
                result2 = str(-1 * self.coeff[1] / (2 * self.coeff[2])) + " - " + str(abs(discriminant**(1.0/2.0)) / (2 * self.coeff[2])) + "i"
                print(result1)
                print(result2)
            elif discriminant == 0:
                print("Discriminant is equal zero, the solution is:")
                print(str(-1 * self.coeff[1] / 2 * self.coeff[2]))
            else:
                print("Discriminant is strictly positive, the two solutions are:")
                result1 = str((-1 * self.coeff[1] + discriminant**(1.0/2.0)) / (2 * self.coeff[2]))
                result2 = str((-1 * self.coeff[1] - discriminant**(1.0/2.0)) / (2 * self.coeff[2]))
                print(result1)
                print(result2)

    def __split_polynomial(self, polynomial_string):
        polynomial_members = []
        while len(polynomial_string) > 0:
            pos_power_sign = polynomial_string.find(self.CHAR_POWER)
            if pos_power_sign == -1:
                self.__error_exit("ERROR: Wrong format1")
            polynomial_members.append(polynomial_string[:pos_power_sign + 3])
            polynomial_string = polynomial_string[pos_power_sign + 3:]
        return (polynomial_members)

    def __extract_coefficient(self, polynomial_member, SIDE):
        pow_value = 0
        try:
            pow_value = eval(polynomial_member[polynomial_member.find(self.CHAR_POWER) + 1:])
        except:
            self.__error_exit("Wrong format1")
        if 2 < pow_value or pow_value < 0:
            self.__error_exit("The polynomial degree is stricly greater than 2, I can't solve.")
        try:
            coeff = eval(polynomial_member[:polynomial_member.find(self.CHAR_ASTERIX) - 1])
            self.coeff[pow_value] = self.coeff[pow_value] + coeff * SIDE
        except:
            self.__error_exit("Wrong format2")

    def __output_member(self, simplified_equation, member, member_power):
        member_string = ""
        if int(member) < 0:
            member_string = member_string + " - " + str(abs(member))
        elif int(member) > 0 and not len(simplified_equation):
            member_string = member_string + str(abs(member))
        elif int(member) > 0 and len(simplified_equation):
            member_string = member_string + " + "+ str(abs(member))

        if member_power == 2 and member:
            member_string = member_string + " * X ^ 2"
        elif member_power == 1 and member:
            member_string = member_string + " * X"
        elif member_power == 0 and not member and not len(simplified_equation):
            member_string = member_string + "0"
        return member_string

    def __error_exit(self, error_comment):
        print(error_comment)
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        eq = sys.argv[1]
        Computor(eq).compute()
    else:
        print("ERROR: Must be 2 arguments")
