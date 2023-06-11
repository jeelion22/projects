import csv


class CoffeeJournal:
    # initializer method
    def __init__(self, file):
        self._file = file
        self._roaster = ""
        self._country = ""
        self._region = ""
        self._stars = ""
        self._old_coffee = self.load_coffee()
        self._new_coffee = []

    # loads the data from the .csv file and returns list
    def load_coffee(self):
        coffee = []
        with open(self._file) as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                coffee.append(row)
        return coffee

    # inbuilt property decorator is used to get and mutate the  instance variable
    @property
    def roaster(self):
        return self._roaster

    @roaster.setter
    def roaster(self, new_roaster):
        self._roaster = new_roaster

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, new_country):
        self._country = new_country

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, new_region):
        self._region = new_region

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, new_stars):
        self._stars = new_stars

    # adds the coffee to the instance variable self._new_coffee
    def add_coffee(self):
        self._new_coffee.append(
            [self._roaster, self._country, self._region, self._stars]
        )

    # saves newely added coffee to the .csv file
    def save(self):
        with open(self._file, "a") as f:
            writer = csv.writer(f)
            writer.writerows(self._new_coffee)

    # reads the .csv file and shows the result
    def show_coffee(self):
        print()
        # if there is no information on any coffee, tell the user to add one
        if len(self._old_coffee) < 2 and len(self._new_coffee) == 0:
            print("Enter a coffee first")
        # if there is information in the CSV but not new coffee print the old coffee
        elif len(self._old_coffee) > 2 and len(self._new_coffee) == 0:
            for row in self._old_coffee:
                print(f"{row[0]:13} {row[1]:13} {row[2]:13}  {row[3]:13}")
        # print both the old coffee and the new coffee
        else:
            for row in self._old_coffee:
                print(f"{row[0]:13} {row[1]:13} {row[2]:13}  {row[3]:13}")
            for row in self._new_coffee:
                print(f"{row[0]:13} {row[1]:13} {row[2]:13}  {row[3]:13}")
        print()


# defines main manu for CLI
def main_menu():
    print("Coffees of the world")
    print("\t1. Show Coffee")
    print("\t2. Add Coffee")
    print("\t3. Save and Quit")
    choice = int(input("Enter the number of your selection: "))
    return choice


# handles the user input
def perform_action(choice, coffee):
    if choice == 1:
        coffee.show_coffee()

    elif choice == 2:
        enter_coffee(coffee)

    elif choice == 3:
        quit(coffee)


# if choice is 2, this function is called
def enter_coffee(coffee):
    print()
    coffee.roaster = input("Enter the name of the roaster: ")
    coffee.country = input("Enter the name of the country: ")
    coffee.region = input("Enter the name of the region: ")
    coffee.stars = int(input("Enter the nunber of stars '*' (1-4): ")) * "*"
    print()
    coffee.add_coffee()


# defines the function for the user choice is quit
def quit(coffee):
    global run_loop  # variable run_loop as the global scope
    coffee.save()
    run_loop = False


# instantiation of the CoffeeJournal object
coffee = CoffeeJournal("test_coffeejournal.csv")

run_loop = True
file = "test_coffeejournal.csv"
my_coffee = CoffeeJournal(file)


# looping through the main_manu function
while run_loop:
    choice = main_menu()
    perform_action(choice, my_coffee)
