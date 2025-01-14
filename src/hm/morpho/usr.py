'''
Directory with user-specific information.
'''

import os

USER_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'usr')

def get_path_file():
    return os.path.join(USER_DIR, 'paths.txt')

def get_path(name):
    try:
        with open(get_path_file()) as file:
            for line in file:
                line = line.strip()
                if not line or line[0] == '#':
                    continue
                nm, path = line.split('=')
                nm = nm.strip()
                if nm == name:
                    return path.strip()
#        print("**Path for {} not found in path file!")
        return
    except IOError:
        print('**No paths file found!')

def write_path(name, path):
    try:
        with open(get_path_file(), 'a') as file:
            print("{} = {}".format(name, path), file=file)
        return
    except IOError:
        print('**No paths file found!')

def file_exists(path):
    return os.path.isfile(path)
        
        

            
    
