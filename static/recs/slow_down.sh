#!/bin/bash
source=`ls ~/ZF_recordings/recs/`
slow='_slow.wav'
for entry in $source
do
	sox $entry $(echo "$entry" | cut -f -1 -d '.')$slow speed 0.25
done
