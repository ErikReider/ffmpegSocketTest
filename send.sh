#!/usr/bin/env bash
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0+1920,0 -threads 0 -f rawvideo -pix_fmt bgr24 -an -sn tcp://localhost:6969