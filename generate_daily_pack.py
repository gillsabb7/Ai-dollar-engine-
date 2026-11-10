#!/usr/bin/env python3
from datetime import date
from pathlib import Path

SETS = [
[
("Octopus ke teen dil hote hain", "Do dil khoon ko gills tak bhejte hain jahan oxygen milti hai. Teesra dil oxygen wala khoon baaki body tak pahunchata hai. Swimming ke waqt teesre dil ki dhadkan dheemi ho sakti hai."),
("Octopus ka khoon neela hota hai", "Iske khoon mein hemocyanin naam ka copper-based protein hota hai. Yeh oxygen transport karta hai aur oxygen milne par neela rang dikhata hai."),
("Venus par ek din uske saal se lamba hai", "Venus ko apni dhuri par ek rotation poora karne mein lagbhag 243 Earth days lagte hain. Suraj ka ek chakkar lagane mein lagbhag 225 Earth days lagte hain."),
("Sharks bahut pracheen hain", "Sharks ke purvajon ke fossils lagbhag 400 million saal purane milte hain. Isliye sharks ka evolutionary group pedon se bhi purana hai."),
("Space ke vacuum mein awaaz travel nahi karti", "Awaaz ko hawa, paani ya kisi solid jaise medium ki zaroorat hoti hai. Space ka vacuum aam sound waves ko travel karne ke liye medium nahi deta.")
],
[
("Honey bahut lambe samay tak tik sakta hai", "Sahi tarah sealed aur dry rakha honey bahut lambe samay tak kharab hone se bach sakta hai. Iski kam moisture aur acidity kai microbes ki growth ko rokne mein madad karti hai."),
("Butterflies pairon se taste karti hain", "Butterflies ke pairon par taste-sensing receptors hote hain. Inse woh patton aur plants ko pehchanne mein madad leti hain."),
("Banana botanical berry hai", "Botany ki definition ke mutabik banana berry hai, kyunki yeh flower ke ovary se develop hone wala fleshy fruit hai. Strawberry is definition mein true berry nahi hai."),
("Kuch jellyfish roshni bana sakti hain", "Kuch species bioluminescence dikhati hain. Unke body ke chemicals reaction karke light banate hain, jo defence ya communication mein kaam aa sakti hai."),
("Skin human body ka sabse bada organ hai", "Skin body ko cover karke germs, chot aur paani ke loss se bachati hai. Yeh temperature control aur touch sensation mein bhi madad karti hai.")
],
[
("Sunlight ko Earth tak aane mein 8 minute lagte hain", "Sunlight ko Earth tak pahunchne mein average lagbhag 8 minute 20 seconds lagte hain. Isliye hum Sun ko kuch minute purana dekhte hain."),
("Plants photosynthesis se food banate hain", "Plants sunlight ki energy se carbon dioxide aur water ka use karke sugars banate hain. Is process mein oxygen bhi release hoti hai."),
("Saturn ki average density paani se kam hai", "Saturn ki average density water se kam hai, lekin iska matlab yeh nahi ki use kisi real ocean mein tairaya ja sakta hai. Aisa ocean maujood nahi."),
("Koala fingerprints insaan jaise lag sakte hain", "Koala ke fingerprints ka pattern human fingerprints jaisa ho sakta hai. Close examination se dono ko alag pehchana ja sakta hai."),
("Bees flowers se nectar collect karti hain", "Worker honeybees flowers se nectar leti hain. Hive mein nectar process hota hai aur paani kam hone par honey ke roop mein store kiya jata hai.")
]
]

def main():
    today = date.today()
    facts = SETS[today.toordinal() % len(SETS)]
    out = Path("output")
    out.mkdir(exist_ok=True)
    lines = [
        "# FactSpark Hindi — Daily 5 Facts Pack",
        f"**Date:** {today.isoformat()}",
        "**Format:** 5 facts with explanations | Suggested duration: 45–60 seconds",
        "",
        "## Opening hook",
        "Aaj ke 5 amazing facts aapko hairaan kar denge — aakhir tak zaroor dekho!",
        "",
        "## Five detailed facts",
        ""
    ]
    for i, (title, detail) in enumerate(facts, 1):
        lines += [f"### Fact {i}: {title}", detail, ""]
    narration = "Namaste dosto! Aaj ke paanch amazing facts suno. " + " ".join(
        f"Fact number {i}: {title}. {detail}" for i, (title, detail) in enumerate(facts, 1)
    ) + " Aapko kaunsa fact sabse interesting laga? Comment karo aur FactSpark Hindi ko follow karo!"
    lines += [
        "## Hindi voice-over script (Roman Hindi)",
        narration, "",
        "## Suggested title",
        "5 Amazing Facts Jo Aapko Hairaan Kar Denge! | FactSpark Hindi", "",
        "## Hashtags",
        "#AmazingFacts #HindiFacts #FactSparkHindi #Shorts #DidYouKnow", "",
        "## Publishing checklist",
        "- [ ] Har fact ko reliable source se verify kiya.",
        "- [ ] Voice-over aur captions check kiye.",
        "- [ ] Visuals original ya properly licensed hain.",
        "- [ ] Final video manually review ki.",
        "",
        "> Yeh draft hai. Publish karne se pehle facts reliable sources se verify karein."
    ]
    path = out / f"{today.isoformat()}-facts.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created {path}")

if __name__ == "__main__":
    main()
