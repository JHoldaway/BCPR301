import unittest
from module_builder.interpreter import Interpreter
import os
import controller

class BasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.my_interpreter = Interpreter()

    def test_add_class(self):
        self.my_interpreter.add_class("testclass", [], [], [])
        self.assertEqual(self.my_interpreter.all_my_classes[0].name, "testclass")

class SpecificFunctions(unittest.TestCase):
    def setUp(self):
        self.my_interpreter = Interpreter()
        self.my_interpreter.add_file("example.txt", "testmodule")
        self.my_interpreter.read_file()

    def test_classes_added(self):
        self.assertEqual(len(self.my_interpreter.all_my_classes), 4)

    def test_module_added(self):
        self.assertEqual(len(self.my_interpreter.all_my_modules), 1)

    def test_modulename(self):
        the_module = self.my_interpreter.all_my_modules[0]
        module_name = the_module.module_name
        self.assertEqual(module_name, "testmodule")

    def test_class_names(self):
        the_module = self.my_interpreter.all_my_modules[0]
        class_names = [i.name for i in the_module.all_my_classes]
        self.assertIn("ClassBuilder", class_names)
        self.assertIn("Attribute", class_names)
        self.assertIn("Method", class_names)
        self.assertIn("Relationship", class_names)

    def test_relationships(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "ClassBuilder"]
        self.assertEqual(len(the_class[0].all_my_composite_classes), 3)

    def test_methods(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "ClassBuilder"]
        self.assertEqual(len(the_class[0].all_my_methods), 4)

    def test_attributes(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "ClassBuilder"]
        self.assertEqual(len(the_class[0].all_my_attributes), 4)

    def test_methods_2(self):
        themodule = self.my_interpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "Method"]
        self.assertEqual(len(theclass[0].all_my_methods), 2)

    def test_attributes_2(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "Method"]
        self.assertEqual(len(the_class[0].all_my_attributes), 3)

    def test_makes_files(self):
        self.my_interpreter.write_modules()
        self.assertTrue(os.path.isfile("./testmodule/attribute.py"))
        self.assertTrue(os.path.isfile("./testmodule/classbuilder.py"))
        self.assertTrue(os.path.isfile("./testmodule/method.py"))
        self.assertTrue(os.path.isfile("./testmodule/relationship.py"))

    def test_class_representation(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "Attribute"]
        stringrep = the_class[0].print_class()
        self.assertRegex(stringrep, "class Attribute:")

    def test_classes_get_methods(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "Attribute"]
        stringrep = the_class[0].print_class()
        self.assertRegex(stringrep, "def __init__\(self\):")
        self.assertRegex(stringrep, "def find_type\(self, new_type\)")
        self.assertRegex(stringrep, "def __str__\(self\)")

    def test_classes_get_attributes(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "Attribute"]
        stringrep = the_class[0].print_class()
        self.assertRegex(stringrep, "self.name")
        self.assertRegex(stringrep, "self.type")

    def test_classes_get_relationships(self):
        the_module = self.my_interpreter.all_my_modules[0]
        the_class = [i for i in the_module.all_my_classes if i.name == "ClassBuilder"]
        stringrep = the_class[0].print_class()
        self.assertRegex(stringrep, "self.all_my_Attributes = \[\]")
        self.assertRegex(stringrep, "self.all_my_Methods = \[\]")
        self.assertRegex(stringrep, "self.all_my_Relationships = \[\]")

class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.my_controller = controller.Controller()

    def test_controller_runs(self):
        try:
            self.my_controller.go()
        except:
            self.fail("The controller raised an exception")

    def test_controller_saves(self):
        self.my_controller.go()
        self.my_controller.save_state("save.p")
        self.assertTrue(os.path.isfile("./save.p"))
    
    def test_controller_loads(self):
        self.my_controller.go()
        self.my_controller.save_state("save.p")
        self.my_controller = controller.Controller()
        self.my_controller.load_state("save.p")
        the_interpreter = self.my_controller.my_interpreter
        self.assertEqual(len(the_interpreter.all_my_classes), 4)


if __name__ == '__main__':
    unittest.main()
