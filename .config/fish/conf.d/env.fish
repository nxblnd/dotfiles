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
