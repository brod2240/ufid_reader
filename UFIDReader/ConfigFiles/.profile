# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.   a
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi


# FOR RUNNING UFID READER OFF BOOT: 

#default location
if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
    cd ~/ufid_reader
    #git pull # make sure project is up to date

    cd UFIDReader

    if [ -f "ConfigFiles/.profile" ] && [ -f "ConfigFiles/.xinitrc" ]; then
        cp ConfigFiles/.profile ~/.profile
        cp ConfigFiles/.xinitrc ~/.xinitrc
    fi
    
    if [ ! -d "venv" ]; then # checks if the virtual env folder exists or not before creating. If there already, skip init
        python -m venv venv # creates virtual python folder where the required dependencies are installed. 
        # Mostly done to allow for running pip install without need for user confirmation in command line.
    fi 

    source venv/bin/activate # begin using created virtual env
    python src/setup.py # verify dependencies in requirements.txt are installed and are the proper version. Also verifies pip and the proper python version is installed
    startx
fi


# testing
# if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
#     cd ~/new//ufid_reader
#     python -m venv venv
#     source venv/bin/activate
#     cd ~/new/ufid_reader/GUI
#     python setup.py
#     startx
# fi
