from random import randint
import sys
from fillpdf import fillpdfs
import requests
"""
Project: Modron - A Multi-Purpose Tool for Dungeons and Dragons 5th Edition
Name: Hunter Martin
From: Crystal River, Florida, United States
# Recorded October 2nd, 2024
Github: https://github.com/tacogosa
"""



class Dice:
    def __init__(self):
        self._roll = 0

    def rollStats(self):
        results = []
        for _ in range(6):
            result = 0
            dice01 = randint(1, 6)
            dice02 = randint(1, 6)
            dice03 = randint(1, 6)
            dice04 = randint(1, 6)
            diceCount = [dice01, dice02, dice03, dice04]
            diceCount.remove(min(diceCount))
            result = sum(diceCount)
            results.append(result)
        return results


    def rollScores(self):
        # Set default scores to 0 so the attributes can be applied later
        abScores = {
            "Strength": 0,
            "Dexterity": 0,
            "Constitution": 0,
            "Intelligence": 0,
            "Wisdom": 0,
            "Charisma": 0,
        }
        results = self.rollStats()
        print(results)
        continueSheet = input("Continue with these stats? Y/N ").lower().strip()
        if continueSheet == "y":
            for item in abScores:
                while True:
                    try:
                        print(results)
                        value = int(input(f"Please enter a value for {item} \n"))
                        abScores[item] = value
                        results.remove(value)
                        break
                    except ValueError:
                        print("Invalid score")

            # --- Calculate proficiency bonus ---
            # For every 2 points above or below 10 in an attribute, the bonus gains +/- 1.
            # Strength
            strBonus = abScores['Strength']
            strBonus = self.calculateBonus(strBonus)
            # Dexterity
            dexBonus = abScores['Dexterity']
            dexBonus = self.calculateBonus(dexBonus)
            # Constitution
            conBonus = abScores['Constitution']
            conBonus = self.calculateBonus(conBonus)
            # Intelligence
            intBonus = abScores['Intelligence']
            intBonus = self.calculateBonus(intBonus)
            # Wisdom
            wisBonus = abScores['Wisdom']
            wisBonus = self.calculateBonus(wisBonus)
            # Charisma
            chaBonus = abScores['Charisma']
            chaBonus = self.calculateBonus(chaBonus)
            # --- end of prof bonus ---

            print("Your ability scores are...")
            print(f"Str: {abScores['Strength']}({strBonus}), Dex: {abScores['Dexterity']}({dexBonus}), Con: {abScores['Constitution']}({conBonus}), Int: {abScores['Intelligence']}({intBonus}), Wis: {abScores['Wisdom']}({wisBonus}), Cha: {abScores['Charisma']}({chaBonus})")
            
            # CONTINUE
            while True:
                continueToPdf = input("Continue with character creation? \n Y) Yes \n N) Return to options ").lower().strip()
                if continueSheet in ("y", "n"):
                    break
                else:
                    print("Invalid input")
            if continueToPdf == "y":
                abilityScores = {
                    "Strength": abScores['Strength'],
                    "Dexterity": abScores['Dexterity'],
                    "Constitution": abScores['Constitution'],
                    "Intelligence": abScores['Intelligence'],
                    "Wisdom": abScores['Wisdom'],
                    "Charisma": abScores['Charisma'],
                }
                abilityScores = {key: str(value) for key, value in abScores.items()}
                for key, value in abilityScores.items():
                    abilityScores[key] = value.replace("{", "").replace("}", "")
                abilityBonus = {
                    "strBonus": strBonus,
                    "dexBonus": dexBonus,
                    "conBonus": conBonus,
                    "intBonus": intBonus,
                    "wisBonus": wisBonus,
                    "chaBonus": chaBonus,
                }
                abilityScores, abilityBonus = self.createCharacter(abilityScores, abilityBonus)
        else:
            print("Returning to main menu")
            return

    def calculateBonus(self, score):
        profDict = {
            1: '-5',
            2: '-4',
            3: '-4',
            4: '-3',
            5: '-3',
            6: '-2',
            7: '-2',
            8: '-1',
            9: '-1',
            10: '0',
            11: '0',
            12: '+1',
            13: '+1',
            14: '+2',
            15: '+2',
            16: '+3',
            17: '+3',
            18: '+4',
            19: '+4',
            20: '+5',
        }
        if score in profDict:
            return profDict[score]


    def createCharacter(self, abilityScores, abilityBonus):
        formFields = list(fillpdfs.get_form_fields("DnD_5E_CharacterSheet_FormFillable.pdf").keys())
        playerName = input("Player Name: ")
        characterName = input("Character Name: ")
        characterClass = input("Please enter your class(es) and levels: ")
        characterBG = input("Background: ")
        race = input("Race: ")
        alignment = input("Alignment: ")
        armorClass = input("AC: ")
        hpMax = input("Max HP: ")

        dataDict = {
            formFields[0]: characterClass,
            formFields[1]: characterBG,
            formFields[2]: playerName,
            formFields[3]: characterName,
            formFields[4]: race,
            formFields[5]: alignment,
            # Skip 6, 7
            formFields[8]: abilityScores['Strength'],
            formFields[9]: +2,
            formFields[10]: armorClass,
            formFields[12]: "30ft",
            # Skip 13
            formFields[14]: abilityBonus['strBonus'],
            formFields[15]: hpMax,
            formFields[16]: abilityBonus['strBonus'],
            formFields[17]: abilityScores['Dexterity'],
            # Skip 18, 19
            formFields[20]: abilityBonus['dexBonus'],
            # Skip 21, 22
            formFields[23]: abilityScores['Constitution'],
            # Skip 24, 27
            formFields[28]: abilityBonus['conBonus'],
            # Skip 29, 33
            # Saving Throws
            formFields[34]: abilityScores['Intelligence'],
            formFields[35]: abilityBonus['dexBonus'],
            formFields[36]: abilityBonus['conBonus'],
            formFields[37]: abilityBonus['intBonus'],
            formFields[38]: abilityBonus['wisBonus'],
            formFields[39]: abilityBonus['chaBonus'],
            formFields[40]: abilityBonus['dexBonus'],
            formFields[41]: abilityBonus['wisBonus'],
            formFields[42]: abilityBonus['strBonus'],
            formFields[43]: abilityBonus['chaBonus'],
            formFields[44]: abilityBonus['intBonus'],
            formFields[45]: abilityBonus['wisBonus'],
            formFields[46]: abilityBonus['chaBonus'],
            #skip 47 through 55
            formFields[56]: abilityBonus['intBonus'],
            # skip 57, 59
            formFields[60]: abilityBonus['intBonus'],
            formFields[61]: abilityScores['Wisdom'],
            # skip 62, 63
            formFields[64]: abilityBonus['intBonus'],
            # skip 65
            formFields[66]: abilityBonus['wisBonus'],
            formFields[67]: abilityBonus['wisBonus'],
            formFields[68]: abilityScores['Charisma'],
            formFields[69]: abilityBonus['intBonus'],
            formFields[70]: abilityBonus['chaBonus'],
            formFields[71]: abilityBonus['wisBonus'],
            formFields[72]: abilityBonus['intBonus'],
            formFields[73]: abilityBonus['dexBonus'],
            # skip 74, 91
            formFields[92]: abilityBonus['chaBonus'],
            formFields[93]: abilityBonus['dexBonus'],
            formFields[94]: abilityBonus['chaBonus'],
            formFields[95]: abilityBonus['wisBonus'],
        }
        print("Finished filling sheet, exporting PDF...")
        print("Note: Bonuses from Race, Class, Subclass will not be added automatically.")
        fillpdfs.write_fillable_pdf("DnD_5E_CharacterSheet_FormFillable.pdf", f"{characterName}.pdf", dataDict)
        return abilityScores, abilityBonus



dice = Dice()

def main():
    intro()
    functions = {
        "a": dice.rollScores,
        "b": spellSearch,
        "c": diceRoller,
        "d": sys.exit,
    }
    while True:
        choice = input("Please select a function\nA) Character Builder\nB) Spellbook\nC) Dice\nD) Exit ").lower().strip()
        if choice in functions:
            functions[choice]()
        else:
            print("Invalid choice")

def spellSearch():
        userInput = input("Enter spell name: ").lower().strip()
        userInput = userInput.replace(" ", "-")
        url = f"https://www.dnd5eapi.co/api/spells/{userInput}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            name = data.get("name")
            range = data.get("range")
            level = data.get("level")
            school = data.get("school", {}).get("name", "Unknown")
            classes = ", ".join([cls['name'] for cls in data.get("classes", [])])
            description = "\n".join(data.get("desc", []))
            components = ", ".join(data.get("components", []))
            material = data.get("material", "None")

            print(f"Name: {name} \nLevel: {level} {school}\nRange: {range}\nDescription: {description}\nComponents: {components}\nMaterials: {material}\nClasses: {classes}")
        else:
            print("Spell not found")

def diceRoller():
    functions = {
        "a": d4,
        "b": d6,
        "c": d8,
        "d": d10,
        "e": d12,
        "f": d20,
        "g": returnToMenu,
    }
    while True:
        print("Please choose a type of dice")
        choice = input("A) D4\nB) D6\nC) D8\nD) D10\nE) D12\nF) D20\nG) Exit ").lower().strip()
        if choice == "g":
            break
        elif choice in functions:
            try:
                amount = int(input("How many? "))
                for _ in range(amount):
                    result = functions[choice]()
                    print(f"Result: {result}")
            except ValueError:
                print("Invalid amount entered.")
        else:
            print("Invalid choice. Try again.")
# Dice functions
def d4():
    result = randint(1, 4)
    return result
def d6():
    result = randint(1, 6)
    return result
def d8():
    result = randint(1, 8)
    return result
def d10():
    result = randint(1, 10)
    return result
def d12():
    result = randint(1, 12)
    return result
def d20():
    result = randint(1, 20)
    return result
def returnToMenu():
    print("Returning to main menu")
    return

def intro():
    print("""            ,:::,
       ,,,:;  :  ;:,,, 
   ,,,:       :       :,,, 
,,;...........:...........;,,
; ;          ;';          ; ;
;  ;        ;   ;        ;  ;
;   ;      ;     ;      ;   ;
;    ;    ;       ;    ;    ;
;     Welcome to Modron     ;
;      ;:...........:;      ;
;     , ;           ; ,     ;
;   ,'   ;         ;   ',   ;
'';'      ;       ;      ';''
   ''';    ;     ;    ;'''         
       ''':;;   ;;:'''
            ':::' """)

if __name__ == "__main__":
    main()

