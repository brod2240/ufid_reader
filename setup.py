import sys, subprocess

MIN_PYTHON_VERSION = (3,10)

def verify_all():
    verify_python()
    verify_imports()

def verify_python():
    current_python_version = sys.version_info
    if current_python_version < MIN_PYTHON_VERSION:
        print(f"Current Python version {current_python_version.major}.{current_python_version.minor} is outdated.")
        print("Please update your Python version usng the following two lines:\nsudo apt update\nsudo apt install python3")
        sys.exit(1) 

def verify_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"]) # if ans != 0, then error and must install pip
    except subprocess.CalledProcessError:
        print("pip is not available. Please install pip first using the following two lines:\nsudo apt update\nsudo apt install python3-pip")
        sys.exit(1)

def verify_imports():
    verify_pip()
    # now that we know that pip is installed and usable, we can use it to download dependencies in requirements.txt

    try:
        with open('requirements.txt') as file: #use with to auto close file after reading requirements
            requirements = file.read().splitlines()

        subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements]) # *requirements splits tuple gotten from file and passes each argument seperately to pip install
        #check_call returns exception, can check if worked correctly (ie if except not entered we know it was successful)

    except FileNotFoundError:
        print("requirements.txt not found. Please make sure that the requirements.txt file is in the same directory as setup.py.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_all()