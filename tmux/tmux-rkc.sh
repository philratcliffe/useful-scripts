#!/bin/bash

# use the -d switch so we don't attach yet
tmux new -d -s rkc
tmux split-pane -h
tmux split-pane -v  
tmux select-pane -t 0
tmux send-keys "workon redkestrel" C-m
tmux select-pane -t 1
tmux send-keys "workon redkestrel" C-m
tmux attach-session
