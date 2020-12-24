#!/bin/sh

if [[ "$(pmset -g | grep ' sleep')" == *"coreaudiod"* ]]; then 
    echo playing; 
else 
    echo not_playing; 
fi