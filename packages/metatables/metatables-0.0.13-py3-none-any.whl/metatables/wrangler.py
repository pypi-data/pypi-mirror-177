

class Person():
    def __init__(self, fname: str, lname: str) -> None:
        """This is a person

        Args:
            fname (str): first name
            lname (str): last name
        """
        self.fname = fname
        self.lname = lname

        self.print_main_greeting()

    def print_main_greeting(self):
        """Prints a greeting.
        """
        print(f'Welcome {self.fname} {self.lname}!')


class Student(Person):
    def __init__(self, fname: str, lname: str, semester: int) -> None:
        """This is a student

        Args:
            fname (str): first name
            lname (str): last name
            semester (int): Students semester
        """
        super().__init__(fname, lname)
        self.semester = semester

        self.print_greeting()

    def print_greeting(self):
        """Prints a more specific greeting
        """
        print(f'Welcome {self.fname} {self.lname} to the {str(self.semester)}. semester!')

    def return_greeting(self):
        """Returns a more specific greeting
        """
        return f'Welcome {self.fname} {self.lname} to the {str(self.semester)}. semester!'
