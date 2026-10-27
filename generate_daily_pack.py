
from datetime import datetime, timezone
from pathlib import Path

facts = [
    {
        "topic": "Octopus ke teen dil",
        "script": "Kya aap jaante hain ki octopus ke teen dil hote hain? Do dil khoon ko gills tak bhejte hain aur teesra sharir ke baaki hisson tak. Nature sach mein kamaal hai!"
    },
    {
        "topic": "Shukra grah ka din",
        "script": "Kya aap jaante hain? Shukra grah apni dhuri par ek chakkar lagane mein lagbhag 243 Earth days leta hai. Iska saal lagbhag 225 Earth days ka hota hai!"
    },
    {
        "topic": "Samundar ke chamakte jeev",
        "script": "Samundar mein kuch jeev apni roshni khud paida kar sakte hain. Is process ko bioluminescence kehte hain. Nature ke aise facts hairan kar dete hain!"
    },
    {
        "topic": "Kele ka science",
        "script": "Botany yani paudhon ki science mein kele ko berry maana jata hai. Science ki definitions kabhi-kabhi hamari aam soch se alag hoti hain!"
    },
    {
        "topic": "Space mein awaaz",
        "script": "Khule vacuum space mein awaaz aam tareeke se travel nahi kar sakti, kyunki sound ko travel karne ke liye kisi medium ki zaroorat hoti hai!"
    },
    {
        "topic": "Shahad ka raaz",
        "script": "Shahad mein paani kam aur acidity hoti hai, isliye kai microbes ke liye badhna mushkil hota hai. Lekin storage aur quality phir bhi matter karte hain!"
    },
    {
        "topic": "Samundar ki duniya",
        "script": "Samundar ke kuch jeev roshni ka istemal shikar ko attract karne ya dushman se bachne ke liye karte hain. Is duniya mein abhi bahut kuch seekhna baaki hai!"
    }
]

today = datetime.now(timezone.utc).date()
fact = facts[today.timetuple().tm_yday % len(facts)]

output = Path("output")
output.mkdir(exist_ok=True)

content = f"""# FactSpark Hindi
Date: {today}

## Video topic
{fact['topic']}

## Hindi Shorts script
{fact['script']}

## Title
{fact['topic']} 😲 | Amazing Facts #Shorts

## Hashtags
#HindiFacts #AmazingFacts #Shorts

## Before publishing
- Verify facts using reliable sources.
- Add original visuals and narration.
- Use only visuals and music you have permission to use.
- Watch the complete video before uploading.

Note: This is a content draft, not a finished video.
"""

file = output / f"{today}-facts.md"
file.write_text(content, encoding="utf-8")

print(f"Content pack created: {file}")
