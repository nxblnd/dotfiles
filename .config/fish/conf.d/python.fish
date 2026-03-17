if type -q pyenv && status is-interactive
    pyenv init - | source
end

set -x PYTHONSTARTUP "$XDG_CONFIG_HOME/pythonrc.py"
set -x PYTHONHISTORY "$XDG_STATE_HOME/python_history"
set -x IPYTHONDIR "$XDG_CONFIG_HOME/ipython"
set -x JUPITER_CONFIG_DIR "$XDG_CONFIG_HOME/jupyter"
set -x PYENV_ROOT "$XDG_DATA_HOME/pyenv"
