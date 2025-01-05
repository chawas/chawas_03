#!/bin/bash
set -e

# Configuration for retries
MAX_RETRIES=100
DELAY=60

# Set the base directory (the location of this script)
BASE_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
echo $BASE_DIR

# Define the virtual environment path
VENV_PATH="$BASE_DIR/.venv/bin/activate"

# Python script to execute
PYTHON_SCRIPT="$BASE_DIR/src/main.py"

# Check if the virtual environment exists
if [ ! -f "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Change to the base directory
cd "$BASE_DIR" || exit

# Retry logic
for ((i=1; i<=MAX_RETRIES; i++)); do
    echo "Attempt $i of $MAX_RETRIES: Running Python script..."

    # Activate the virtual environment
    source "$VENV_PATH"

    # Run the Python script
    if python "$PYTHON_SCRIPT"; then
        echo "Success! Python script completed."
        exit 0  # Exit successfully
    else
        echo "Python script failed. Retrying in $DELAY seconds..."
        sleep $DELAY
    fi
done

echo "Max retries reached. Script failed to complete."
exit 1
