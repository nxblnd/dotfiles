# Dotfiles helper
abbr --add dotfiles "git --git-dir=\"$HOME/.config/dotfiles/\" --work-tree=\"$HOME\""

# Git
abbr --add gs "git status"
abbr --add ga "git add"
abbr --add gco "git checkout"

# Added proxy flags
if type -q sslocal
    set -l ssconfig "/etc/shadowsocks-rust/config.json"
    set -l parsed_config (jq -r .local_address,.local_port $ssconfig)
    set -l SSPROXY "socks5://$parsed_config[1]:$parsed_config[2]"
    abbr --add curlss "curl --proxy=$SSPROXY"
    abbr --add ytdlpss "yt-dlp --proxy=$SSPROXY"
end

# Pacman
abbr --add pacman-unlock "sudo rm /var/lib/pacman/db.lck"
abbr --add pacman-orphans "pacman -Qdtq | sudo pacman -Rns -"

# Docker
abbr --add docker-shell "docker run --rm -it --entrypoint /bin/sh"
