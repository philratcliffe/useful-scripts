#!/bin/bash

# File to store tmux session information
TMUX_SAVE_FILE="$HOME/.tmux-session-backup.txt"

function save_tmux_sessions() {
    echo "Saving tmux sessions to $TMUX_SAVE_FILE..."
    
    # Check if tmux is running
    if ! tmux list-sessions &>/dev/null; then
        echo "No tmux sessions found running."
        return 1
    fi

    # Create the save file and clear it
    > "$TMUX_SAVE_FILE"
    
    # Add a comment header to the file
    echo "#!/bin/bash" >> "$TMUX_SAVE_FILE"
    echo "# Tmux session restore file - generated $(date)" >> "$TMUX_SAVE_FILE"
    echo "# This file contains tmux commands without the 'tmux' prefix" >> "$TMUX_SAVE_FILE"
    echo "" >> "$TMUX_SAVE_FILE"
    
    # Get all sessions
    local sessions=$(tmux list-sessions -F "#{session_name}")
    
    # For each session, save its windows and panes
    for session in $sessions; do
        # Record session creation
        echo "new-session -d -s \"$session\"" >> "$TMUX_SAVE_FILE"
        
        # Get windows for this session
        local windows=$(tmux list-windows -t "$session" -F "#{window_index}")
        
        for window in $windows; do
            # Get window name and properly escape quotes
            local window_name=$(tmux display-message -p -t "$session:$window" '#{window_name}' | sed 's/"/\\"/g')
            
            # Get panes for this window
            local panes=$(tmux list-panes -t "$session:$window" -F "#{pane_index}")
            
            # First pane in a window uses new-window, others use split-window
            local first_pane=true
            
            for pane in $panes; do
                # Get pane working directory
                local pane_path=$(tmux display-message -p -t "$session:$window.$pane" '#{pane_current_path}')
                
                # Get pane running command (if available)
                local pane_command=""
                if tmux display-message -p -t "$session:$window.$pane" '#{pane_current_command}' &>/dev/null; then
                    pane_command=$(tmux display-message -p -t "$session:$window.$pane" '#{pane_current_command}')
                    # Skip if it's just a shell
                    if [[ "$pane_command" == "bash" || "$pane_command" == "zsh" || "$pane_command" == "sh" || "$pane_command" == "fish" ]]; then
                        pane_command=""
                    fi
                fi
                
                # For first pane in window, use new-window
                if $first_pane; then
                    if [ $window -eq 0 ]; then
                        # For the first window (0), just rename it
                        echo "rename-window -t $session:0 \"$window_name\"" >> "$TMUX_SAVE_FILE"
                        echo "send-keys -t $session:$window \"cd '$pane_path'\" C-m" >> "$TMUX_SAVE_FILE"
                    else
                        # For other windows, create a new window
                        echo "new-window -t $session:$window -n \"$window_name\" -c \"$pane_path\"" >> "$TMUX_SAVE_FILE"
                    fi
                    first_pane=false
                else
                    # For other panes, use split-window
                    
                    # Get pane layout info to determine if split is vertical or horizontal
                    local pane_info=$(tmux display-message -p -t "$session:$window.$pane" '#{pane_at_left} #{pane_at_right} #{pane_at_top} #{pane_at_bottom}')
                    
                    # Determine split direction based on position (very simplified)
                    # This is a heuristic and might not be 100% accurate for complex layouts
                    local split_option="-h" # default to horizontal split
                    if [[ $(tmux display-message -p -t "$session:$window.$pane" '#{pane_width}') -gt $(tmux display-message -p -t "$session:$window.$pane" '#{pane_height}') ]]; then
                        split_option="-v" # vertical split if pane is wider than tall
                    fi
                    
                    echo "split-window $split_option -t $session:$window -c \"$pane_path\"" >> "$TMUX_SAVE_FILE"
                fi
                
                # Add command to run in pane if it exists
                if [ -n "$pane_command" ] && [ "$pane_command" != "tmux" ]; then
                    echo "send-keys -t $session:$window.$pane \"$pane_command\" C-m" >> "$TMUX_SAVE_FILE"
                fi
            done
            
            # Try to capture and restore the layout
            local layout=$(tmux display-message -p -t "$session:$window" '#{window_layout}')
            echo "select-layout -t $session:$window \"$layout\" || true" >> "$TMUX_SAVE_FILE"
        done
        
        # Select the active window in the session
        local active_window=$(tmux display-message -p -t "$session" '#{session_windows}')
        echo "select-window -t $session:0" >> "$TMUX_SAVE_FILE"
    done
    
    # Select the previously active session
    local active_session=$(tmux display-message -p '#{client_session}')
    echo "select-session -t $active_session" >> "$TMUX_SAVE_FILE"
    
    echo "Tmux sessions saved successfully!"
}

function kill_tmux_sessions() {
    echo "Killing all tmux sessions..."
    tmux kill-server
    echo "All tmux sessions terminated."
}

function restore_tmux_sessions() {
    echo "Restoring tmux sessions from $TMUX_SAVE_FILE..."
    
    if [ ! -f "$TMUX_SAVE_FILE" ]; then
        echo "No saved sessions found. ($TMUX_SAVE_FILE doesn't exist)"
        return 1
    fi
    
    # Create a temporary script with corrected commands
    TEMP_SCRIPT=$(mktemp)
    
    # Process the save file and prefix all tmux commands with "tmux "
    while IFS= read -r line; do
        # Skip empty lines and comments
        if [[ -z "$line" || "$line" == \#* ]]; then
            echo "$line" >> "$TEMP_SCRIPT"
            continue
        fi
        
        # Add tmux prefix to commands
        echo "tmux $line" >> "$TEMP_SCRIPT"
    done < "$TMUX_SAVE_FILE"
    
    # Make the temporary script executable
    chmod +x "$TEMP_SCRIPT"
    
    # Execute the fixed script
    bash "$TEMP_SCRIPT"
    
    # Clean up
    rm "$TEMP_SCRIPT"
    
    echo "Tmux sessions restored! Use 'tmux attach' to connect."
}

# Main script execution
case "$1" in
    save)
        save_tmux_sessions
        ;;
    kill)
        kill_tmux_sessions
        ;;
    restore)
        restore_tmux_sessions
        ;;
    save-and-kill)
        save_tmux_sessions && kill_tmux_sessions
        ;;
    *)
        echo "Usage: $0 {save|kill|restore|save-and-kill}"
        echo "  save          - Save all tmux sessions"
        echo "  kill          - Kill all tmux sessions"
        echo "  restore       - Restore saved tmux sessions"
        echo "  save-and-kill - Save and then kill all tmux sessions"
        exit 1
        ;;
esac

exit 0
