# Dotfiles

Using bare git repo method

https://wiki.archlinux.org/title/Dotfiles

## How to use

In fish, use abbreviation `dotfiles` to manipulate repo.

Setup dotfiles with this command:
```sh
git clone --bare git@github.com:nxblnd/dotfiles.git $HOME/.config/dotfiles && \
git --git-dir="$HOME/.config/dotfiles" --work-tree="$HOME" config --local status.showUntrackedFiles no && \
git --git-dir="$HOME/.config/dotfiles" --work-tree="$HOME" sparse-checkout set --no-cone '/*' '!README.md' && \
git --git-dir="$HOME/.config/dotfiles" --work-tree="$HOME" checkout
```
