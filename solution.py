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
    
    os.makdir(REPO_DIR); # make repo and sub directories 
    os.makdir(os.path.join(REPO_DIR , "objects"));
    os.makdir(os.path.join(REPO_DIR, "branches"));

    with open(os.path.join(REPO_DIR , "HEAD"), "w" )as file:
        file.write("main")

    with open(os.path.join(REPO_DIR, "index"), "w") as file:
        file.write("")

    print("Initialized an empty repository")        

    
     


