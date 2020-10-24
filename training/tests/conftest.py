def pytest_addoption(parser):
    parser.addoption("--datafile", action="append", default=[],
        help="list of datafiles to pass to test functions")

def pytest_generate_tests(metafunc):
    if 'datafile' in metafunc.fixturenames:
        metafunc.parametrize("datafile",
                             metafunc.config.option.datafile)