'''
Directory with user-specific information.
'''

import os

USER_DIR = os.path.join(os.path.dirname(__file__), 'usr')

def get_path_file():
    return os.path.join(USER_DIR, 'paths.txt')

def get_path(name):
    try:
        with open(get_path_file()) as file:
            for line in file:
                nm, path = line.split('=')
                nm = nm.strip()
                if nm == name:
                    return path.strip()
        print("**Path for {} not found in path file!")
        return
    except IOError:
        print('**No paths file found!')



            
    
