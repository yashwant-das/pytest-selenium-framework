#!/bin/bash

# ===============================================================================
# Enhanced Test Script for Comprehensive Framework Testing
# ===============================================================================
# 
# This script provides comprehensive testing capabilities for the pytest-selenium
# framework with the following enhancements:
#
# 🚀 FEATURES:
# - Colored output for better readability
# - Command-line argument support for flexible testing
# - Automatic Python executable detection (python3/python)
# - Error tracking and comprehensive reporting
# - System check integration with optional skip
# - Quick mode for faster basic testing
# - Browser-specific testing (Chrome, Firefox, Edge)
# - Test execution timing and summary statistics
#
# 📋 USAGE EXAMPLES:
# ./test_all_features.sh                  # Run all tests with all browsers
# ./test_all_features.sh --chrome-only    # Run only Chrome tests
# ./test_all_features.sh --quick          # Run basic tests only (faster)
# ./test_all_features.sh --no-system-check # Skip system validation
# ./test_all_features.sh --help          # Show usage information
#
# 🔧 COMPATIBILITY:
# - Works with Python 3.x environments
# - Supports both conda and venv environments
# - Cross-platform shell script (macOS, Linux)
# - Integrates with existing pytest-selenium framework
#
# ===============================================================================

set -e  # Exit on any error

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
START_TIME=$(date +%s)

# Configuration variables (can be overridden by command line)
RUN_CHROME=true
RUN_FIREFOX=true
RUN_EDGE=true
RUN_SYSTEM_CHECK=true
QUICK_MODE=false

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --chrome-only       Run only Chrome tests"
    echo "  --firefox-only      Run only Firefox tests"
    echo "  --edge-only         Run only Edge tests"
    echo "  --no-system-check   Skip system environment check"
    echo "  --quick             Run only basic configurations (faster)"
    echo "  --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                  # Run all tests with all browsers"
    echo "  $0 --chrome-only    # Run only Chrome tests"
    echo "  $0 --quick          # Run basic tests only"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --chrome-only)
            RUN_CHROME=true
            RUN_FIREFOX=false
            RUN_EDGE=false
            shift
            ;;
        --firefox-only)
            RUN_CHROME=false
            RUN_FIREFOX=true
            RUN_EDGE=false
            shift
            ;;
        --edge-only)
            RUN_CHROME=false
            RUN_FIREFOX=false
            RUN_EDGE=true
            shift
            ;;
        --no-system-check)
            RUN_SYSTEM_CHECK=false
            shift
            ;;
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO") echo -e "${BLUE}[INFO]${NC} $message" ;;
        "SUCCESS") echo -e "${GREEN}[SUCCESS]${NC} $message" ;;
        "WARNING") echo -e "${YELLOW}[WARNING]${NC} $message" ;;
        "ERROR") echo -e "${RED}[ERROR]${NC} $message" ;;
    esac
}

# Function to run tests with specific configuration
run_tests() {
    local browser=$1
    local headless=$2
    local parallel=$3
    local description=$4
    local extra_args=$5
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    print_status "INFO" "Running tests with configuration: $description"
    echo "Browser: $browser, Headless: $headless, Parallel: $parallel"
    echo "----------------------------------------"
    
    # Build command with optional arguments
    local python_cmd
    python_cmd=$(detect_python) || return 1
    
    local cmd="$python_cmd run_tests.py --test-path tests/test_features.py --browser $browser"
    [[ -n "$headless" ]] && cmd="$cmd --headless"
    [[ -n "$parallel" ]] && cmd="$cmd --parallel $parallel"
    [[ -n "$extra_args" ]] && cmd="$cmd $extra_args"
    
    print_status "INFO" "Executing: $cmd"
    
    if eval "$cmd"; then
        print_status "SUCCESS" "Test configuration passed: $description"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_status "ERROR" "Test configuration failed: $description"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    
    echo "----------------------------------------"
    echo ""
}

# Function to detect Python executable
detect_python() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        print_status "ERROR" "No Python executable found"
        return 1
    fi
}

# Function to run system check
run_system_check() {
    local python_cmd
    python_cmd=$(detect_python) || return 1
    
    print_status "INFO" "Running system environment check..."
    if $python_cmd run_system_check.py; then
        print_status "SUCCESS" "System check passed"
        return 0
    else
        print_status "ERROR" "System check failed"
        return 1
    fi
}

# Function to generate summary report
generate_summary() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))
    
    echo ""
    echo "========================================"
    print_status "INFO" "TEST EXECUTION SUMMARY"
    echo "========================================"
    echo "Total Test Configurations: $TOTAL_TESTS"
    echo "Passed: $PASSED_TESTS"
    echo "Failed: $FAILED_TESTS"
    echo "Duration: ${minutes}m ${seconds}s"
    echo "========================================"
    
    if [ $FAILED_TESTS -eq 0 ]; then
        print_status "SUCCESS" "All test configurations passed!"
        return 0
    else
        print_status "ERROR" "$FAILED_TESTS test configuration(s) failed"
        return 1
    fi
}

# Main execution starts here
print_status "INFO" "Starting comprehensive framework testing..."
echo "Test run started at: $(date)"
echo ""

# Run system check first (if enabled)
if [ "$RUN_SYSTEM_CHECK" = true ]; then
    if ! run_system_check; then
        print_status "ERROR" "System check failed. Aborting test execution."
        exit 1
    fi
else
    print_status "WARNING" "Skipping system check as requested"
fi

echo ""
print_status "INFO" "Starting browser test configurations..."
echo ""

# Test Chrome configurations
if [ "$RUN_CHROME" = true ]; then
    print_status "INFO" "=== CHROME BROWSER TESTS ==="
    run_tests "chrome" "" "" "Chrome - Normal mode"
    run_tests "chrome" "true" "" "Chrome - Headless mode"
    
    if [ "$QUICK_MODE" = false ]; then
        run_tests "chrome" "" "2" "Chrome - Parallel execution (2 workers)"
        run_tests "chrome" "true" "3" "Chrome - Headless + Parallel (3 workers)"
        run_tests "chrome" "" "" "Chrome - With Allure reporting" "--allure"
    fi
fi

# Test Firefox configurations
if [ "$RUN_FIREFOX" = true ]; then
    echo ""
    print_status "INFO" "=== FIREFOX BROWSER TESTS ==="
    run_tests "firefox" "" "" "Firefox - Normal mode"
    run_tests "firefox" "true" "" "Firefox - Headless mode"
    
    if [ "$QUICK_MODE" = false ]; then
        run_tests "firefox" "" "2" "Firefox - Parallel execution (2 workers)"
        run_tests "firefox" "true" "3" "Firefox - Headless + Parallel (3 workers)"
    fi
fi

# Test Edge configurations
if [ "$RUN_EDGE" = true ]; then
    echo ""
    print_status "INFO" "=== EDGE BROWSER TESTS ==="
    run_tests "edge" "" "" "Edge - Normal mode"
    run_tests "edge" "true" "" "Edge - Headless mode"
    
    if [ "$QUICK_MODE" = false ]; then
        run_tests "edge" "" "2" "Edge - Parallel execution (2 workers)"
        run_tests "edge" "true" "3" "Edge - Headless + Parallel (3 workers)"
    fi
fi

# Advanced test configurations (only in full mode)
if [ "$QUICK_MODE" = false ] && [ "$RUN_CHROME" = true ]; then
    echo ""
    print_status "INFO" "=== ADVANCED CONFIGURATIONS ==="
    run_tests "chrome" "" "4" "Chrome - High parallelism (4 workers)"
    run_tests "chrome" "true" "" "Chrome - Headless with cleanup" "--clean"
fi

# Generate final summary
generate_summary
exit_code=$?

print_status "INFO" "Test execution completed at: $(date)"
exit $exit_code