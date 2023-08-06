import os


os.mkdir("allure_report")
os.mkdir("data")
os.mkdir("fixture")
os.mkdir("generator")
os.mkdir("locators")
os.mkdir("pages")
os.mkdir("test")


def dir_data():
    init = open("data/__init__.py", "w+")
    init.close()
    db_data = open("data/db_data.json", "w+")
    db_data.close()
    pages_text = open("data/pages_text.py", "w+")
    pages_text.close()


def dir_fixture():
    init = open("fixture/__init__.py", "w+")
    init.close()
    data_application = open("fixture/application.py", "w+")
    data_application.close()
    data_session = open("fixture/session.py", "w+")
    data_session.close()

def dir_generator():
    init = open("generator/__init__.py", "w+")
    init.close()
    data_generator = open("generator/generate_data.py", "w+")
    data_generator.close()
    data_read_data = open("generator/read_data.py", "w+")
    data_read_data.close()


def dir_locators():
    init = open("locators/__init__.py", "w+")
    init.close()
    data_locators = open("locators/example_locators.py", "w+")
    data_locators.close()

def dir_pages():
    init = open("pages/__init__.py", "w+")
    init.close()
    init = open("pages/PO_example.py", "w+")
    init.close()

def dir_test():
    init = open("test/__init__.py", "w+")
    init.close()
    testExample = open("test/testExample.py", "w+")
    testExample.close()

def dir_main():
    conftest = open("conftest.py", "w+")
    conftest.close()
    requirements = open("requirements.txt", "w+")
    requirements.close()
    target = open("target.json", "w+")
    target.close()

def startapp():
    dir_data()
    dir_fixture()
    dir_generator()
    dir_locators()
    dir_pages()
    dir_test()
    dir_main()








