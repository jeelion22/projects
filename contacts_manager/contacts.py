class Contacts:
    def __init__(self):
        self.view = "list"  # represents the status of the view attribute
        self.contact_list = (
            []
        )  # contains the list of objects those contain contact information
        self.choice = None  # represents the user choice
        self.index = (
            None  # represents the index of the object in the contact_list attribute
        )

    def display(self):
        """This method performs various operations based on the value of the view attribute of the class"""
        while True:
            if self.view == "list":
                self.show_list()

            elif self.view == "info":
                self.show_info()

            elif self.view == "add":
                self.add_contact()
            elif self.view == "quit":
                print("\nClosing the contacts list...\n")
                break

    def show_list(self):
        print()
        # if the contact_list attribute contains no elements, this block will be executed
        if len(self.contact_list) == 0:
            # Gets inputs from the user
            self.choice = input("(A)dd a new contact \n(Q)uit \n>").lower()
        else:
            #  if the contact_list contains elements, this block of code will be executed
            for index, contact in enumerate(self.contact_list):
                # prints the contact person's first_name and last_name along with serial number
                print(f"{index + 1} {contact.first_name} {contact.last_name}")
            # gets the input from the user whether they want get the contact details or want to add new contact
            self.choice = input(
                "\n(#) Select a name \n(A)dd a new contact\n(Q)uit \n> "
            ).lower()
        # at the end, the handle method is invoked
        self.handle_choice()

    def handle_choice(self):
        """This method handles the operation on the object based on the user's input"""
        if self.choice == "q":
            self.view = "quit"
        elif self.choice == "a" and self.view == "list":
            self.view = "add"
        elif self.choice.isnumeric() and self.view == "list":
            index = (
                int(self.choice) - 1
            )  # represents the index of the object in the contact_list

            if index >= 0 and index < len(self.contact_list):
                self.index = index  # sets the value for the index attribute
                self.view = "info"  # changes the value of the instance variable to info
        elif (
            self.choice == "c" and self.view == "info"
        ):  # c represents the contact list if there is atleast one contact
            self.view = (
                "list"  # as we set the attribute to list, the show() method is invoked
            )

        elif (
            self.choice == "n" and self.view == "info"
        ):  # if the condtions staisfied, the next contact will be showed
            self.index = (
                self.index + 1 if self.index + 1 < len(self.contact_list) else 0
            )

        elif (
            self.choice == "p" and self.view == "info"
        ):  # if the conditions satisfied, the previous contact will be showed
            self.index = (
                self.index - 1 if self.index - 1 >= 0 else len(self.contact_list) - 1
            )

    def show_info(self):
        """It is the mathod used to display the information about the contact"""
        self.contact_list[
            self.index
        ].display_info()  # it is the method of Information class
        self.choice = input(
            "\n(C)ontact List \n(P)revious contact \n(N)ext contact \n(Q)uit \n> "
        ).lower()
        self.handle_choice()

    # the concept of polymorphism is involved
    # operator overloading concept is used
    # defined opertor overloading
    def __add__(self, new_contact):  # overloading addition operator
        self.contact_list.append(
            new_contact
        )  # opends the instance of the Information class to the contact_list attribute of the Contacts class

    def add_contact(self):
        self + Information()  # used operator overloading
        self.view = "list"


# definition of Information class and its methods
class Information:
    def __init__(self):
        self.first_name = input("Enter their first name: ")
        self.last_name = input("Enter their last name: ")
        self.personal_phone = input("Enter their personal phone number: ")
        self.personal_email = input("Enter their personal email: ")
        self.work_phone = input("Enter their work phone number: ")
        self.work_email = input("Enter their work email: ")
        self.work_title = input("Enter their work title: ")

    # method displays the contacts information when it is invocked on the information class instance
    def display_info(self):
        print(f"\n{self.first_name} {self.last_name}")
        print(f"Personal phone number: {self.personal_phone}")
        print(f"Personal email address: {self.personal_email}")
        print(f"Work title: {self.work_title}")
        print(f"Work phone number: {self.work_phone}")
        print(f"Work email address: {self.work_email}")


contacts = Contacts()
contacts.display()
