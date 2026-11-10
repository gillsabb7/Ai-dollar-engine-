#!/usr/bin/env python3
"""Create a 5-fact vertical MP4 with Hindi TTS and animated visual cards."""
import asyncio, os, subprocess
from datetime import date
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT=Path(__file__).resolve().parent
OUT,WORK=ROOT/"video_output",ROOT/".video_work"
W,H,FPS=720,1280,24
VOICE="hi-IN-SwaraNeural"
FACTS=[
("OCTOPUS KE TEEN DIL","Do dil gills tak khoon bhejte hain. Teesra dil baaki body tak oxygen wala khoon pahunchata hai."),
("OCTOPUS KA KHOON NEELA","Iske khoon mein hemocyanin naam ka copper-based protein oxygen transport karta hai."),
("VENUS KA DIN LAMBA","Venus ko ek rotation mein lagbhag 243 Earth days lagte hain. Uska saal lagbhag 225 Earth days ka hota hai."),
("SHARKS BAHUT PURANE HAIN","Sharks ke purvajon ke fossils lagbhag 400 million saal purane milte hain."),
("SPACE MEIN AAWAAZ NAHI","Awaaz ko medium chahiye. Space ke vacuum mein aam sound waves travel nahi kar sakti.")
]
NARRATION=("Namaste dosto! Aaj ke paanch amazing facts suno. "
"Fact number one: Octopus ke teen dil hote hain. Do dil gills tak khoon bhejte hain. Teesra dil baaki body tak oxygen wala khoon pahunchata hai. "
"Fact number two: Octopus ka khoon neela hota hai. Ismein hemocyanin naam ka copper-based protein oxygen transport karta hai. "
"Fact number three: Venus ko ek rotation mein lagbhag 243 Earth days lagte hain, jabki uska saal lagbhag 225 din ka hota hai. "
"Fact number four: Sharks ke purvaj lagbhag 400 million saal pehle maujood the. "
"Fact number five: Space ke vacuum mein aam awaaz travel nahi kar sakti, kyunki sound ko medium chahiye. "
"Aapko kaunsa fact sabse interesting laga? Comment karo aur FactSpark Hindi ko follow karo!")

def run(cmd):
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size) if os.path.exists(p) else ImageFont.load_default()
def wrap(draw,text,f,maxw):
    lines=[]; cur=""
    for word in text.split():
        test=(cur+" "+word).strip()
        if draw.textbbox((0,0),test,font=f)[2]<=maxw: cur=test
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines
def card(idx,title,detail,path):
    im=Image.new("RGB",(W,H),(4,22,49)); d=ImageDraw.Draw(im,"RGBA")
    for n in range(24):
        x=(n*97+idx*43)%W; y=(n*151+50)%600; r=5+n%5*3
        d.ellipse((x-r,y-r,x+r,y+r),outline=(90,220,245,120),width=2)
    d.rounded_rectangle((32,42,W-32,120),radius=24,fill=(7,75,112,230),outline=(80,225,245,220),width=2)
    d.text((W//2,81),f"FACTSPARK HINDI • FACT {idx}",font=font(24,True),fill="white",anchor="mm")
    cx,cy=W//2,390
    if idx in (1,2):
        d.ellipse((cx-110,cy-110,cx+110,cy+110),fill=(240,117,102),outline=(255,210,170),width=5)
        d.ellipse((cx-45,cy-15,cx-15,cy+20),fill="white"); d.ellipse((cx+15,cy-15,cx+45,cy+20),fill="white")
    elif idx==3:
        d.ellipse((cx-120,cy-120,cx+120,cy+120),fill=(224,151,82),outline=(255,220,150),width=5)
        for yy in [-50,0,50]: d.arc((cx-100,cy+yy-20,cx+100,cy+yy+20),10,170,fill=(150,75,45),width=12)
    elif idx==4:
        d.ellipse((cx-115,cy-115,cx+115,cy+115),fill=(94,110,220),outline=(175,195,255),width=5)
        d.arc((cx-165,cy-65,cx+165,cy+65),180,360,fill=(250,190,90),width=12)
    else:
        d.polygon([(cx-165,cy),(cx-70,cy-55),(cx+80,cy-45),(cx+160,cy),(cx+75,cy+60),(cx-70,cy+50)],fill=(100,170,195))
        d.polygon([(cx-20,cy-40),(cx+20,cy-120),(cx+55,cy-38)],fill=(100,170,195))
    d.rounded_rectangle((30,690,W-30,1090),radius=30,fill=(0,8,25,235),outline=(70,215,240,220),width=3)
    tf,bf=font(34,True),font(26); y=770
    for line in wrap(d,title,tf,W-100)[:3]:
        d.text((W//2,y),line,font=tf,fill=(255,225,100),anchor="mm"); y+=48
    y+=12
    for line in wrap(d,detail,bf,W-100)[:5]:
        d.text((W//2,y),line,font=bf,fill=(245,250,255),anchor="mm"); y+=42
    d.text((W//2,1170),"5 FACTS • FOLLOW FOR MORE",font=font(22,True),fill=(145,235,255),anchor="mm")
    im.save(path)

async def main():
    OUT.mkdir(exist_ok=True); WORK.mkdir(exist_ok=True)
    audio=WORK/"voice.mp3"
    await edge_tts.Communicate(NARRATION,VOICE,rate="+2%").save(str(audio))
    cards=[("5 AMAZING FACTS!","Aakhir tak dekho — paanch interesting facts!",0)]+[(a,b,i) for i,(a,b) in enumerate(FACTS,1)]
    clips=[]
    for i,(title,detail,num) in enumerate(cards):
        img=WORK/f"card_{i:02d}.png"; clip=WORK/f"clip_{i:02d}.mp4"
        card(num,title,detail,img); dur=4 if i==0 else 7
        run(["ffmpeg","-y","-loop","1","-i",str(img),"-t",str(dur),"-vf",
             f"scale=800:1422,zoompan=z='min(zoom+0.0007,1.06)':d={dur*FPS}:s=720x1280:fps={FPS},format=yuv420p",
             "-r",str(FPS),"-an","-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p",str(clip)])
        clips.append(clip)
    concat=WORK/"concat.txt"; concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips))
    silent=WORK/"silent.mp4"
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(silent)])
    final=OUT/f"factspark-5-facts-{date.today().isoformat()}.mp4"
    run(["ffmpeg","-y","-i",str(silent),"-i",str(audio),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",str(final)])
    (OUT/"publishing-details.txt").write_text("Title: 5 Amazing Facts Jo Aapko Hairaan Kar Denge! | FactSpark Hindi\nHashtags: #AmazingFacts #HindiFacts #FactSparkHindi #Shorts #DidYouKnow\nVerify facts before publishing.\n",encoding="utf-8")
    print(f"Created {final}")
if __name__=="__main__": asyncio.run(main())
