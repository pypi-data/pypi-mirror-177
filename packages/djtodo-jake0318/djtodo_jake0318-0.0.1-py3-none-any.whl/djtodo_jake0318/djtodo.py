import sys
import File
import module

File.create_file()
argument = ""
try:
    argument = sys.argv[1]
except IndexError:
    pass


if argument == "add":
    module.add()

if argument == "list" or argument == "ls":
    module.ls()

if argument == "remove":
    module.remove()

if argument == "done":
    module.done()