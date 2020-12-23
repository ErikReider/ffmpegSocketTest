#!/usr/bin/env bash
IFS=$'\n'
for monitor in `xrandr --listactivemonitors`; do if [[ "$monitor" == *"+*"* ]]; then break; fi; done

monParse=`echo $monitor | cut -f4 -d' '`
height=`echo $monParse | cut -f2 -d'/' | cut -f2 -d'x'`
width=`echo $monParse | cut -f1 -d'/'`
xOffset=`echo $monParse | cut -f2 -d'+'`
yOffset=`echo $monParse | cut -f3 -d'+'`

ffmpeg -f x11grab -s "$width"x"$height" -r 30 -i :0+"$xOffset","$yOffset" -threads 0 -f rawvideo -pix_fmt bgr24 -an -sn tcp://localhost:6969