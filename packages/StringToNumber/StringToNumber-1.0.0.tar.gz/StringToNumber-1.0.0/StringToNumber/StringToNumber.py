class StringToNumber:

    def zero(command=None):
        if command:
            return eval('0' + str(command))
        else:
            return '0'

    def one(command=None):
        if command:
            return eval('1' + str(command))
        else:
            return '1'

    def two(command=None):
        if command:
            return eval('2' + str(command))
        else:
            return '2'

    def three(command=None):
        if command:
            return eval('3' + str(command))
        else:
            return '3'

    def four(command=None):
        if command:
            return eval('4' + str(command))
        else:
            return '4'

    def five(command=None):
        if command:
            return eval('5' + str(command))
        else:
            return '5'

    def six(command=None):
        if command:
            return eval('6' + str(command))
        else:
            return '6'

    def seven(command=None):
        if command:
            return eval('7' + str(command))
        else:
            return '7'

    def eight(command=None):
        if command:
            return eval('8' + str(command))
        else:
            return '8'

    def nine(command=None):
        if command:
            return eval('9' + str(command))
        else:
            return '9'

    def ten(command=None):
        if command:
            return eval('10' + str(command))
        else:
            return '10'

    def one_hundred(command=None):
        if command:
            return eval('100' + str(command))
        else:
            return '100'

    def one_thousand(command=None):
        if command:
            return eval('1000' + str(command))
        else:
            return '1000'

    def plus(command):
        return '+' + str(command)

    def minus(command):
        return '-' + str(command)

    def times(command):
        return '*' + str(command)

    def divided_by(command):
        return '//' + str(command)