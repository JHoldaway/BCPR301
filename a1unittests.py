import unittest
from module_builder.interpreter import Interpreter
import os
import controller

class BasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.myinterpreter = Interpreter()

    def test_add_class(self):
        self.myinterpreter.add_class("testclass", [], [], [])
        self.assertEqual(self.myinterpreter.all_my_classes[0].name, "testclass")

class SpecificFunctions(unittest.TestCase):
    def setUp(self):
        self.myinterpreter = Interpreter()
        self.myinterpreter.add_file("example.txt", "testmodule")
        self.myinterpreter.read_file()

    def test_classes_added(self):
        self.assertEqual(len(self.myinterpreter.all_my_classes), 4)

    def test_module_added(self):
        self.assertEqual(len(self.myinterpreter.all_my_modules), 1)

    def test_modulename(self):
        themodule = self.myinterpreter.all_my_modules[0]
        modulename = themodule.module_name
        self.assertEqual(modulename, "testmodule")

    def test_class_names(self):
        themodule = self.myinterpreter.all_my_modules[0]
        classnames = [i.name for i in themodule.all_my_classes]
        self.assertIn("ClassBuilder", classnames)
        self.assertIn("Attribute", classnames)
        self.assertIn("Method", classnames)
        self.assertIn("Relationship", classnames)

    def test_relationships(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "ClassBuilder"]
        self.assertEqual(len(theclass[0].all_my_composite_classes), 3)

    def test_methods(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "ClassBuilder"]
        self.assertEqual(len(theclass[0].all_my_methods), 4)

    def test_attributes(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "ClassBuilder"]
        self.assertEqual(len(theclass[0].all_my_attributes), 4)

    def test_methods_2(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "Method"]
        self.assertEqual(len(theclass[0].all_my_methods), 2)

    def test_attributes_2(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "Method"]
        self.assertEqual(len(theclass[0].all_my_attributes), 3)

    def test_makes_files(self):
        self.myinterpreter.write_modules()
        self.assertTrue(os.path.isfile("./testmodule/attribute.py"))
        self.assertTrue(os.path.isfile("./testmodule/classbuilder.py"))
        self.assertTrue(os.path.isfile("./testmodule/method.py"))
        self.assertTrue(os.path.isfile("./testmodule/relationship.py"))

    def test_class_representation(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "Attribute"]
        stringrep = theclass[0].print_class()
        self.assertRegex(stringrep, "class Attribute:")

    def test_classes_get_methods(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "Attribute"]
        stringrep = theclass[0].print_class()
        self.assertRegex(stringrep, "def __init__\(self\):")
        self.assertRegex(stringrep, "def find_type\(self, new_type\)")
        self.assertRegex(stringrep, "def __str__\(self\)")

    def test_classes_get_attributes(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "Attribute"]
        stringrep = theclass[0].print_class()
        self.assertRegex(stringrep, "self.name")
        self.assertRegex(stringrep, "self.type")

    def test_classes_get_relationships(self):
        themodule = self.myinterpreter.all_my_modules[0]
        theclass = [i for i in themodule.all_my_classes if i.name == "ClassBuilder"]
        stringrep = theclass[0].print_class()
        self.assertRegex(stringrep, "self.all_my_Attributes = \[\]")
        self.assertRegex(stringrep, "self.all_my_Methods = \[\]")
        self.assertRegex(stringrep, "self.all_my_Relationships = \[\]")

class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.mycontroller = controller.Controller()

    def test_controller_runs(self):
        try:
            self.mycontroller.go()
        except:
            self.fail("The controller raised an exception")

    def test_controller_saves(self):
        self.mycontroller.go()
        self.mycontroller.save_state("save.p")
        self.assertTrue(os.path.isfile("./save.p"))
    
    def test_controller_loads(self):
        self.mycontroller.go()
        self.mycontroller.save_state("save.p")
        self.mycontroller = controller.Controller()
        self.mycontroller.load_state("save.p")
        theinterpreter = self.mycontroller.myinterpreter
        self.assertEqual(len(theinterpreter.all_my_classes), 4)


if __name__ == '__main__':
    unittest.main()
