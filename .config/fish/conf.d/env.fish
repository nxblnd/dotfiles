set -x EDITOR 'nvim'
set -x VISUAL 'nvim'
set -x MANPAGER 'nvim +Man!'
set -x BROWSER 'firefox'
set -x SUDO_PROMPT '[sudo] password for %p: ' # Adds bell to sudo prompt
set -x SSH_AUTH_SOCK "$XDG_RUNTIME_DIR/ssh-agent.socket"

set -x LOCAL_BIN "$HOME/.local/bin"
set -x LOCAL_SCRIPTS "$HOME/.local/scripts"

set -x XDG_DATA_HOME "$HOME/.local/share"
set -x XDG_CONFIG_HOME "$HOME/.config"
set -x XDG_STATE_HOME "$HOME/.local/state"
set -x XDG_CACHE_HOME "$HOME/.cache"

# based on xdg-ninja recommendations
set -x ANSIBLE_HOME "$XDG_DATA_HOME/ansible"
set -x HITSFILE "$XDG_STATE_HOME/bash/history"
set -x CARGO "$XDG_DATA_HOME/cargo"
set -x CUDA_CACHE_PATH "$XDG_CACHE_HOME/nv"
set -x DOCKER_CONFIG "$XDG_CONFIG_HOME/docker"
set -x DOTNET_CLI_HOME "$XDG_DATA_HOME/dotnet"
set -x GOPATH "$XDG_DATA_HOME/go"
set -x GRADLE_USER_HOME "$XDG_DATA_HOME/gradle"
set -x GTK2_RC_FILES "$XDG_CONFIG_HOME/gtk-2.0/gtkrc"
set -x IPYTHONDIR "$XDG_CONFIG_HOME/ipython"
set -x JUPITER_CONFIG_DIR "$XDG_CONFIG_HOME/jupyter"
set -x NODE_REPL_HISTORY "$XDG_DATA_HOME/node_repl_history"
set -x NPM_CONFIG_USERCONFIG "$XDG_CONFIG_HOME/npm/npmrc"
set -x NUGET_PACKAGES "$XDG_CACHE_HOME/NuGetPackages"
set -x PYENV_ROOT "$XDG_DATA_HOME/pyenv"
set -x TEXMFVAR "$XDG_CACHE_HOME/texlive/texmf-var"
set -x VAGRANT_HOME "$XDG_DATA_HOME/vagrant"
set -x WINEPREFIX "$XDG_DATA_HOME/wine"
