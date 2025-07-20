#!/bin/bash

# Function to run tests with specific configuration
run_tests() {
    local browser=$1
    local headless=$2
    local parallel=$3
    local description=$4
    
    echo "Running tests with configuration: $description"
    echo "Browser: $browser, Headless: $headless, Parallel: $parallel"
    echo "----------------------------------------"
    
    python run_tests.py --test-path tests/test_features.py \
        --browser "$browser" \
        ${headless:+--headless} \
        ${parallel:+--parallel "$parallel"}
    
    echo "----------------------------------------"
    echo ""
}

# Test Chrome configurations
run_tests "chrome" "" "" "Chrome - Normal mode"
run_tests "chrome" "--headless" "" "Chrome - Headless mode"
run_tests "chrome" "" "2" "Chrome - Parallel execution"
run_tests "chrome" "--headless" "2" "Chrome - Headless + Parallel"

# # Test Firefox configurations
# run_tests "firefox" "" "" "Firefox - Normal mode"
# run_tests "firefox" "--headless" "" "Firefox - Headless mode"
# run_tests "firefox" "" "2" "Firefox - Parallel execution"
# run_tests "firefox" "--headless" "2" "Firefox - Headless + Parallel"

# # Test Edge configurations
# run_tests "edge" "" "" "Edge - Normal mode"
# run_tests "edge" "--headless" "" "Edge - Headless mode"
# run_tests "edge" "" "2" "Edge - Parallel execution"
# run_tests "edge" "--headless" "2" "Edge - Headless + Parallel"