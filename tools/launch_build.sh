#!/bin/bash
# Launch video v3: hyped VO + background music (ducked) over portrait Trailer 2 footage.
set -e
S=$(dirname "$0"); R=/home/user/gta6channel
T=$S/dl/trailer.mp4; VO=$S/vo2/launch_b.mp3; MU=$S/vo2/music_a.mp3
OUT=$R/media/edits/2026-11-18_launch_out_now_v3.mp4
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
PINK=0xFF2BD6; CYAN=0x22E6FF; D=11.0
BG="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=-0.12:saturation=1.15,setsar=1"
H(){ echo "drawtext=fontfile=$F:text='$1':fontsize=$2:fontcolor=white:borderw=7:bordercolor=$PINK:x=(w-tw)/2:y=$3"; }
B(){ echo "drawtext=fontfile=$F:text='$1':fontsize=$2:fontcolor=$3:x=(w-tw)/2:y=$4:box=1:boxcolor=black@0.75:boxborderw=16:enable='between(t,$5,$6)'"; }
ffmpeg -v error -y -ss 75 -t $D -i $T -i $R/brand/profile_picture.png -i $VO -stream_loop -1 -i $MU -filter_complex "
[0:v]$BG,trim=0:$D,setpts=PTS-STARTPTS[bg];
[1:v]scale=360:360:flags=lanczos,format=rgba,colorchannelmixer=aa=0.92[logo];
[bg][logo]overlay=(W-w)/2:H-620[v1];
[v1]drawbox=x=0:y=0:w=iw:h=580:color=0x0A0014@1:t=fill,
$(H 'GTA 6' 150 190),$(H 'IS OUT NOW' 120 370),
$(B 'New Zealand got it FIRST' 56 white 1060 3.5 7.9),
$(B 'Midnight local time everywhere' 52 $CYAN 1160 4.8 7.9),
$(B 'WELCOME TO LEONIDA' 72 white 1100 7.9 $D),
drawtext=fontfile=$F:text='Footage\: Rockstar Games (Trailer 2)':fontsize=20:fontcolor=white@0.6:x=24:y=h-44,
null[v];
[2:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur=$D,asplit[vo1][vo2];
[3:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.09,afade=t=out:st=$(echo "$D-0.8"|bc):d=0.8[mu];
[mu][vo1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=300[duck];
[vo2][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]" \
 -map "[v]" -map "[a]" -t $D -c:v libx264 -preset slow -crf 16 -profile:v high -maxrate 16M -bufsize 32M -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -movflags +faststart $OUT
echo ok $OUT
