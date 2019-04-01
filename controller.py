from module_builder.interpreter import Interpreter
import pickle


class Controller:

    def __init__(self):
        self.myinterpreter = Interpreter()

    def go(self):
        self.myinterpreter.add_file("example.txt", "testmodule")
        self.myinterpreter.read_file()
        self.myinterpreter.write_modules()

    # def goload(self):
    #   self.myinterpreter.write_modules()

    def save_state(self, filename):
        try:
            thefile = open(filename, "wb")
            pickle.dump(self.myinterpreter, thefile)
            thefile.close()
        except pickle.PicklingError:
            print("Error with saving: Unpickleable object passed to pickler.")
        except FileNotFoundError:
            print("Error with saving: Directory does not exist")
        except:
            print("Unexpected error while saving")

    def load_state(self, filename):
        try:
            thefile = open(filename, "rb")
            self.myinterpreter = pickle.load(thefile)
            thefile.close()
        except pickle.UnpicklingError:
            print("Error loading file: Issue with file format")
        except AttributeError:
            print("Error loading file: Attribute Error encountered while loading")
        except EOFError:
            print("Error loading file: End Of File Error")
        except ImportError:
            print("Error loading file: Imported module not found")
        except IndexError:
            print("Error loading file: Index out of range")
        except FileNotFoundError:
            print("Error loading file: File does not exist")
        except:
            print("Unexpected error while loading")


def main():
    mycontroller = Controller()
    mycontroller.go()
    mycontroller.save_state("save.p")
    # mycontroller.load_state("save.p")
    # mycontroller.goload()


if __name__ == "__main__":
    main()


