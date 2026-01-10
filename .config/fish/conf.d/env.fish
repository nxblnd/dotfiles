set -x EDITOR 'nvim'
set -x VISUAL 'nvim'
set -x MANPAGER 'nvim +Man!'
set -x BROWSER 'firefox'
set -x SUDO_PROMPT '[sudo] password for %p: ' # Adds bell to sudo prompt
set -x SSH_AUTH_SOCK "$XDG_RUNTIME_DIR/ssh-agent.socket"

set -x LOCAL_BIN "$HOME/.local/bin"
set -x LOCAL_SCRIPTS "$HOME/.local/scripts"
