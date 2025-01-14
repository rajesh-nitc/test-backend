#!/bin/bash

set -e

# Install Zsh Autosuggestions plugin
OH_MY_ZSH_DIR="$HOME/.oh-my-zsh"
ZSH_CUSTOM="$OH_MY_ZSH_DIR/custom"
git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"

# Add plugins to .zshrc
sed -i "/^plugins=/c\plugins=("zsh-autosuggestions" "terraform" "gcloud" "git" "docker" "kubectl")" ~/.zshrc

# Set Zsh as the default shell for the 'vscode' user without using `chsh`
echo "$(which zsh)" >> ~/.bashrc

# Source .zshrc to apply changes immediately
zsh -c 'source ~/.zshrc'

echo "post_create script completed successfully!"
