#!/bin/bash
set -e

# Configuration for retries
MAX_RETRIES=100
DELAY=60

# Get the directory of the script
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# Log file setup
LOG_FILE="$SCRIPT_DIR/run.log"
echo "Logging to: $LOG_FILE"

# Start logging
exec > >(tee -a "$LOG_FILE") 2>&1

# Log the script directory
echo "Script directory: $SCRIPT_DIR"

# Change to the script's directory
cd "$SCRIPT_DIR" || { echo "Error: Could not change to script directory"; exit 1; }

# Retry logic
for ((i=1; i<=MAX_RETRIES; i++)); do
    echo "Attempt $i of $MAX_RETRIES: Running Python script at $(date)..."

    # Check for the virtual environment and activate it
    if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source "$SCRIPT_DIR/.venv/bin/activate"
    else
        echo "Error: Virtual environment not found at $SCRIPT_DIR/.venv/bin/activate"
        exit 1
    fi

    # Run the Python script
    if "$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/src/main.py"; then
        echo "Success! Python script completed at $(date)."
        exit 0  # Exit successfully
    else
        echo "Python script failed at $(date). Retrying in $DELAY seconds..."
        sleep $DELAY
    fi
done

echo "Max retries reached at $(date). Script failed to complete."
exit 1
