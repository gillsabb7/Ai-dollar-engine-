import asyncio, subprocess, os
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import edge_tts
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'video_output'; TMP=ROOT/'.video_work'
W,H=720,1280; FPS=24; VOICE='hi-IN-SwaraNeural'
NARRATION=('Namaste dosto! Aaj ka amazing fact hai. Octopus ke teen dil hote hain. Do dil khoon ko gills tak bhejte hain, aur teesra dil baaki body tak. Aise facts ke liye FactSpark Hindi ko follow karein!')
SCENES=[('Aaj ka amazing fact!','Kya aap jaante hain?',4),('Octopus ke teen dil!','Ji haan, ek nahi teen dil.',6),('Do dil gills tak khoon bhejte hain','Teesra dil baaki body tak.',7),('Samundar ka kamaal!','FactSpark Hindi ko follow karein.',7)]
def font(size,bold=False):
 p='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf' if bold else '/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'
 if not os.path.exists(p): p='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 return ImageFont.truetype(p,size) if os.path.exists(p) else ImageFont.load_default()
def scene(i,title,sub):
 im=Image.new('RGB',(W,H),(5,24,50)); d=ImageDraw.Draw(im,'RGBA')
 for j in range(30):
  x=(j*137+i*51)%W; y=(j*193+70)%H; r=5+j%5*3; d.ellipse((x-r,y-r,x+r,y+r),outline=(100,220,245,120),width=2)
 d.rounded_rectangle((35,45,W-35,125),radius=25,fill=(5,75,115,230),outline=(70,220,240,200),width=2)
 d.text((W//2,85),'FACTSPARK HINDI',font=font(30,True),fill='white',anchor='mm')
 # original drawn octopus illustration
 cx,cy=W//2,430; col=(245,105,100)
 paths=[[(cx-55,cy+45),(cx-130,cy+110),(cx-165,cy+70)],[(cx-25,cy+60),(cx-65,cy+145),(cx-105,cy+145)],[(cx+15,cy+60),(cx+20,cy+145),(cx+65,cy+150)],[(cx+55,cy+45),(cx+120,cy+110),(cx+165,cy+70)],[(cx-75,cy+10),(cx-145,cy+20),(cx-165,cy-10)],[(cx+75,cy+10),(cx+145,cy+20),(cx+165,cy-10)]]
 for pts in paths: d.line(pts,fill=col,width=27,joint='curve')
 d.ellipse((cx-100,cy-100,cx+100,cy+100),fill=col)
 for ex in (cx-35,cx+35): d.ellipse((ex-14,cy-12,ex+14,cy+24),fill='white'); d.ellipse((ex-5,cy-2,ex+5,cy+15),fill=(5,25,50))
 d.rounded_rectangle((30,700,W-30,1010),radius=28,fill=(0,8,24,225),outline=(70,220,240,220),width=3)
 d.text((W//2,775),title,font=font(39,True),fill=(255,224,90),anchor='mm',align='center')
 f=font(29); words=sub.split(); lines=[]; cur=''
 for word in words:
  test=(cur+' '+word).strip()
  if d.textbbox((0,0),test,font=f)[2] < W-80: cur=test
  else: lines.append(cur); cur=word
 if cur: lines.append(cur)
 y=865
 for line in lines[:3]: d.text((W//2,y),line,font=f,fill='white',anchor='mm'); y+=48
 d.text((W//2,1150),'Follow for more amazing facts',font=font(23,True),fill=(150,235,255),anchor='mm')
 p=TMP/f'scene{i}.png'; im.save(p); return p
async def main():
 OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True); audio=TMP/'voice.mp3'
 await edge_tts.Communicate(NARRATION,VOICE).save(str(audio))
 clips=[]
 for i,(title,sub,dur) in enumerate(SCENES):
  img=scene(i,title,sub); clip=TMP/f'clip{i}.mp4'
  subprocess.run(['ffmpeg','-y','-loop','1','-i',str(img),'-t',str(dur),'-r',str(FPS),'-vf','format=yuv420p','-an','-c:v','libx264','-preset','veryfast',str(clip)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); clips.append(clip)
 concat=TMP/'concat.txt'; concat.write_text(''.join(f"file '{p.as_posix()}'\n" for p in clips))
 silent=TMP/'silent.mp4'; subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(silent)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 date=datetime.now().strftime('%Y-%m-%d'); final=OUT/f'factspark-hindi-{date}.mp4'
 subprocess.run(['ffmpeg','-y','-i',str(silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-shortest','-movflags','+faststart',str(final)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 (OUT/f'factspark-hindi-{date}.txt').write_text('TOPIC: Octopus ke teen dil\n\nVOICEOVER:\n'+NARRATION+'\n\nTITLE: Aaj ka Amazing Fact 😲 | FactSpark Hindi\n\n#AmazingFacts #HindiFacts #FactSparkHindi #Shorts #DidYouKnow\n\nPlease verify facts and review the video before publishing.\n',encoding='utf-8')
 print(f'Created {final}')
if __name__=='__main__': asyncio.run(main())
