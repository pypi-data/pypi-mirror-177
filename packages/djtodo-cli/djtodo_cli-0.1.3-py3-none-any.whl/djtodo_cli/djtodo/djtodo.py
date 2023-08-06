import sys
from File import create_file
import module

create_file()


def command(argument):
    if argument == "add":
        module.add()

    if argument == "list" or argument == "ls":
        module.ls()

    if argument == "remove":
        module.remove()

    if argument == "done":
        module.done()
    
    if argument == "search":
        module.search()

def cli(args=None):
    
    if not args:
        argument = ""
        try:
            argument = sys.argv[1]
            command(argument)
        except IndexError:
            print("No argument")
            sys.exit()
