import json
import sys
import File

argument = ""
try:
    argument = sys.argv[1]
except IndexError:
    pass
test= {}
data = {}
task_removed = []
new_data = []
reloaded_data = []
done_data = []

def reload_name():
    with open(File.file, "r") as f:
        dt = json.load(f)
    for items in dt:
        index = dt.index(items)
        items["name"] = index + 1
        reloaded_data.append(items)
    
    with open(File.file, "w") as f:
        json.dump(dt, f, indent=4)

def add():
    try:
        task = sys.argv[2]
    except IndexError:
        print("djtodo: empy argument")
        sys.exit()

    
    data = {'name': 0,'task': task, 'status': False}
    
    with open(File.file, "+r") as f:
        dt = json.load(f)
        dt.append(data)
        f.seek(0)
        json.dump(dt, f, indent=4)
    reload_name()

def ls():
    with open(File.file, "r", encoding='utf-8') as f:
        dt = json.load(f)
        for items in dt:
            if items["status"] == False:
                flag = "x"
                print("{} {} {}".format(flag, items["name"], items["task"]))
            else:
                flag = "o"
                print("{} {} {}".format(flag, items["name"], items["task"]))

def remove():
    try:
        name = sys.argv[2]
    except IndexError:
        print("djtodo: empy argument")
        sys.exit()
    
    with open(File.file, "r") as f:
        dt = json.load(f)

    for items in dt:
        if items["name"] != int(name):
            new_data.append(items)
            
    
    with open(File.file, "w") as f:
        json.dump(new_data, f, indent= 4)
    reload_name()

def done():
    try:
        status = sys.argv[2]
    except IndexError:
        print("djtodo: empy argument")
        sys.exit()
    
    with open(File.file, "r") as f:
        dt = json.load(f)
    
    for items in dt:
        if items["name"] == int(status):
            items["status"] = True
            done_data.append(items)
        else:
            done_data.append(items)
    
    with open(File.file, "w") as f:
        json.dump(done_data, f, indent=4)
        


