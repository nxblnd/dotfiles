# ls & alternatives
if type -q eza
    function ls --wraps eza
        eza --long --almost-all --binary --smart-group --group-directories-first --git --git-repos --color=auto --icons=never $argv
    end

    function lss --wraps eza --description "ls with total dir size"
        ls --total-size $argv
    end
end

function goto
    if test -d $argv[1]
        cd $argv[1]
    end

    mkdir -p $argv[1] && cd $argv[1]
end

function gitinit -a name
    if test -z "$name"
        set name "./"
    end

    goto $name

    git init
    git commit -m "Initial commit" --allow-empty
end
