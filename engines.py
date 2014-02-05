import traceback
from util import *
import importlib

class DefaultLoader(object):
    def __init__(self):
        self.fixtures = {}
    def load(self, name):
        org_name = name

        fixture = self.fixtures.get(name)
        if fixture:
            print 'already exists, return'
            return fixture

        print 'DefaultLoader.load'
        try:
            module = self.do_load(name)
        except ImportError, inst:
            a = traceback.format_exc()
            print '{\n%s}' % inst.value
        names = name.split('.')[1:]
        for name in names:
            module = getattr(module, name)
        fixture = getattr(module, name)()
        self.fixtures[org_name] = fixture
        return fixture

    def do_load(self, name):
        return __import__(name)

class StringLoader(DefaultLoader):
    def __init__(self, script):
        self.script = script
    def load(self, name):
        x = compile(self.script, 'not_a_file.py', 'exec')
        return eval(x)
        return x
            
class Summary(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.right = 0
        self.wrong = 0
        self.ignored = 0
        self.exceptions = 0
        
class Engine(object):
    
    # return the next object in the flow or None.
    # check if fixture has attribute with name of next table.
    # if not create an instance with that name
    def __init__(self):
        self.loader = DefaultLoader()
        self.fixture = None
        self.print_traceback = False
        self.adapters = DefaultAdapters()
        self.summary = Summary()

    def do_process(self, table):
        name = table.name()
        try:
            return_table = getattr(self.fixture, name)
            self.fixture = return_table()
            self.fixture.process(table)
            return
        except AttributeError:
            pass

        self.fixture = self.loader.load(name)
        self.fixture.engine = self #hack
        self.fixture.process(table)

    def process(self, table, throw = True):
        name = table.name()
        if throw == True:
            self.do_process(table)
        else:
            try:
                self.do_process(table)
            except Exception, inst:
                '''Fixme: Should the rest of the table become grey?'''

                table.cell(0,0).error(inst)
                if self.print_traceback:
                    print 'Processing table `%s` failed' % table.name()
                    print '====='
                    print traceback.format_exc()
                    print '====='
        
        return self.fixture

    def compare(self, cell, actual_value):
        expected_value = str(cell)
        target_type = type(actual_value)
        if self.adapters.has_key(target_type):
            adapter = self.adapters[target_type]
            expected = adapter.convert(expected_value)
        else:
            expected = type(actual_value)(expected_value)

        if expected == actual_value:
            cell.passed()
            self.summary.right += 1
        else:
            cell.failed(actual_value)
            self.summary.wrong += 1
