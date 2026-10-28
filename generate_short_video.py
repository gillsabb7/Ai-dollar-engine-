#!/usr/bin/env python3
"""FactSpark Hindi: build a 5-fact vertical Short with Hindi TTS and animated scenes."""
import asyncio, os, subprocess, math
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "video_output"
WORK = ROOT / ".video_work"
W, H, FPS = 720, 1280, 24
VOICE = "hi-IN-SwaraNeural"

# Five short, broadly established facts. Verify sources before publishing.
FACTS = [
    ("OCTOPUS", "Octopus ke teen dil hote hain.", "Do dil gills tak khoon bhejte hain, teesra body tak."),
    ("VENUS", "Venus par ek din, uske ek saal se lamba hota hai.", "Venus apni dhuri par bahut dheere ghoomta hai."),
    ("SHARK", "Sharks, pedon se bhi purane hain.", "Sharks ke purvaj lagbhag 400 million saal pehle maujood the."),
    ("SPACE", "Space mein awaaz aam taur par travel nahi karti.", "Awaaz ko travel karne ke liye medium chahiye, jaise hawa."),
    ("OCTOPUS", "Octopus ka khoon neela hota hai.", "Uske khoon mein oxygen le jaane ke liye copper wala hemocyanin hota hai."),
]
NARRATION = (
    "Namaste dosto! Aaj ke paanch amazing facts aapko hairaan kar denge. "
    "Fact number one: Octopus ke teen dil hote hain. Do dil gills tak khoon bhejte hain, aur teesra body tak. "
    "Fact number two: Venus par ek din, uske ek saal se lamba hota hai. Venus bahut dheere ghoomta hai. "
    "Fact number three: Sharks ke purvaj pedon se bhi pehle maujood the, lagbhag chaar sau million saal pehle. "
    "Fact number four: Space mein awaaz aam taur par travel nahi karti, kyunki awaaz ko hawa jaise medium ki zaroorat hoti hai. "
    "Fact number five: Octopus ka khoon neela hota hai, kyunki usmein hemocyanin hota hai. "
    "Aapko kaunsa fact sabse interesting laga? Comment karein aur FactSpark Hindi ko follow karein!"
)

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textbbox((0,0), test, font=f)[2] <= maxw:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def draw_scene(path, idx, tag, title, detail):
    im = Image.new("RGB", (W,H), (4,18,39))
    pix = im.load()
    for y in range(H):
        t=y/H
        col=(int(3+8*t), int(20+28*t), int(44+55*t))
        for x in range(W): pix[x,y]=col
    d=ImageDraw.Draw(im, "RGBA")
    # glowing rings and bubbles for depth
    for j in range(15):
        x=(j*83+idx*57)%W; y=(j*149+100)%H; r=8+(j%4)*6
        d.ellipse((x-r,y-r,x+r,y+r), outline=(77,207,244,90), width=2)
    d.rounded_rectangle((32,42,W-32,118), radius=26, fill=(7,75,111,230), outline=(87,226,246,230), width=2)
    d.text((W//2,80), "FACTSPARK HINDI  •  FACT "+str(idx+1), font=font(25,True), fill=(235,251,255), anchor="mm")
    # distinctive graphic per fact
    cx, cy = W//2, 390
    if idx in (0,4):  # octopus
        col=(247,111,107)
        for dx,dy in [(-125,80),(-80,145),(-25,165),(35,165),(90,140),(135,80)]:
            d.line((cx,cy+50,cx+dx,cy+dy), fill=col, width=25)
            d.ellipse((cx+dx-12,cy+dy-12,cx+dx+12,cy+dy+12), fill=(255,184,151))
        d.ellipse((cx-100,cy-95,cx+100,cy+105), fill=col)
        d.ellipse((cx-47,cy-15,cx-15,cy+25), fill="white"); d.ellipse((cx+15,cy-15,cx+47,cy+25), fill="white")
        d.ellipse((cx-35,cy-5,cx-20,cy+15), fill=(3,18,40)); d.ellipse((cx+27,cy-5,cx+42,cy+15), fill=(3,18,40))
        if idx==4:
            d.rounded_rectangle((cx-74,cy+115,cx+74,cy+166),radius=20,fill=(30,117,220,220))
            d.text((cx,cy+141),"BLUE BLOOD",font=font(18,True),fill="white",anchor="mm")
    elif idx==1: # Venus planet
        d.ellipse((cx-125,cy-125,cx+125,cy+125), fill=(235,153,78), outline=(255,213,147), width=5)
        for yy in [-65,-15,42,78]:
            d.arc((cx-112,cy+yy-25,cx+112,cy+yy+25), 10, 170, fill=(167,86,57), width=13)
        d.arc((cx-170,cy-160,cx+170,cy+160), 30, 320, fill=(255,219,123), width=4)
    elif idx==2: # shark
        pts=[(cx-160,cy),(cx-60,cy-50),(cx+30,cy-55),(cx+125,cy-12),(cx+175,cy-42),(cx+165,cy+20),(cx+80,cy+55),(cx-65,cy+48)]
        d.polygon(pts,fill=(113,170,196),outline=(208,239,247))
        d.polygon([(cx-25,cy-45),(cx+15,cy-115),(cx+52,cy-45)],fill=(113,170,196))
        d.ellipse((cx+112,cy-12,cx+126,cy+2),fill=(4,20,40))
        d.polygon([(cx-55,cy+35),(cx-5,cy+105),(cx+25,cy+42)],fill=(113,170,196))
    elif idx==3: # space planet + stars
        d.ellipse((cx-105,cy-105,cx+105,cy+105),fill=(104,111,219),outline=(172,193,255),width=5)
        d.arc((cx-160,cy-60,cx+160,cy+70),190,350,fill=(247,190,89),width=13)
        for x,y in [(cx-180,cy-120),(cx+165,cy-95),(cx+180,cy+105),(cx-160,cy+135)]:
            d.line((x-10,y,x+10,y),fill=(255,245,183),width=3); d.line((x,y-10,x,y+10),fill=(255,245,183),width=3)
    # readable Roman Hindi captions avoids missing Devanagari glyphs on some runners
    d.rounded_rectangle((30,680,W-30,1070),radius=30,fill=(0,7,23,232),outline=(65,211,239,220),width=3)
    titlef=font(36,True); detailf=font(27)
    lines=wrap(d,title,titlef,W-100)
    y=760
    for line in lines[:3]:
        d.text((W//2,y),line,font=titlef,fill=(255,224,90),anchor="mm")
        y+=48
    y+=12
    for line in wrap(d,detail,detailf,W-100)[:4]:
        d.text((W//2,y),line,font=detailf,fill=(243,250,255),anchor="mm")
        y+=42
    d.text((W//2,1160),"5 FACTS • SHORT & SIMPLE",font=font(22,True),fill=(135,229,255),anchor="mm")
    im.save(path)

async def main():
    OUT.mkdir(exist_ok=True); WORK.mkdir(exist_ok=True)
    date=datetime.now().strftime("%Y-%m-%d")
    audio=WORK/"voice.mp3"
    await edge_tts.Communicate(NARRATION,VOICE,rate="+4%").save(str(audio))
    clips=[]
    # 4-second hook + 5 fact cards + short end card
    cards=[("5 Amazing Facts!", "Aakhir tak dekho — fact number 5 sabse alag hai.", 0, "HOOK")]
    for i,(tag,title,detail) in enumerate(FACTS):
        cards.append((title,detail,i,tag))
    cards.append(("Aapka favourite fact kaunsa tha?", "Comment karein aur FactSpark Hindi ko follow karein.", 3, "FOLLOW"))
    durations=[3]+[5]*5+[4]
    for i,(title,detail,sceneidx,tag) in enumerate(cards):
        img=WORK/f"scene_{i:02d}.png"
        draw_scene(img, min(sceneidx,4), tag, title, detail)
        clip=WORK/f"clip_{i:02d}.mp4"
        dur=durations[i]
        # Subtle motion zoom so cards aren't completely static
        vf=f"scale=800:1422,zoompan=z='min(zoom+0.0008,1.08)':d={dur*FPS}:s=720x1280:fps={FPS},format=yuv420p"
        run(["ffmpeg","-y","-loop","1","-i",str(img),"-t",str(dur),"-vf",vf,"-r",str(FPS),"-an","-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p",str(clip)])
        clips.append(clip)
    concat=WORK/"concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips),encoding="utf-8")
    silent=WORK/"silent.mp4"
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(silent)])
    final=OUT/f"factspark-5-facts-{date}.mp4"
    run(["ffmpeg","-y","-i",str(silent),"-i",str(audio),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",str(final)])
    (OUT/f"factspark-5-facts-{date}.txt").write_text(
        "TITLE: 5 Amazing Facts Jo Aapko Hairaan Kar Denge! | FactSpark Hindi\n"
        "HASHTAGS: #AmazingFacts #HindiFacts #FactSparkHindi #Shorts #DidYouKnow\n\n"
        "VOICEOVER:\n"+NARRATION+
        "\n\nNOTE: Captions use Roman Hindi to avoid missing Devanagari font glyphs. Verify all facts from reliable sources before publishing.\n",
        encoding="utf-8")
    print(f"Created: {final}")

if __name__=="__main__":
    asyncio.run(main())
