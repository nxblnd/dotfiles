if type -q fnm && status is-interactive
    fnm env --use-on-cd --shell fish | source
end
