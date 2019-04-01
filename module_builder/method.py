class Method:

    """Define the methods for each class
    >>> a = Method('method1', ':a_return', '(an_input)')
    >>> print(a.name)
    method1
    >>> print(a.input)
    (an_input)
    >>> print(a.return_type)
    a_return
    >>> a = Method('method1', '', '()')
    >>> print(a.input)
    <BLANKLINE>
    >>> print(a.return_type)
    pass
    """

    def __init__(self, new_name, new_return, new_input):
        self.name = new_name.replace("()", "").replace(" ", "")
        self.input = new_input.replace("()", "")
        self.return_type = self.get_return(new_return)

    def get_return(self, new_return):
        if new_return:
            return new_return.replace(":", "")
        else:
            return "pass"

    def __str__(self):
        if self.input != "":
            return f"    def {self.name}" \
                f"(self, {self.input}) ->{self.return_type}:\n " \
                f"       # ToDo\n        pass\n\n"
        else:
            return f"    def {self.name}" \
                f"(self) ->{self.return_type}:\n        " \
                f"# ToDo\n        pass\n\n"


if __name__ == "__main__":
    from doctest import testmod
    testmod()
