import json, subprocess, sys
P='/tmp/claude-0/-home-user-gta6channel/1751b18b-43f4-5e5f-aba6-7cc270fec014/scratchpad/own2/seg'
src='media/raw/clips/own_fake_robbery_src.mp4'
S=json.loads(sys.argv[1]); PUNCH_IDX=int(sys.argv[2])
lst=open(f'{P}/list.txt','w')
for i,(a,b,sp,*ex) in enumerate(S):
    vf=(f"setpts=PTS/{sp},fps=30" if sp!=1 else "fps=30")+(","+ex[0] if ex else "")
    af=(f"atempo={sp}," if sp!=1 else "")+"aresample=48000"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(round(b-a,3)),"-i",src,"-vf",vf,"-af",af,"-ac","2",
      "-c:v","libx264","-crf","17","-preset","fast","-threads","2","-c:a","aac","-b:a","192k",f"{P}/s{i}.mp4"],check=True)
    lst.write(f"file '{P}/s{i}.mp4'\n")
lst.close()
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{P}/list.txt","-c","copy",f"{P}/cat.mp4"],check=True)
t=sum((b-a)/sp for a,b,sp,*_ in S[:PUNCH_IDX])
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{P}/cat.mp4","-i","media/music/sting_whoosh_boom.wav","-filter_complex",
 f"[1:a]aresample=48000,adelay={int(t*1000)}|{int(t*1000)},volume=0.8[st];[0:a][st]amix=inputs=2:duration=first:normalize=0[a]",
 "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","media/raw/clips/own_fake_robbery_cut.mp4"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","media/raw/clips/own_fake_robbery_cut.mp4","-vn","-c:a","libmp3lame","-b:a","192k","media/raw/clips/own_fake_robbery_audio.mp3"],check=True)
w=json.load(open('/tmp/claude-0/-home-user-gta6channel/1751b18b-43f4-5e5f-aba6-7cc270fec014/scratchpad/own2/words.json'))
out=[];off=0
for a,b,sp,*_ in S:
    for t_,x,y in w:
        if t_.startswith('['): continue
        if x>=a-0.02 and y<=b+0.05: out.append([t_,round(off+max(0,x-a)/sp,2),round(off+(min(y,b)-a)/sp,2)])
    off+=(b-a)/sp
print('dur',round(off,2),'punch',round(t,2)); print(' '.join(x[0] for x in out))
p='media/configs/2026-11-24_own_fake_robbery.json'; C=json.load(open(p))
C['words']=out; C['end_text']=["WOULD YOU HIT HIM?",round(off-5.0,2)]
json.dump(C,open(p,'w'),ensure_ascii=False)
