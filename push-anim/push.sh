#!/bin/bash

# Path to the compiled animation binary
ANIM_BIN="/home/karthik/Documents/Projects/hobbie project/a/push-anim/target/release/push-anim"

# Start the animation in the background
"$ANIM_BIN" &
ANIM_PID=$!

# Run git push with all arguments passed to this script
git push "$@"
PUSH_EXIT_CODE=$?

# Kill the animation
kill $ANIM_PID 2>/dev/null
# Wait a tiny bit for the animation to clean up/stop
wait $ANIM_PID 2>/dev/null

# Show the cursor again and reset terminal just in case
tput cnorm
reset

exit $PUSH_EXIT_CODE
