import os
import re
import random
import subprocess

champions = ["#1 Ægon", "#2 Agent Venom", "#3 Ant Man", "#4 Beast", "#5 Black Panther (Civil War)", "#6 Black Widow", "#7 Blade", "#8 Captain America", "#9 Captain America (Infinity War)", "#10 Captain Marvel (Classic)", "#11 Carnage", "#12 Civil Warrior", "#13 Colossus", "#14 Corvus Glaive", "#15 Cyclops (Blue Team)", "#16 Daredevil (Classic)", "#17 Deadpool", "#18 Doctor Octopus", "#19 Doctor Strange", "#20 Dormammu", "#21 Drax", "#22 Falcon", "#23 Gamora", "#24 Ghost", "#25 Ghost Rider", "#26 Green Goblin", "#27 Groot", "#28 Guillotine", "#29 Gwenpool", "#30 Hawkeye", "#31 Heimdall", "#32 Hela", "#33 Howard The Duck", "#34 Hulk", "#35 Hulk (Ragnarok)", "#36 Hulkbuster", "#37 Iceman", "#38 Iron Fist", "#39 Iron Man (Infinity War)", "#40 Joe Fixit", "#41 Killmonger", "#42 Kingpin", "#43 Korg", "#44 Loki", "#45 Luke Cage", "#46 Magneto (Marvel Now!)", "#47 Masacre", "#48 M.O.D.O.K.", "#49 Morningstar", "#50 Nebula", "#51 Phoenix", "#52 Proxima Midnight", "#53 Punisher", "#54 Red Hulk", "#55 Red Skull", "#56 Rocket Raccoon", "#57 Rogue", "#58 Scarlet Witch", "#59 Spider-Gwen", "#60 Spider-Man (Classic)", "#61 Spider-Man (Stark Enhanced)", "#62 Star-Lord", "#63 Storm", "#64 Thor (Ragnarok)", "#65 Ultron", "#66 Venom", "#67 Venompool", "#68 Vision (Age of Ultron)", "#69 War Machine", "#70 Wasp", "#71 Winter Soldier", "#72 Wolverine", "#73 Wolverine (X-23)", "#74 Yellowjacket", "#75 Yondu", "#76 Angela", "#77 Captain Marvel", "#78 Cull Obsidian", "#79 Darkhawk", "#80 Ebony Maw", "#81 Gambit", "#82 Human Torch", "#83 Invisible Woman", "#84 Juggernaut", "#85 Magik", "#86 Mister Sinister", "#87 Mysterio", "#88 Namor", "#89 Nick Fury", "#90 Ronin", "#91 Sabretooth", "#92 Sentinel", "#93 She-Hulk", "#94 Spider-Man (Stealth Suit)", "#95 Taskmaster", "#96 The Hood", "#97 Thing", "#98 Thor", "#99 Thor (Jane Foster)", "#100 Vulture"]

def parse_champion_info(champion_string):
    match = re.match(r"#(\d+)\s+(.*)", champion_string)
    if match:
        number = match.group(1)
        name = match.group(2)
        return number, name
    return None, None

def get_champion_name(card_number):
    for champion in champions:
        number, name = parse_champion_info(champion)
        if number and int(number) == card_number:
            return name
    return None

def create_initial_unlocks_file():
    if not os.path.exists("unlocks.txt"):
        print("Creating initial unlocks.txt file...")
        with open("unlocks.txt", "w") as f:
            for i in range(1, 101):
                f.write(f"{i:03d} NO\n")
        print("unlocks.txt created with all cards locked.\n")

def read_current_unlocks():
    unlocks = {}
    try:
        with open("unlocks.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        card_num = parts[0]
                        status = parts[1].upper()
                        unlocks[card_num] = status
    except FileNotFoundError:
        pass
    return unlocks

def update_unlock_status(card_number_str, status="YES"):
    lines = []
    try:
        with open("unlocks.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        create_initial_unlocks_file()
        with open("unlocks.txt", "r") as f:
            lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith(card_number_str):
            lines[i] = f"{card_number_str} {status}\n"
            updated = True
            break

    with open("unlocks.txt", "w") as f:
        f.writelines(lines)

    return updated

def show_shield_splash():
    """S.H.I.E.L.D. splash screen"""
    print("\n" * 3)
    print("=" * 60)
    print("MARVEL CONTEST OF CHAMPIONS CARD COLLECTION")
    print("[CLASSIFIED - REDACTED BY S.H.I.E.L.D.]")
    print()
    print("⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣾⠿⠿⠿⠿⢷⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⡿⠀⠀⠀⢠⣬⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⣠⣾⠟⠉⠛⢿⣿⣿⣿⠃⠀⠀⠀⠈⢿⣿⣿⣿⡿⠛⠉⠻⣷⣄⠀⠀⠀")
    print("⠀⠀⣴⡿⠁⠀⠀⠀⠀⠈⠛⠏⠀⠀⠀⠀⠀⠈⠿⠛⠁⠀⠀⠀⠀⠀⠈⢿⣦⠀⠀")
    print("⠀⣼⡟⠻⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⢻⣧⠀")
    print("⢰⣿⠀⠀⢠⡟⠛⢶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡶⠛⠹⣆⠀⠀⣿⡆")
    print("⣾⡏⠀⢠⡟⠀⠀⢠⡟⠙⠷⣦⣀⠀⠀⠀⠀⣀⣤⠾⠛⢻⣆⠀⠀⠹⣆⠀⢸⣷")
    print("⣿⡇⢠⡟⠀⠀⢠⡟⠀⠀⠀⣸⠟⠳⣦⣴⠾⠛⣧⠀⠀⠀⢻⣆⠀⠀⠹⣆⢸⣿")
    print("⢿⣷⡟⠀⠀⢠⡿⠁⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⢻⣆⠀⠀⠹⣿⡿")
    print("⠸⣿⡀⠀⢀⡾⠁⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⢻⡆⠀⢀⣿⠇")
    print("⠀⢻⣷⣀⡞⠁⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⢻⣄⣾⡟⠀")
    print("⠀⠀⠻⣿⣅⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⣠⣿⠟⠀⠀")
    print("⠀⠀⠀⠙⢿⣷⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⣾⡿⠋⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠙⠻⣿⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⣾⠟⠋⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⣿⣷⣶⣶⣾⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀")
    print()
    print("=" * 60)
    print()

def show_shield_splash2():
    """S.H.I.E.L.D. splash screen"""
    print("\n" * 3)
    print("=" * 60)
    print("MARVEL CONTEST OF CHAMPIONS CARD COLLECTION")
    print("[TAHITI - It's a wonderful place!]")
    print()
    print("⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣾⠿⠿⠿⠿⢷⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⡿⠀⠀⠀⢠⣬⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⣠⣾⠟⠉⠛⢿⣿⣿⣿⠃⠀⠀⠀⠈⢿⣿⣿⣿⡿⠛⠉⠻⣷⣄⠀⠀⠀")
    print("⠀⠀⣴⡿⠁⠀⠀⠀⠀⠈⠛⠏⠀⠀⠀⠀⠀⠈⠿⠛⠁⠀⠀⠀⠀⠀⠈⢿⣦⠀⠀")
    print("⠀⣼⡟⠻⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⢻⣧⠀")
    print("⢰⣿⠀⠀⢠⡟⠛⢶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡶⠛⠹⣆⠀⠀⣿⡆")
    print("⣾⡏⠀⢠⡟⠀⠀⢠⡟⠙⠷⣦⣀⠀⠀⠀⠀⣀⣤⠾⠛⢻⣆⠀⠀⠹⣆⠀⢸⣷")
    print("⣿⡇⢠⡟⠀⠀⢠⡟⠀⠀⠀⣸⠟⠳⣦⣴⠾⠛⣧⠀⠀⠀⢻⣆⠀⠀⠹⣆⢸⣿")
    print("⢿⣷⡟⠀⠀⢠⡿⠁⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⢻⣆⠀⠀⠹⣿⡿")
    print("⠸⣿⡀⠀⢀⡾⠁⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⢻⡆⠀⢀⣿⠇")
    print("⠀⢻⣷⣀⡞⠁⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⢻⣄⣾⡟⠀")
    print("⠀⠀⠻⣿⣅⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⣠⣿⠟⠀⠀")
    print("⠀⠀⠀⠙⢿⣷⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⣾⡿⠋⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠙⠻⣿⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⣾⠟⠋⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⣿⣷⣶⣶⣾⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀")
    print()
    print("=" * 60)
    print()

def show_avengers_splash():
    """New Avengers-themed splash screen"""
    print("\n" * 3)
    print("=" * 60)
    print("MARVEL CONTEST OF CHAMPIONS CARD COLLECTION")
    print("[HAVE YOU EVER TRIED SHWARMA?]")
    print()
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣾⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⣠⣴⣿⡿⠟⠛⠋⣽⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀")
    print("⠀⠀⢀⣾⣿⠟⠁⠀⠀⠀⣼⣿⣿⠏⢸⣿⣿⡏⠻⣿⣷⡀⠀⠀")
    print("⠀⢠⣿⡟⠁⠀⠀⠀⠀⣼⣿⣿⡟⠀⢸⣿⣿⡇⠀⠈⢻⣿⡄⠀")
    print("⢠⣿⡟⠀⠀⠀⠀⠀⣼⣿⣿⡿⠀⠀⢸⣿⣿⡇⠀⠀⠀⢻⣿⡄")
    print("⣸⣿⠇⠀⠀⠀⠀⣼⣿⣿⣿⠁⠀⠀⠘⢿⣿⡇⠀⠀⠀⠘⣿⣇")
    print("⢿⣿⠀⠀⠀⠀⣰⣿⣿⣿⣇⣀⣀⣀⣼⣦⡙⠇⠀⠀⠀⠀⣿⡿")
    print("⢸⣿⡇⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡦⠀⠀⠀⢸⣿⡇")
    print("⠀⢿⣿⡀⣸⣿⣿⣿⠟⠉⠉⠉⠉⠉⣿⠟⣡⡆⠀⠀⢀⣿⡿⠀")
    print("⠀⠈⠛⣰⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠠⠾⠿⠇⠀⣠⣿⡿⠁⠀")
    print("⠀⠀⣰⣿⣿⣿⡟⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⡿⠋⠀⠀⠀")
    print("⠀⣰⣿⣿⣿⡿⠰⠿⣿⣶⣶⣶⣶⣶⣶⣿⠿⠟⠉⠀⠀⠀⠀⠀")
    print("⠀⠉⠉⠉⠉⠁⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print()
    print("=" * 60)
    print()

def show_random_splash_screen():
    """Randomly select and display one of the available splash screens"""
    splash_screens = [
        show_shield_splash,
        show_shield_splash2,
        show_avengers_splash
    ]
    
    # Randomly select one of the splash screen functions
    selected_splash = random.choice(splash_screens)
    selected_splash()

def get_unlock_count():
    unlocks = read_current_unlocks()
    count = sum(1 for status in unlocks.values() if status == "YES")
    return count

def main():
    create_initial_unlocks_file()

    while True:
        show_random_splash_screen()
        unlock_count = get_unlock_count()
        print(f"Current Collection: {unlock_count}/100 cards unlocked")
        print()

        user_input = input("Which card have you unlocked (enter the 3 digit value, or 'quit' to exit): ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n🎴 Thanks for using the S.H.I.E.L.D. Card Unlock System! 🎴")
            break

        if not user_input.isdigit() or len(user_input) != 3:
            print("\n❌ ERROR: Please enter exactly 3 digits (e.g., '001', not '1')")
            input("\nPress Enter to continue...")
            continue

        card_number = int(user_input)
        if card_number < 1 or card_number > 100:
            print(f"\n❌ ERROR: Card number must be between 001 and 100")
            input("\nPress Enter to continue...")
            continue

        current_unlocks = read_current_unlocks()
        if current_unlocks.get(user_input, "NO") == "YES":
            champion_name = get_champion_name(card_number)
            print(f"\n⚠️  Card {user_input}/100 {champion_name} is already in your collection!")
            input("\nPress Enter to continue...")
            continue

        champion_name = get_champion_name(card_number)
        if not champion_name:
            print(f"\n❌ ERROR: Could not find champion for card {user_input}")
            input("\nPress Enter to continue...")
            continue

        success = update_unlock_status(user_input, "YES")

        if success:
            print(f"\n🎉 CONGRATULATIONS! 🎉")
            print(f"Card {user_input}/100 {champion_name} has been added to your collection!")

            try:
                #print("\nLaunching Marvel Champions Trading Card Generator...")
                subprocess.run(["python", "subp.py"], check=True)
            except Exception as e:
                print(f"\n❌ ERROR: Could not run subp.py automatically: {e}")
        else:
            print(f"\n❌ ERROR: Could not unlock card {user_input}")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🎴 S.H.I.E.L.D. Card System terminated. Stay vigilant, Agent! 🎴")
    except Exception as e:
        print(f"\n❌ SYSTEM ERROR: {e}")
        print("Please contact S.H.I.E.L.D. Technical Support.")
        input("\nPress Enter to exit...")
