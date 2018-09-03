# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
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

# p4c binaries
P4C_BUILD_DIR="$HOME/p4c/build"

# klee binaries
KLEE_BIN_DIR="$HOME/klee-build/klee/Release+Asserts/bin"
LLVM_BIN_DIR="$HOME/klee-build/llvm/Release/bin"

# set PATH so it includes user's private bin directories
PATH="$P4C_BUILD_DIR:$KLEE_BIN_DIR:$LLVM_BIN_DIR:$HOME/bin:$HOME/.local/bin:$PATH"