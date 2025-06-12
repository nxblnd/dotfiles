# Dotfiles helper
abbr --add dotfiles "git --git-dir=\"$HOME/.config/dotfiles/\" --work-tree=\"$HOME\""

# Git
abbr --add gs "git status"
abbr --add ga "git add"
abbr --add gco "git checkout"

# Added proxy flags
set SSPROXY 'socks5://localhost:1080'
abbr --add curlss "curl --proxy=$SSPROXY"
abbr --add ytdlpss "yt-dlp --proxy=$SSPROXY"

# Pacman
abbr --add pacman-unlock "sudo rm /var/lib/pacman/db.lck"
abbr --add pacman-orphans "pacman -Qdtq | sudo pacman -Rns -"
