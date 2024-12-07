# Python script for implementing version control like git 

# to handle file and directory operations
import os
import shutil #to handle directory copying
import time # to handle timestamps
import hashlib # to generate hash commits 
import json # for handling commits and data 

REPO_DIR = ".pygit"; #Repo directory 

def initialize_repo():
    '''' Initiliaze a new repository'''
    if os.path.exists(REPO_DIR):
        print("Error: repository already exists")
        return

