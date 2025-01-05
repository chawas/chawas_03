#!/bin/bash
set -e

# Configuration for retries
MAX_RETRIES=100
DELAY=60

# Define the path to the virtual environment
VENV_PATH="/home/wrf/deployed/chawas_03/.venv/bin/activate"

# Get the directory of the script
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# Change to the script's directory
cd "$SCRIPT_DIR" || exit
echo $SCRIPT_DIR
# Retry logic
for ((i=1; i<=MAX_RETRIES; i++)); do
    echo "Attempt $i of $MAX_RETRIES: Running Python script..."

    # Check if the virtual environment exists
    if [ ! -f "$VENV_PATH" ]; then
        echo "Error: Virtual environment not found at $VENV_PATH"
        exit 1
    fi

    # Activate the virtual environment
    source "$VENV_PATH"

    # Run the Python script
    if python /home/wrf/deployed/chawas_03/src/main.py; then
        echo "Success! Python script completed."
        exit 0  # Exit successfully
    else
        echo "Python script failed. Retrying in $DELAY seconds..."
        sleep $DELAY
    fi
done

echo "Max retries reached. Script failed to complete."
exit 1

