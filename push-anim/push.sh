#!/bin/bash

# Path to the compiled animation binary
ANIM_BIN="/home/karthik/Documents/Projects/hobbie project/a/push-anim/target/release/push-anim"

# Start the animation in the background
"$ANIM_BIN" &
ANIM_PID=$!

# Temporary file for git output
PUSH_LOG=$(mktemp)

# Run git push with all arguments, capturing all output (including progress)
git push --progress "$@" > "$PUSH_LOG" 2>&1
PUSH_EXIT_CODE=$?

# Kill the animation
kill $ANIM_PID 2>/dev/null
wait $ANIM_PID 2>/dev/null

# Clean up terminal state
tput cnorm
clear

# Display the captured git output
cat "$PUSH_LOG"
rm "$PUSH_LOG"

exit $PUSH_EXIT_CODE
