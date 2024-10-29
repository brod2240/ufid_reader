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
    git pull
    python -m venv venv
    source venv/bin/activate
    cd ~/new/ufid_reader/GUI
    python setup.py
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
