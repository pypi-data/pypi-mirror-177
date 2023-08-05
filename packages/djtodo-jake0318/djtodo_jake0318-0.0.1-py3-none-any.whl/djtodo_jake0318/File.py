import os
from pathlib import Path
import getpass
import shutil
import pickle

username = getpass.getuser()
base = Path("/home/{}/.config/".format(username))
folder = Path("{}/djtodo".format(base))
file = Path("{}/djtodo/task.json".format(base))

def create_file():
    if not folder.is_dir():
            os.mkdir(folder)
    if not file.is_file(): 
            shutil.copy('task.json', file)
            pickle.dump(1, open("VSF.dat","wb"))


