from . import backup, dump, dbapi, factory, hooks, regression, transactions, types, userfunctions

def load_tests(loader, tests, pattern):
    tests.addTests(loader.loadTestsFromModule(backup, pattern))
    tests.addTests(loader.loadTestsFromModule(dump, pattern))
    tests.addTests(loader.loadTestsFromModule(dbapi, pattern))
    tests.addTests(loader.loadTestsFromModule(factory, pattern))
    tests.addTests(loader.loadTestsFromModule(hooks, pattern))
    tests.addTests(loader.loadTestsFromModule(regression, pattern))
    tests.addTests(loader.loadTestsFromModule(transactions, pattern))
    tests.addTests(loader.loadTestsFromModule(types, pattern))
    tests.addTests(loader.loadTestsFromModule(userfunctions, pattern))
    return tests
