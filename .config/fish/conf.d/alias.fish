# ls & alternatives
if type -q eza
    alias ls "eza --long --almost-all --binary --smart-group --group-directories-first --git --git-repos --color=auto --icons=never"
    alias lss "ls --total-size"
end
