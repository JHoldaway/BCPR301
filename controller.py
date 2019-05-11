from module_builder.interpreter import Interpreter
import pickle
import sys
import tkinter as tk
from tkinter import filedialog
from cmd import *


class Controller(Cmd):
    """Controller class for python module builder."""

    prompt = ">>>"
    source_file = None
    module_directory = None

    def __init__(self):
        """Initialises the controller."""
        self.my_interpreter = Interpreter()
        self.the_window = None

    def _open_files(self):
        """Method for opening files from GUI"""
        input_file = filedialog.askopenfilename()
        output_directory = filedialog.askdirectory()
        self.my_interpreter.add_file(input_file, output_directory)
        self.my_interpreter.read_file()
        self.my_interpreter.write_modules()

    def go(self):
        """Defines the usual behaviour of the controller"""
        if len(sys.argv) == 1:
            self.my_interpreter.add_file("example.txt", "testmodule")
            self.my_interpreter.read_file()
            self.my_interpreter.write_modules()
        elif len(sys.argv) == 2 and "-?" in sys.argv or "/?" in sys.argv:
            sys.stdout.write("Converts pluntuml file to python module")
            sys.stdout.write("\n\ncontroller.py [input_file [output_location]]")
            sys.stdout.write("\n\nIf no parameters, the program runs an example version")
            sys.stdout.write("\ninput_file: the path of the file to use as input, defaults to example.txt")
            sys.stdout.write("\noutput_location: the location of the directory to output the module")
            sys.stdout.write("\n(defaults to testmodule)\n\n")
        elif len(sys.argv) == 2:
            try:
                filename = sys.argv[1]
                self.my_interpreter.add_file(filename, "testmodule")
                self.my_interpreter.read_file()
                self.my_interpreter.write_modules()
                # sys.stdout.write("success")
            except FileNotFoundError:
                sys.stdout.write("Error loading file, file does not exist.")
        elif len(sys.argv) == 3:
            try:
                file_to_read = sys.argv[1]
                module_name = sys.argv[2]
                self.my_interpreter.add_file(file_to_read, module_name)
                self.my_interpreter.read_file()
                self.my_interpreter.write_modules()
            except FileNotFoundError:
                sys.stdout.write("Error loading file or writing module, please check both inputs.")
        else:
            sys.stdout.write("Too many arguments")

    def go_tk(self):
        """Graphical version of the go method"""
        self.the_window = tk.Tk()
        menubar = tk.Menu(self.the_window)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open PlantUML File", command=self._open_files)
        file_menu.add_command(label="Exit", command=self.the_window.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.the_window.config(menu=menubar)
        self.the_window.mainloop()


    # def goload(self):
    #   self.myinterpreter.write_modules()

    def save_state(self, filename):
        """Uses pickle to save the state of the interpreter to filename"""
        try:
            the_file = open(filename, "wb")
            pickle.dump(self.my_interpreter, the_file)
            the_file.close()
        except pickle.PicklingError:
            print("Error with saving: Unpickleable object passed to pickler.")
        except FileNotFoundError:
            print("Error with saving: Directory does not exist")
        except:
            print("Unexpected error while saving")

    def load_state(self, filename):
        """Uses pickle to load saved state of the interpreter from filename"""
        try:
            the_file = open(filename, "rb")
            self.my_interpreter = pickle.load(the_file)
            the_file.close()
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

    def do_source(self, args):
        self.source_file = args
        print("Source file set.")

    def do_directory(self, args):
        self.module_directory = args
        print("Target directory set.")

    def do_interpret(self, args):
        if self.source_file is None:
            print("Sorry, please choose a source file.")
        elif self.module_directory is None:
            print("Sorry, please choose a directory.")
        else:
            the_interpreter = Interpreter()
            the_interpreter.add_file(self.source_file, self.module_directory)
            the_interpreter.write_modules()
            print("Files Interpreted")

    def do_quit(self, args):
        return True

    def help_source(self):
        print("""---
        Set the Source File
        Format: source [file]
        ---
        """)

    def help_directory(self):
        print("""---
        Set the module directory
        Format: directory [directory]
        ---
        """)

    def help_interpret(self):
        print("""---
        Interpret the files.
        Outputs to the directory set in the directory command.
        Processes the file set in the source command.
        Format: interpret
        ---
        """)


def main():
    my_controller = Controller()
    # my_controller.go_tk()
    # my_controller.go()
    # my_controller.save_state("save.p")

    my_controller.cmdloop()

    # mycontroller.load_state("save.p")
    # mycontroller.goload()


if __name__ == "__main__":
    main()


