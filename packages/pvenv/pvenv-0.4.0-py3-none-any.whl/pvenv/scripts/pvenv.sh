function venv {
    case "$1" in
    in)
        invenv "${@:2}"
        ;;
    out)
        outvenv "${@:2}"
        ;;
    activate)
        avenv "${@:2}"
        ;;
    deactivate)
        dvenv "${@:2}"
        ;;
    list)
        lsvenv "${@:2}"
        ;;
    make)
        mkvenv "${@:2}"
        ;;
    rm)
        rmvenv "${@:2}"
        ;;
    *)
        pvenv "$@"
        return
        ;;
    esac
}

function invenv {
    local IFS=$'\n'
    for command in $(pvenv in "$@"); do
        eval "${command}"
    done
}

function outvenv {
    local IFS=$'\n'
    for command in $(pvenv out); do
        eval "${command}"
    done
}

function avenv {
    local IFS=$'\n'
    for command in $(pvenv activate "$@"); do
        eval "${command}"
    done
}

function dvenv {
    local IFS=$'\n'
    for command in $(pvenv deactivate "$@"); do
        eval "${command}"
    done
}

function lsvenv {
    pvenv list "$@"
}

function mkvenv {
    local IFS=$'\n'
    for command in $(pvenv make "$@"); do
        eval "${command}"
    done
}

function rmvenv {
    pvenv rm "$@"
}
