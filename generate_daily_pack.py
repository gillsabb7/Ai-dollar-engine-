from datetime import date
from pathlib import Path

# FactSpark Hindi: creates one text draft per day. Verify facts before publishing.
FACTS = [
    ("Octopus ke teen dil", "Octopus ke teen dil hote hain: do gills tak khoon bhejte hain aur teesra baaki body tak."),
    ("Chand ki roshni", "Chand apni roshni khud nahi banata; woh Suraj ki roshni reflect karta hai."),
    ("Space mein awaaz", "Space ke vacuum mein awaaz aam hawa ki tarah travel nahi karti, kyunki awaaz ko medium chahiye."),
    ("Banana aur berry", "Botany ki technical definition ke mutabik banana berry maana jata hai, jabki strawberry true berry nahi hai."),
    ("Shukra grah", "Shukra grah apni dhuri par bahut dheere ghoomta hai; uska ek rotation uske saal se bhi lamba hota hai."),
    ("Shahad", "Sahi tarah se seal kiya gaya shahad bahut lambe samay tak tik sakta hai."),
    ("Sharks", "Sharks machhliyon ka ek purana group hain aur unki kai alag-alag species hoti hain."),
]

def main():
    today = date.today()
    topic, fact = FACTS[today.timetuple().tm_yday % len(FACTS)]
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    script = f"Namaste dosto! Aaj ka amazing fact hai: {fact} Aise hi facts ke liye FactSpark Hindi ko subscribe karein!"
    content = f"""# FactSpark Hindi — Daily Facts Pack

Date: {today.isoformat()}

## Topic
{topic}

## Hindi voice-over script
{script}

## Suggested title
Aaj ka Amazing Fact 😲 | FactSpark Hindi

## Hashtags
#AmazingFacts #HindiFacts #FactSparkHindi #Shorts #DidYouKnow

## Publishing checklist
- [ ] Fact ko reliable source se verify kiya.
- [ ] Original ya properly licensed visuals/audio use kiye.
- [ ] Final video ko manually review kiya.

Note: Ye sirf text draft hai; ye video render ya YouTube par upload nahi karta.
"""
    output_file = output_dir / f"{today.isoformat()}-facts.md"
    output_file.write_text(content, encoding="utf-8")
    print(f"Success: created {output_file}")

if __name__ == "__main__":
    main()
