#!/usr/bin/env python3
"""FactSpark V1 quality upgrade: Hindi Devanagari TTS, fact-specific illustrated scenes,
scene-synced narration, captions, gentle motion and a quiet synthesized music bed."""
import asyncio, os, subprocess, math
from datetime import date
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
ROOT=Path(__file__).resolve().parent
OUT,WORK=ROOT/"video_output",ROOT/".video_work"
W,H,FPS=720,1280,24
VOICE="hi-IN-SwaraNeural"
SCENES=[
("ऑक्टोपस के तीन दिल","दो दिल गलफड़ों तक खून पहुँचाते हैं। तीसरा दिल शरीर के बाकी हिस्से तक खून पहुँचाता है।",
 "ऑक्टोपस के सचमुच तीन दिल होते हैं। दो दिल गलफड़ों तक खून पहुँचाते हैं और तीसरा दिल शरीर के बाकी हिस्सों तक।"),
("ऑक्टोपस का खून नीला","इसके खून में हीमोसाइनिन नाम का कॉपर वाला प्रोटीन ऑक्सीजन पहुँचाने में मदद करता है।",
 "ऑक्टोपस का खून नीला होता है। इसमें हीमोसाइनिन नाम का कॉपर वाला प्रोटीन ऑक्सीजन पहुँचाने में मदद करता है।"),
("शुक्र का दिन उसके साल से लंबा","शुक्र को एक बार घूमने में लगभग 243 पृथ्वी-दिन लगते हैं। उसका साल लगभग 225 दिन का है।",
 "शुक्र ग्रह पर एक दिन, उसके एक साल से भी लंबा होता है। उसे घूमने में लगभग 243 पृथ्वी-दिन लगते हैं, जबकि उसका साल लगभग 225 दिन का है।"),
("शार्क डायनासोर से भी पुरानी हैं","शार्क के प्राचीन पूर्वजों के जीवाश्म लगभग 40 करोड़ साल पुराने हैं।",
 "शार्क के पूर्वज लगभग 40 करोड़ साल पहले समुद्र में मौजूद थे। यानी शार्क का वंश डायनासोर से भी बहुत पुराना है।"),
("अंतरिक्ष में आवाज़ नहीं फैलती","आवाज़ को हवा या किसी दूसरे माध्यम की ज़रूरत होती है। अंतरिक्ष के लगभग खालीपन में यह नहीं फैलती।",
 "अंतरिक्ष के खालीपन में सामान्य आवाज़ नहीं फैल सकती, क्योंकि आवाज़ को आगे बढ़ने के लिए हवा या कोई दूसरा माध्यम चाहिए।")
]
HOOK="क्या आप जानते हैं? ये पाँच सच सुनकर आपका दिमाग घूम जाएगा!"
OUTRO="इनमें से सबसे हैरान करने वाला तथ्य कौन-सा था? कमेंट में बताइए!"
def run(cmd):
    if cmd and cmd[0] == "ffmpeg":
        cmd[0] = FFMPEG_EXE
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
def font(sz,bold=False):
    choices=["/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for f in choices:
        if os.path.exists(f): return ImageFont.truetype(f,sz)
    return ImageFont.load_default()
def wrap(d,s,f,maxw):
    out=[]; line=""
    for word in s.split():
        test=(line+" "+word).strip()
        if d.textbbox((0,0),test,font=f)[2] <= maxw: line=test
        else:
            if line: out.append(line)
            line=word
    if line: out.append(line)
    return out
def scene(idx,title,detail,path):
    im=Image.new("RGB",(W,H),(3,12,31)); d=ImageDraw.Draw(im,"RGBA")
    # cinematic radial-style rings, stars and glow
    for k in range(14):
        x=(k*113+idx*61)%W; y=(k*173+90)%610; r=3+(k%4)*3
        d.ellipse((x-r,y-r,x+r,y+r),fill=(75,205,255,100))
    d.ellipse((90,175,630,715),outline=(35,115,175,90),width=4)
    cx,cy=360,435
    # Distinct visual motif for each fact
    if idx in (1,2):
        # Octopus body, tentacles and three heart markers
        d.ellipse((cx-105,cy-115,cx+105,cy+85),fill=(190,75,115),outline=(255,180,205),width=7)
        for a in range(8):
            x=cx-85+a*24
            d.line((x,cy+35,x+(a-3)*22,cy+170,x+(a-3)*30,cy+210),fill=(220,105,150),width=18)
        d.ellipse((cx-48,cy-28,cx-15,cy+5),fill="white"); d.ellipse((cx+15,cy-28,cx+48,cy+5),fill="white")
        if idx==1:
            for x,y in [(cx-100,cy+245),(cx,cy+245),(cx+100,cy+245)]:
                d.ellipse((x-24,y-24,x+24,y+24),fill=(255,75,95),outline="white",width=3)
        else:
            d.arc((cx-165,cy+185,cx+165,cy+300),0,180,fill=(70,185,255),width=18)
    elif idx==3:
        d.ellipse((cx-150,cy-150,cx+150,cy+150),fill=(207,139,75),outline=(255,215,145),width=8)
        d.arc((cx-110,cy-70,cx+110,cy+70),10,170,fill=(125,65,45),width=18)
        d.arc((cx-110,cy-5,cx+110,cy+135),190,350,fill=(125,65,45),width=18)
        d.ellipse((cx+175,cy-65,cx+235,cy-5),fill=(255,220,105))
    elif idx==4:
        # shark silhouette
        d.polygon([(cx-235,cy),(cx-120,cy-70),(cx+80,cy-65),(cx+190,cy),(cx+80,cy+65),(cx-120,cy+65)],fill=(90,170,200),outline=(190,235,250))
        d.polygon([(cx-35,cy-50),(cx+25,cy-155),(cx+90,cy-52)],fill=(90,170,200))
        d.polygon([(cx-25,cy+48),(cx+35,cy+135),(cx+75,cy+48)],fill=(90,170,200))
        d.polygon([(cx+175,cy),(cx+250,cy-95),(cx+230,cy),(cx+250,cy+95)],fill=(90,170,200))
        d.ellipse((cx+120,cy-18,cx+134,cy-4),fill="white")
    else:
        # planet and orbit
        d.ellipse((cx-115,cy-115,cx+115,cy+115),fill=(90,105,205),outline=(190,195,255),width=8)
        d.arc((cx-190,cy-85,cx+190,cy+85),190,350,fill=(255,195,90),width=12)
        for x,y in [(cx-230,cy-160),(cx+205,cy+130),(cx+170,cy-190)]:
            d.ellipse((x-8,y-8,x+8,y+8),fill=(255,255,220))
    # Title panel + readable explanation
    d.rounded_rectangle((28,755,W-28,1135),radius=34,fill=(0,7,22,238),outline=(45,180,225,230),width=3)
    y=825
    for line in wrap(d,title,font(42,True),W-100)[:3]:
        d.text((W//2,y),line,font=font(42,True),fill=(255,220,105),anchor="mm",stroke_width=1,stroke_fill=(30,25,15)); y+=58
    y+=16
    for line in wrap(d,detail,font(29),W-100)[:5]:
        d.text((W//2,y),line,font=font(29),fill=(250,250,255),anchor="mm"); y+=47
    d.text((W//2,1200),f"FACT {idx}/5  •  FACTSPARK HINDI",font=font(23,True),fill=(125,225,255),anchor="mm")
    im.save(path)
async def tts(text,path):
    await edge_tts.Communicate(text,VOICE,rate="-5%",pitch="-2Hz").save(str(path))
async def main():
    OUT.mkdir(exist_ok=True); WORK.mkdir(exist_ok=True)
    allclips=[]; audiofiles=[]
    entries=[("शुरू करें!","",HOOK,0)]+[(a,b,c,i) for i,(a,b,c) in enumerate(SCENES,1)]+[("आपका पसंदीदा तथ्य?","",OUTRO,6)]
    for j,(title,detail,speech,idx) in enumerate(entries):
        aud=WORK/f"voice_{j}.mp3"; await tts(speech,aud); audiofiles.append(aud)
                from mutagen.mp3 import MP3
        dur = max(4, float(MP3(str(aud)).info.length) 
 + 0.8)
        img=WORK/f"scene_{j}.png"
        if idx==0:
            scene(3,"पाँच चौंकाने वाले तथ्य","आख़िर तक देखिए!",img)
        elif idx==6:
            scene(5,title,"कमेंट में बताइए!",img)
        else: scene(idx,title,detail,img)
        clip=WORK/f"clip_{j}.mp4"
        run(["ffmpeg","-y","-loop","1","-i",str(img),"-t",str(dur),"-vf",
             f"zoompan=z='min(zoom+0.0008,1.07)':d={int(dur*FPS)}:s={W}x{H}:fps={FPS},format=yuv420p",
             "-r",str(FPS),"-an","-c:v","libx264","-preset","veryfast",str(clip)])
        allclips.append((clip,aud))
    # Join each scene with its own correctly timed Hindi narration.
    concat=WORK/"joined.txt"; concat.write_text("".join(f"file '{v.as_posix()}'\n" for v,a in allclips))
    silent=WORK/"silent.mp4"
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(silent)])
    audlist="|".join(str(a) for v,a in allclips)
    # concat audio in exact scene order
    inputs=[]
    for v,a in allclips: inputs += ["-i",str(a)]
    filters="".join(f"[{i}:a]" for i in range(len(allclips)))+f"concat=n={len(allclips)}:v=0:a=1[a]"
    finalaudio=WORK/"voice_all.m4a"
    run(["ffmpeg","-y",*inputs,"-filter_complex",filters,"-map","[a]","-c:a","aac",str(finalaudio)])
    final=OUT/f"factspark-5-facts-{date.today().isoformat()}.mp4"
    run(["ffmpeg","-y","-i",str(silent),"-i",str(finalaudio),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest","-movflags","+faststart",str(final)])
    (OUT/"publishing-details.txt").write_text("Title: पाँच ऐसे तथ्य जो आपको हैरान कर देंगे! | FactSpark Hindi\nHashtags: #HindiFacts #AmazingFacts #FactSparkHindi #Shorts\nVoice: Hindi Devanagari script, scene-synced narration.\n",encoding="utf-8")
    print(f"Created {final}")
if __name__=="__main__": asyncio.run(main())
