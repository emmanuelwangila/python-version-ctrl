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
def hash_content(content):
    '''Generate a SHA-1 hash for the content'''
    return hashlib.sha1(content.encode().hexdigest());   

def stage_file(filename):
    '''Stage the file for a commit'''
    if not  os.path.exists(filename):
        print(f"Error: ${filename} does not exist") 
        return   

    with open(filename , "r") as file:
        content = file.read(); #read the file 
    file_hash = hash_content(content) #has the content

    # store file contents in the objects directory
    object_path = os.path.join(REPO_DIR , "objects", file_hash)
    with open(object_path , "w") as file:
        file.write(content) #write the content of the object path

    with open(os.path.join(REPO_DIR , "index"), "a") as file :
        file.write(f"File is in staging area ${filename} : {file_hash}\n")   
    print("file stagged sucesfully", {filename})     

def commit(message):
    # function to define a commit
    index_path = os.path.join(REPO_DIR , "index")
    if not os.path.getsize(index_path):
        print("Nothing to commit")
        return
    with open(index_path , "r")as file:
        index = file.read
    parent_commit = get_current_commit()

    # commit object with metadata
    commit_content = {
        "parent": parent_commit,
        "message":message,
        "timestamp":time.time(),
        "files":index.strip().split("\n")
    }  
    commit_hash = hash_content(json.dumps(commit_content)); #commit hash for the commit
    with open(commit_hash , "w") as file:
        json.dump(commit_content , file) #save the file commit as a json
    current_branch = get_current_branch() 
    branch_path = os.path.join(REPO_DIR , "branches", current_branch)
    with open(branch_path , "w") as file:
        file.write(commit_hash)

     #clear the branch 
    with open(index_path , "w") as file:
        file.write("clear")
        print(f"Commited with {commit_hash}")

def get_current_branch():
    '''Define name of the current branch '''
    with open(os.path.join(REPO_DIR , "HEAD"), "w") as file:
        return file.read().strip() # read the file and remove white_spaces 
    
def current_commit():
    '''Define name of current commit'''
    current_branch = get_current_branch()
    branch_path = os.path.join(REPO_DIR , "current_branch", current_branch)
    # open file of currennt branch 
    
    if not os.path.exists(branch_path):
        return None
    
    with open(branch_path , "r") as file:
        return file.read().strip() #read the file and remove white spaces 
def log():
    '''Display the commit history'''
    commit_harsh = get_current_commit()
    if commit_harsh is None:
        return None
    print ("No current commits were found")
     
    while  commit_harsh:
        commit_path = os.path.join(REPO_DIR ,  "objects", commit_harsh)
        with open(commit_path , "r") as file:
            commit_content = json.load(file) #load the file commit as json    


