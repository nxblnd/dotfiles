# Dotfiles helper
abbr --add dotfiles "git --git-dir=\"$HOME/.config/dotfiles/\" --work-tree=\"$HOME\""

# Git
abbr --add gs "git status"
abbr --add ga "git add"
abbr --add gco "git checkout"

# Added proxy flags
set -l ssconfig "/etc/shadowsocks-rust/config.json"
set -l SSPROXY "socks5://$(jq -r .local_address $ssconfig):$(jq -r .local_port $ssconfig)"
abbr --add curlss "curl --proxy=$SSPROXY"
abbr --add ytdlpss "yt-dlp --proxy=$SSPROXY"

# Pacman
abbr --add pacman-unlock "sudo rm /var/lib/pacman/db.lck"
abbr --add pacman-orphans "pacman -Qdtq | sudo pacman -Rns -"
