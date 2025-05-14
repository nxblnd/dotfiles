pyenv init - | source
if status is-interactive
    abbr --add dotfiles git --git-dir="$HOME/.config/dotfiles/" --work-tree="$HOME"
    abbr --add ls eza -lAb --git --git-repos

    set -gx MANPAGER 'nvim +Man!'
end
