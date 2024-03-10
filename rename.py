import os
import random
import string

def generateRandomName(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def renameImages(path):
    files = os.listdir(path)

    for oldName in files:
        _, ext = os.path.splitext(oldName)
        newName = generateRandomName() + ext
        os.rename(os.path.join(path, oldName), os.path.join(path, newName))

