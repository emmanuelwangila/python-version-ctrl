# Python script for implementing version control like git 

# to handle file and directory operations
import os
import argparse
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
    
    os.mkdir(REPO_DIR); # make repo and sub directories 
    os.mkdir(os.path.join(REPO_DIR , "objects"));
    os.mkdir(os.path.join(REPO_DIR, "branches"));

    with open(os.path.join(REPO_DIR , "HEAD"), "w" )as file:
        file.write("main")

    with open(os.path.join(REPO_DIR, "index"), "w") as file:
        file.write("")

    print("Initialized an empty repository")    
def hash_content(content):
    '''Generate a SHA-1 hash for the content'''
    return hashlib.sha1(content.encode()).hexdigest() #hash the content   

def stage_file(filename):
    '''Stage the file for a commit'''
    if not  os.path.exists(filename):
        print(f"Error: {filename} does not exist") 
        return   

    with open(filename , "r") as file:
        content = file.read(); #read the file 
    file_hash = hash_content(content) #has the content

    # store file contents in the objects directory
    object_path = os.path.join(REPO_DIR , "objects", file_hash)
    with open(object_path , "w") as file:
        file.write(content) #write the content of the object path

    with open(os.path.join(REPO_DIR , "index"), "a") as file :
        file.write(f"File is in staging area {filename} : {file_hash}\n")   
    print("file stagged sucesfully", {filename})     

def commit(message):
    # function to define a commit
    index_path = os.path.join(REPO_DIR , "index")
    if not os.path.getsize(index_path):
        print("Nothing to commit")
        return
    with open(index_path , "r")as file:
        index = file.read() #read the contents of the file
    parent_commit = current_commit()

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
    with open(os.path.join(REPO_DIR , "HEAD"), "r") as file:
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
    """Display the commit history."""
    commit_hash = current_commit()
    if not commit_hash:
        print("No commits found.")
        return

    while commit_hash:
        commit_path = os.path.join(REPO_DIR, "objects", commit_hash)
        with open(commit_path, "r") as file:
            commit_content = json.load(file)

        print(f"Commit: {commit_hash}")
        print(f"Message: {commit_content['message']}")
        print(f"Timestamp: {time.ctime(commit_content['timestamp'])}")
        print()

        # Move to the parent commit
        commit_hash = commit_content["parent"]


def create_branch(branch_name):
    """Create a new branch."""
    current_commit = current_commit()
    branch_path = os.path.join(REPO_DIR, "branches", branch_name)

    if os.path.exists(branch_path):
        print(f"Branch {branch_name} already exists.")
        return

    with open(branch_path, "w") as file:
        file.write(current_commit)

    print(f"Created branch {branch_name}")


def checkout_branch(branch_name):
    """Switch to another branch."""
    branch_path = os.path.join(REPO_DIR, "branches", branch_name)

    if not os.path.exists(branch_path):
        print(f"Branch {branch_name} does not exist.")
        return

    with open(os.path.join(REPO_DIR, "HEAD"), "w") as file:
        file.write(branch_name)

    print(f"Switched to branch {branch_name}")


def clone_repo(source_path, destination_path):
    """Clone the repository to a new location."""
    if os.path.exists(destination_path):
        print(f"Destination {destination_path} already exists.")
        return

    shutil.copytree(source_path, destination_path)
    print(f"Cloned repository to {destination_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple version control system.")
    parser.add_argument("command", help="Command to run (init, add, commit, log, branch, checkout, clone)")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    
    args = parser.parse_args()

    if args.command == "init":
        initialize_repo()
    elif args.command == "add":
        if args.args:
            stage_file(args.args[0])
        else:
            print("Specify a file to add.")
    elif args.command == "commit":
        if args.args:
            commit(args.args[0])
        else:
            print("Specify a commit message.")
    elif args.command == "log":
        log()
    elif args.command == "branch":
        if args.args:
            create_branch(args.args[0])
        else:
            print("Specify a branch name.")
    elif args.command == "checkout":
        if args.args:
            checkout_branch(args.args[0])
        else:
            print("Specify a branch name to checkout.")
    elif args.command == "clone":
        if len(args.args) == 2:
            clone_repo(args.args[0], args.args[1])
        else:
            print("Specify source and destination paths for cloning.")
    else:
        print("Unknown command.")    