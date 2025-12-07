if not type -q fisher && not test "$FISHER_INSTALL_STARTED"
    set -U FISHER_INSTALL_STARTED true
    curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
    fisher update
    set -e FISHER_INSTALL_STARTED
end
