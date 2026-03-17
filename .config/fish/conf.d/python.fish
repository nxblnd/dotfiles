if type -q pyenv && status is-interactive
    pyenv init - | source
end

set -x PYTHONSTARTUP "$XDG_CONFIG_HOME/pythonrc.py"
