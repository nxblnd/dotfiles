pyenv init - | source
if status is-interactive
    abbr --add dotfiles git --git-dir="$HOME/.config/dotfiles/" --work-tree="$HOME"
end
