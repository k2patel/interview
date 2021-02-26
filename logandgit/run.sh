#!/bin/sh

set -eu

run_test_case() {
    local problem="$1"
    local case_number="$2"
    echo
    echo "Running problem $problem, test case $case_number..."
    local input="test_data/$case_number-input"
    local output="test_data/$case_number-output"
    local log="test_data/$case_number-log"
    docker run -i "mozilla-sre-interview/$problem" < "$input" > "$log"
    if diff "$log" "$output"; then
        echo "succeeded."
    else
        echo "FAILED."
    fi
}

run_tests() {
    cd "$1"
    local problem="$(basename $PWD)"
    echo
    echo "===== Problem $problem ====="
    echo "Building Docker image..."
    docker build . -t "mozilla-sre-interview/$problem"
    for input in test_data/*-input; do
        local case_number="${input##*/}"
        case_number="${case_number%-input}"
        run_test_case "$problem" "$case_number"
    done
    cd "$OLDPWD"
}

if [ $# -lt 1 ]; then
    if [ -e Dockerfile ]; then
        set .
    else
        set "$(dirname $0)"/problem*
    fi
fi
if [ "$1" = --help ]; then
    echo "Usage:"
    echo "    $0 <PROBLEM_DIR> ..."
    echo "        runs all test cases in the listed problem directories."
    echo "    $0"
    echo "        without arguments runs the test cases for all problems when called at the"
    echo "        root level, or the current problem when called inside one of the problem"
    echo "        directories."
    exit
fi
for problem in "$@"; do
    run_tests "$problem"
done
