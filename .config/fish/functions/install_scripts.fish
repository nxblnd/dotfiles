#!/usr/bin/env fish

function prepare_directories
    if not test -d "$LOCAL_BIN"
        mkdir "$LOCAL_BIN"
    end

    if not test -d "$LOCAL_SCRIPTS"
        echo "$LOCAL_SCRIPTS not found"
        return 1
    end
end

function install_scripts
    prepare_directories

    for script in "$LOCAL_SCRIPTS"/*
        if string match -q "#!*" (head -n1 "$script")
            string match -rq '^(?<filename>.*)(?<ext>\.[^.]*)$' (basename "$script")
            set symlink "$LOCAL_BIN/$filename"

            if test -L "$symlink"
                echo "$filename" already exists
                continue
            end

            ln -s "$script" "$symlink"
            echo "$filename symlinked"
        end
    end
end
