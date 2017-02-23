#!/bin/bash

ENV_NAME='mbta-env'

create_env() {
    echo "Creating environment '$ENV_NAME'"
    python3 -m venv --without-pip "$ENV_NAME"
    source "$ENV_NAME/bin/activate"
    # TODO - find a better workaround for broken pyvenv
    curl https://bootstrap.pypa.io/get-pip.py | python3
    deactivate
    echo "Environment '$ENV_NAME' created."
}

main() {
    command -v python3 >/dev/null 2>&1 || { echo >&2 "I require python3 but it's not installed.  Aborting."; exit 1; }
    let python_major_version="$(python3 -c 'import sys; print(sys.version_info[0])')"
    let python_minor_version="$(python3 -c 'import sys; print(sys.version_info[1])')"
    if [[ "$python_major_version" -ne "3" || "$python_minor_version" -lt "4" ]]; then
        echo "This project is dependent on python3.4, but you're using $python_major_version . $python_minor_version"
        exit 1
    fi
    if [ ! -d "$ENV_NAME" ]; then
        create_env
    fi
    source "$ENV_NAME/bin/activate"
    # HACK: In some cases the shebang in pip can be too long, which
    # cases it to throw a 'bad interpreter'.  By running
    # pip directly through python, we bypass the shebang.
    python3 -m pip install -r requirements.txt >/dev/null
}
main
