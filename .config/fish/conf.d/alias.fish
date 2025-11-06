# ls & alternatives
if type -q eza
    function ls --wraps eza
        eza --long --almost-all --binary --smart-group --group-directories-first --git --git-repos --color=auto --icons=never
    end

    function lss --wraps eza --description "ls with total dir size"
        ls --total-size
    end
end

