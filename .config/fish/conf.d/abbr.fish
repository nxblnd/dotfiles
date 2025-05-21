# Dotfiles helper
abbr --add dotfiles "git --git-dir=\"$HOME/.config/dotfiles/\" --work-tree=\"$HOME\""

# Git
abbr --add gs "git status"
abbr --add ga "git add"
abbr --add gco "git checkout"

# ls & alternatives
abbr --add ls "eza -lAb --git --git-repos"

# Added proxy flags
set SSPROXY 'socks5://localhost:1080'
abbr --add curlss "curl --proxy=$SSPROXY"
abbr --add ytdlpss "yt-dlp --proxy=$SSPROXY"
