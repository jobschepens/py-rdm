#!/bin/bash
# Script: load-env.sh
# Purpose: Load environment variables from .env file into current shell session
# Usage: source ./load-env.sh

# Define the .env file path (optional parameter, defaults to .env)
EnvFile="${1:-.env}"

# Check if the .env file exists
if [ -f "$EnvFile" ]; then
    # set -a: automatically export all variables defined below
    set -a
    
    # Source (execute) the .env file
    # This reads each line and treats KEY=VALUE as variable assignment
    source "$EnvFile"
    
    # set +a: turn off automatic export
    set +a
    
    # Print success message to confirm variables were loaded
    echo "✓ Environment variables loaded from $EnvFile"
else
    # If .env doesn't exist, print error message
    echo "✗ $EnvFile file not found"
    exit 1
fi