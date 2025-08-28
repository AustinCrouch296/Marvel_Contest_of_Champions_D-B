import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import re
from urllib.parse import quote, urljoin
import time
import json
import random

# Your champions list
champions = ["#1 Ægon", "#2 Agent Venom", "#3 Ant Man", "#4 Beast", "#5 Black Panther (Civil War)", "#6 Black Widow", "#7 Blade", "#8 Captain America", "#9 Captain America (Infinity War)", "#10 Captain Marvel (Classic)", "#11 Carnage", "#12 Civil Warrior", "#13 Colossus", "#14 Corvus Glaive", "#15 Cyclops (Blue Team)", "#16 Daredevil (Classic)", "#17 Deadpool", "#18 Doctor Octopus", "#19 Doctor Strange", "#20 Dormammu", "#21 Drax", "#22 Falcon", "#23 Gamora", "#24 Ghost", "#25 Ghost Rider", "#26 Green Goblin", "#27 Groot", "#28 Guillotine", "#29 Gwenpool", "#30 Hawkeye", "#31 Heimdall", "#32 Hela", "#33 Howard The Duck", "#34 Hulk", "#35 Hulk (Ragnarok)", "#36 Hulkbuster", "#37 Iceman", "#38 Iron Fist", "#39 Iron Man (Infinity War)", "#40 Joe Fixit", "#41 Killmonger", "#42 Kingpin", "#43 Korg", "#44 Loki", "#45 Luke Cage", "#46 Magneto (Marvel Now!)", "#47 Masacre", "#48 M.O.D.O.K.", "#49 Morningstar", "#50 Nebula", "#51 Phoenix", "#52 Proxima Midnight", "#53 Punisher", "#54 Red Hulk", "#55 Red Skull", "#56 Rocket Raccoon", "#57 Rogue", "#58 Scarlet Witch", "#59 Spider-Gwen", "#60 Spider-Man (Classic)", "#61 Spider-Man (Stark Enhanced)", "#62 Star-Lord", "#63 Storm", "#64 Thor (Ragnarok)", "#65 Ultron", "#66 Venom", "#67 Venompool", "#68 Vision (Age of Ultron)", "#69 War Machine", "#70 Wasp", "#71 Winter Soldier", "#72 Wolverine", "#73 Wolverine (X-23)", "#74 Yellowjacket", "#75 Yondu", "#76 Angela", "#77 Captain Marvel", "#78 Cull Obsidian", "#79 Darkhawk", "#80 Ebony Maw", "#81 Gambit", "#82 Human Torch", "#83 Invisible Woman", "#84 Juggernaut", "#85 Magik", "#86 Mister Sinister", "#87 Mysterio", "#88 Namor", "#89 Nick Fury", "#90 Ronin", "#91 Sabretooth", "#92 Sentinel", "#93 She-Hulk", "#94 Spider-Man (Stealth Suit)", "#95 Taskmaster", "#96 The Hood", "#97 Thing", "#98 Thor", "#99 Thor (Jane Foster)", "#100 Vulture"]

def create_directories():
    """Create necessary directories"""
    os.makedirs("cards", exist_ok=True)
    os.makedirs("images", exist_ok=True)
    os.makedirs("images_secret", exist_ok=True)  # New secret images folder
    os.makedirs("cards_secret", exist_ok=True)   # New secret cards folder

def check_existing_files(card_number, character_name):
    """Check if normal or secret cards already exist"""
    # Check for normal card
    normal_card_filename = f"cards/{card_number:03d}_{character_name.replace(' ', '_')}.png"
    normal_exists = os.path.exists(normal_card_filename)
    
    # Check for secret card
    secret_card_filename = f"cards_secret/{card_number:03d}_card_secret.png"
    secret_exists = os.path.exists(secret_card_filename)
    
    return normal_exists, secret_exists

def parse_champion_info(champion_string):
    """Parse champion string to extract number and name"""
    match = re.match(r"#(\d+)\s+(.*)", champion_string)
    if match:
        number = match.group(1)
        name = match.group(2)
        return number, name
    return None, None

def clean_name_for_search(name):
    """Clean character name for search - this function removes parentheses for search purposes"""
    # This function is used elsewhere for search queries, not for wiki URLs
    cleaned = re.sub(r'\([^)]*\)', '', name).strip()
    return cleaned

def get_random_user_agent():
    """Get a random user agent to avoid detection"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def search_unsplash_image(character_name):
    """Try to get images from Unsplash API (free tier)"""
    try:
        # Clean name for search
        clean_name = clean_name_for_search(character_name)
        search_query = f"{clean_name} marvel comic"
        
        # Unsplash API endpoint (requires free API key)
        # You can get one at https://unsplash.com/developers
        # For now, we'll skip this and use placeholder generation
        return None
    except:
        return None

def search_contest_wiki_image(character_name):
    """Try to find images from Marvel Contest of Champions wiki"""
    try:
        # Format character name for URL (replace spaces with underscores, handle special cases)
        url_name = format_name_for_wiki_url(character_name)
        
        # Construct the wiki page URL with the featured image
        wiki_url = f"https://marvel-contestofchampions.fandom.com/wiki/{url_name}?file={url_name.replace('_', '+')}+featured.png"
        
        headers = {'User-Agent': get_random_user_agent()}
        
        # Check if the page exists
        try:
            response = requests.head(wiki_url, headers=headers, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                #print(f"  YES - {wiki_url}")
                
                # Try to download the direct image URL
                # The actual image URL format is different from the page URL
                image_url = f"https://static.wikia.nocookie.net/marvel-contestofchampions/images/featured/{url_name.replace('_', '+')}+featured.png"
                
                # Try a few variations of the image URL
                possible_urls = [
                    f"https://static.wikia.nocookie.net/marvel-contestofchampions/images/featured/{url_name}+featured.png",
                    f"https://static.wikia.nocookie.net/marvel-contestofchampions/images/{url_name}_featured.png",
                    f"https://vignette.wikia.nocookie.net/marvel-contestofchampions/images/featured/{url_name}_featured.png"
                ]
                
                for img_url in possible_urls:
                    try:
                        img_response = requests.get(img_url, headers=headers, timeout=10)
                        if img_response.status_code == 200:
                            return save_image_from_response(img_response, character_name)
                    except:
                        continue
                
                # If direct image download fails, try to scrape the page for the actual image URL
                return scrape_wiki_page_for_image(wiki_url, character_name)
                
            else:
                #print(f"  NO - {wiki_url}")
                return None
                
        except requests.exceptions.RequestException:
            #print(f"  NO - {wiki_url}")
            return None
            
    except Exception as e:
        #print(f"  Error checking wiki for {character_name}: {e}")
        return None

def format_name_for_wiki_url(name):
    """Format character name for wiki URL"""
    # Handle special character name mappings for the wiki FIRST
    name_mappings = {
        "Ægon": "Aegon",
        "M.O.D.O.K.": "M.O.D.O.K.",
        "Joe Fixit": "Joe_Fixit",
        "Agent Venom": "Agent_Venom",
        "Civil Warrior": "Civil_Warrior",
        "Spider-Gwen": "Spider-Gwen",
        "Spider-Man (Classic)": "Spider-Man_(Classic)",
        "Spider-Man (Stark Enhanced)": "Spider-Man_(Stark_Enhanced)",
        "Spider-Man (Stealth Suit)": "Spider-Man_(Stealth_Suit)",
        "Captain America (Infinity War)": "Captain_America_(Infinity_War)",
        "Captain America": "Captain_America",
        "Captain Marvel (Classic)": "Captain_Marvel_(Classic)",  # Fixed this mapping
        "Captain Marvel": "Captain_Marvel",
        "Black Panther (Civil War)": "Black_Panther_(Civil_War)",
        "Black Panther": "Black_Panther",
        "Black Widow": "Black_Widow",
        "Doctor Octopus": "Doctor_Octopus",
        "Doctor Strange": "Doctor_Strange",
        "Green Goblin": "Green_Goblin",
        "Ghost Rider": "Ghost_Rider",
        "Howard The Duck": "Howard_the_Duck",
        "Hulk (Ragnarok)": "Hulk_(Ragnarok)",
        "Iron Fist": "Iron_Fist",
        "Iron Man (Infinity War)": "Iron_Man_(Infinity_War)",
        "Luke Cage": "Luke_Cage",
        "Magneto (Marvel Now!)": "Magneto_(House_of_X)",
        "Proxima Midnight": "Proxima_Midnight",
        "Red Hulk": "Red_Hulk",
        "Red Skull": "Red_Skull",
        "Rocket Raccoon": "Rocket_Raccoon",
        "Scarlet Witch": "Scarlet_Witch",
        "Star-Lord": "Star-Lord",
        "Thor (Ragnarok)": "Thor_(Ragnarok)",
        "Vision (Age of Ultron)": "Vision_(Age_of_Ultron)",
        "War Machine": "War_Machine",
        "Winter Soldier": "Winter_Soldier",
        "Wolverine (X-23)": "Wolverine_(X-23)",
        "Thor (Jane Foster)": "Thor_(Jane_Foster)",
        "Ant Man": "Ant-Man",
        "Corvus Glaive": "Corvus_Glaive",
        "Cyclops (Blue Team)": "Cyclops_(Blue_Team)",
        "Daredevil (Classic)": "Daredevil_(Classic)",
        "Cull Obsidian": "Cull_Obsidian",
        "Ebony Maw": "Ebony_Maw",
        "Human Torch": "Human_Torch",
        "Invisible Woman": "Invisible_Woman",
        "Mister Sinister": "Mister_Sinister",
        "Nick Fury": "Nick_Fury",
        "She-Hulk": "She-Hulk",
        "The Hood": "The_Hood",
        "Wasp": "Wasp"
    }
    
    # Check if we have a specific mapping for this exact name (including parentheses)
    if name in name_mappings:
        return name_mappings[name]
    else:
        # If no exact mapping, format normally by replacing spaces with underscores
        # Keep parentheses and other special characters intact for the URL
        return name.replace(' ', '_')

def scrape_wiki_page_for_image(wiki_url, character_name):
    """Scrape the wiki page to find the actual image URL"""
    try:
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(wiki_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for images with "featured" in the name
            images = soup.find_all('img')
            for img in images:
                src = img.get('src', '')
                if 'featured' in src.lower() and ('png' in src or 'jpg' in src):
                    # Make sure it's a full URL
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = 'https://marvel-contestofchampions.fandom.com' + src
                    
                    return download_image_from_url(src, character_name)
        
        return None
    except ImportError:
        #print("  BeautifulSoup not available for page scraping")
        return None
    except Exception as e:
        #print(f"  Error scraping page: {e}")
        return None

def save_image_from_response(response, character_name, number=None):
    """Save image from HTTP response"""
    try:
        # Determine file extension from content type
        content_type = response.headers.get('content-type', '').lower()
        if 'png' in content_type:
            ext = 'png'
        elif 'jpeg' in content_type or 'jpg' in content_type:
            ext = 'jpg'
        else:
            ext = 'png'  # Default
        
        number_str = f"{number:03d}_" if number else ""
        filename = f"images/{number_str}{character_name.replace(' ', '_')}.{ext}"
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        # Verify the image is valid
        try:
            img = Image.open(filename)
            img.verify()
            #print(f"    Downloaded image: {filename}")
            return filename
        except:
            os.remove(filename)
            #print(f"    Invalid image file, removed")
            return None
            
    except Exception as e:
        #print(f"    Error saving image: {e}")
        return None

def download_image_from_url(url, character_name, number=None):
    """Download image from direct URL"""
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Determine file extension
            content_type = response.headers.get('content-type', '').lower()
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = 'jpg'
            elif 'png' in content_type:
                ext = 'png'
            else:
                ext = 'jpg'  # Default
            
            number_str = f"{number:03d}_" if number else ""
            filename = f"images/{number_str}{character_name.replace(' ', '_')}.{ext}"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            # Verify the image is valid
            try:
                img = Image.open(filename)
                img.verify()
                #print(f"Downloaded image for {character_name}")
                return filename
            except:
                os.remove(filename)
                return None
    except Exception as e:
        print(f"Failed to download image for {character_name}: {e}")
    
    return None

def generate_placeholder_image(character_name, number):
    """Generate a placeholder image with character info"""
    try:
        # Create a 400x600 placeholder image
        img = Image.new('RGB', (400, 600), color='#1e3a8a')  # Marvel blue
        draw = ImageDraw.Draw(img)
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 32)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add Marvel-style design
        draw.rectangle([20, 20, 380, 580], outline='#ff0000', width=3)  # Red border
        
        # Add character name
        lines = character_name.split(' ')
        if len(lines) > 2:
            # Split into multiple lines for long names
            mid = len(lines) // 2
            line1 = ' '.join(lines[:mid])
            line2 = ' '.join(lines[mid:])
            
            bbox1 = draw.textbbox((0, 0), line1, font=font_large)
            bbox2 = draw.textbbox((0, 0), line2, font=font_large)
            
            x1 = (400 - (bbox1[2] - bbox1[0])) // 2
            x2 = (400 - (bbox2[2] - bbox2[0])) // 2
            
            draw.text((x1, 250), line1, fill='white', font=font_large)
            draw.text((x2, 290), line2, fill='white', font=font_large)
        else:
            text = character_name
            bbox = draw.textbbox((0, 0), text, font=font_large)
            x = (400 - (bbox[2] - bbox[0])) // 2
            draw.text((x, 270), text, fill='white', font=font_large)
        
        # Add "MARVEL CHAMPIONS" text
        marvel_text = "MARVEL CHAMPIONS"
        bbox = draw.textbbox((0, 0), marvel_text, font=font_small)
        x = (400 - (bbox[2] - bbox[0])) // 2
        draw.text((x, 350), marvel_text, fill='#ffcc00', font=font_small)  # Gold text
        
        # Save placeholder
        filename = f"images/{number:03d}_{character_name.replace(' ', '_')}_placeholder.png"
        img.save(filename)
        #print(f"Generated placeholder for {character_name}")
        return filename
        
    except Exception as e:
        #print(f"Failed to generate placeholder for {character_name}: {e}")
        return None

def download_image(character_name, number):
    """Try to get character image from Contest of Champions wiki"""
    #print(f"  Checking Contest of Champions wiki for {character_name}...")
    
    # Try Contest of Champions wiki first
    image_path = search_contest_wiki_image(character_name)
    if image_path:
        return image_path
    
    # If no image found, generate a placeholder
    #print(f"  No image found, generating placeholder for {character_name}")
    return generate_placeholder_image(character_name, number)

def create_secret_image(original_image_path, character_name, number):
    """Create a blacked out and blurred version of the character image"""
    if not original_image_path or not os.path.exists(original_image_path):
        return None
    
    try:
        # Open the original image
        img = Image.open(original_image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize to 300x300 to accommodate blur without cutoff
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        
        # Create a copy for the secret version
        secret_img = img.copy()
        
        # Create a black overlay that preserves the alpha channel
        black_overlay = Image.new('RGBA', secret_img.size, (0, 0, 0, 255))
        
        # Get the alpha channel from the original image
        if secret_img.mode == 'RGBA':
            # Extract alpha channel
            alpha = secret_img.split()[-1]
            
            # Apply the black overlay but keep the original alpha shape
            black_overlay.putalpha(alpha)
            secret_img = black_overlay
        else:
            # If no alpha channel, just make it black
            secret_img = black_overlay
        
        # Apply gaussian blur for mystery effect
        secret_img = secret_img.filter(ImageFilter.GaussianBlur(radius=3))
        
        # Save the secret image
        # Get the extension from the original file
        _, ext = os.path.splitext(original_image_path)
        secret_filename = f"images_secret/{number:03d}_secret.png"
        
        secret_img.save(secret_filename)
        #print(f"    Created secret image: {secret_filename}")
        return secret_filename
        
    except Exception as e:
        #print(f"    Error creating secret image for {character_name}: {e}")
        return None

def create_trading_card(number, character_name, image_path=None):
    """Create a 2.5" x 3.5" trading card"""
    # Convert inches to pixels (300 DPI)
    width = int(2.5 * 300)  # 750 pixels
    height = int(3.5 * 300)  # 1050 pixels
    
    # Create blank card with white background
    card = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(card)
    
    # Add border
    border_width = 10
    draw.rectangle(
        [border_width, border_width, width - border_width, height - border_width],
        outline='black',
        width=3
    )
    
    try:
        # Try to load different font sizes - DOUBLED the title font size!
        title_font = ImageFont.truetype("arial.ttf", 56)  # Much larger for impact!
        number_font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        number_font = ImageFont.load_default()
    
    # Handle long character names by splitting into lines (adjusted spacing for larger font)
    lines = []
    words = character_name.split()
    if len(character_name) > 15:  # Split earlier due to larger font
        if len(words) > 2:
            mid = len(words) // 2
            lines.append(' '.join(words[:mid]))
            lines.append(' '.join(words[mid:]))
        else:
            lines = [character_name]
    else:
        lines = [character_name]
    
    # Add character name at top (centered, potentially multi-line) with larger spacing
    y_offset = 30
    line_spacing = 65  # Increased spacing for larger font
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset + i * line_spacing), line, fill='black', font=title_font)
    
    # Calculate image area with adjusted spacing for larger title
    title_height = len(lines) * line_spacing + 30
    img_start_y = title_height + 25
    img_area_height = height - img_start_y - 80  # Leave space for number
    
    # Add character image if available (optimized for 256x256 transparent PNGs)
    if image_path and os.path.exists(image_path):
        try:
            # Open the character image
            char_image = Image.open(image_path)
            
            # Verify it has transparency (RGBA mode)
            if char_image.mode != 'RGBA':
                # Convert to RGBA to preserve any transparency
                char_image = char_image.convert('RGBA')
            
            # Scale the image 2x (256x256 → 512x512)
            scaled_size = (char_image.width * 2, char_image.height * 2)
            char_image = char_image.resize(scaled_size, Image.Resampling.LANCZOS)
            
            # Calculate center position for the scaled image
            img_x = (width - char_image.width) // 2  # Center horizontally
            
            # Vertically center in the available space between title and number
            available_height = img_area_height
            img_y = img_start_y + (available_height - char_image.height) // 2
            
            # Make sure the image doesn't go outside the card boundaries
            if img_y < img_start_y:
                img_y = img_start_y
            if img_y + char_image.height > height - 80:
                img_y = height - 80 - char_image.height
            
            # Convert card to RGBA temporarily to properly handle transparency
            card_rgba = card.convert('RGBA')
            
            # Paste the character image with transparency preserved
            card_rgba.paste(char_image, (img_x, img_y), char_image)
            
            # Convert back to RGB for final card
            card = Image.alpha_composite(Image.new('RGBA', card_rgba.size, 'white'), card_rgba).convert('RGB')
            
            # Recreate draw object since we replaced the card
            draw = ImageDraw.Draw(card)
            
        except Exception as e:
            print(f"  Error adding image to card for {character_name}: {e}")
    
    # Add number at bottom right in ###/100 format
    number_text = f"{number:03d}/100"  # Format as 001/100, 002/100, etc.
    bbox = draw.textbbox((0, 0), number_text, font=number_font)
    text_width = bbox[2] - bbox[0]
    x = width - text_width - 30
    y = height - 50
    draw.text((x, y), number_text, fill='black', font=number_font)
    
    # Save the card
    filename = f"cards/{number:03d}_{character_name.replace(' ', '_')}.png"
    card.save(filename, 'PNG', dpi=(300, 300))
    #print(f"  Created card: {filename}")

def redact_character_name(name):
    """Replace A-Z letters with _ (underscores) while preserving spaces and punctuation"""
    redacted = ""
    for char in name:
        if char.isalpha():  # Replace any letter (A-Z, a-z) with redaction block
            redacted += "_ "  # Add space after each underscore
        else:
            redacted += char  # Keep spaces, parentheses, hyphens, etc.
    return redacted.rstrip()  # Remove trailing space

def create_secret_trading_card(number, character_name, secret_image_path=None):
    """Create a mystery trading card with redacted character name"""
    # Convert inches to pixels (300 DPI)
    width = int(2.5 * 300)  # 750 pixels
    height = int(3.5 * 300)  # 1050 pixels
    
    # Create blank card with white background
    card = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(card)
    
    # Add border
    border_width = 10
    draw.rectangle(
        [border_width, border_width, width - border_width, height - border_width],
        outline='black',
        width=3
    )
    
    try:
        # Try to load different font sizes - same as regular cards but smaller for redacted text
        title_font = ImageFont.truetype("arial.ttf", 56)  # Same size as regular cards
        number_font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        number_font = ImageFont.load_default()
    
    # Create redacted version of character name
    redacted_name = redact_character_name(character_name)
    
    # Handle long character names by splitting into lines (same logic as regular cards)
    lines = []
    words = redacted_name.split()
    if len(redacted_name) > 15:  # Split earlier due to larger font
        if len(words) > 2:
            mid = len(words) // 2
            lines.append(' '.join(words[:mid]))
            lines.append(' '.join(words[mid:]))
        else:
            lines = [redacted_name]
    else:
        lines = [redacted_name]
    
    # Add redacted character name at top (centered, potentially multi-line)
    y_offset = 30
    line_spacing = 65  # Same spacing as regular cards
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset + i * line_spacing), line, fill='#000000', font=title_font)  # Dark red color
    
    # Calculate image area with adjusted spacing for title
    title_height = len(lines) * line_spacing + 30
    img_start_y = title_height + 25
    img_area_height = height - img_start_y - 80
    
    # Add the secret (blacked out) character image if available
    if secret_image_path and os.path.exists(secret_image_path):
        try:
            # Open the secret character image
            char_image = Image.open(secret_image_path)
            
            # Verify it has transparency (RGBA mode)
            if char_image.mode != 'RGBA':
                char_image = char_image.convert('RGBA')
            
            # Scale the image 2x (same as regular cards)
            scaled_size = (char_image.width * 2, char_image.height * 2)
            char_image = char_image.resize(scaled_size, Image.Resampling.LANCZOS)
            
            # Calculate center position
            img_x = (width - char_image.width) // 2
            available_height = img_area_height
            img_y = img_start_y + (available_height - char_image.height) // 2
            
            # Make sure the image doesn't go outside boundaries
            if img_y < img_start_y:
                img_y = img_start_y
            if img_y + char_image.height > height - 80:
                img_y = height - 80 - char_image.height
            
            # Convert card to RGBA temporarily to handle transparency
            card_rgba = card.convert('RGBA')
            card_rgba.paste(char_image, (img_x, img_y), char_image)
            card = Image.alpha_composite(Image.new('RGBA', card_rgba.size, 'white'), card_rgba).convert('RGB')
            
            # Recreate draw object
            draw = ImageDraw.Draw(card)
            
        except Exception as e:
            print(f"  Error adding secret image to card: {e}")
    
    # Add number at bottom right in ###/100 format
    number_text = f"{number:03d}/100"
    bbox = draw.textbbox((0, 0), number_text, font=number_font)
    text_width = bbox[2] - bbox[0]
    x = width - text_width - 30
    y = height - 50
    draw.text((x, y), number_text, fill='black', font=number_font)
    
    # Save the secret card with redacted name in filename
    redacted_filename = redact_character_name(character_name).replace(' ', '_')
    filename = f"cards_secret/{number:03d}_card_secret.png"
    card.save(filename, 'PNG', dpi=(300, 300))
    #print(f"  Created secret card: {filename}")

def read_unlocks_file(filename="unlocks.txt"):
    """Read the unlocks file and return a set of unlocked card numbers"""
    unlocked_cards = set()
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    parts = line.split()
                    if len(parts) >= 2:
                        card_num = parts[0]
                        status = parts[1].upper()
                        if status == "YES":
                            # Remove leading zeros and convert to int for comparison
                            unlocked_cards.add(int(card_num))
        
        #print(f"Found {len(unlocked_cards)} unlocked cards in {filename}")
        return unlocked_cards
        
    except FileNotFoundError:
        #print(f"Warning: {filename} not found. Generating all cards...")
        return set(range(1, 101))  # Generate all cards if file doesn't exist
    except Exception as e:
        #print(f"Error reading {filename}: {e}")
        #print("Generating all cards as fallback...")
        return set(range(1, 101))

def main():
    """Main function to generate all trading cards"""
    create_directories()
    
    # Read which cards are unlocked
    unlocked_cards = read_unlocks_file()
    
    if not unlocked_cards:
        #print("No cards are marked as unlocked. Exiting...")
        return
    
    #print("Starting Marvel Champions Trading Card Generator...")
    #print(f"Generating cards for {len(unlocked_cards)} unlocked champions...")
    
    cards_generated = 0
    cards_skipped_normal = 0
    cards_skipped_secret = 0
    
    for i, champion in enumerate(champions):
        number, character_name = parse_champion_info(champion)
        if number and character_name:
            card_number = int(number)
            
            # Only process if this card is unlocked
            if card_number in unlocked_cards:
                # Check if cards already exist
                normal_exists, secret_exists = check_existing_files(card_number, character_name)
                
                #print(f"Processing unlocked card {cards_generated + 1}/{len(unlocked_cards)}: #{number} {character_name}")
                
                # Handle normal card generation
                if normal_exists:
                    #print(f"  Normal card already exists, skipping...")
                    cards_skipped_normal += 1
                    image_path = None  # We'll need to find the image for secret card generation
                    
                    # Try to find existing image file for secret card generation
                    possible_extensions = ['.png', '.jpg']
                    for ext in possible_extensions:
                        possible_image = f"images/{card_number:03d}_{character_name.replace(' ', '_')}{ext}"
                        if os.path.exists(possible_image):
                            image_path = possible_image
                            break
                        # Also check for placeholder files
                        possible_placeholder = f"images/{card_number:03d}_{character_name.replace(' ', '_')}_placeholder.png"
                        if os.path.exists(possible_placeholder):
                            image_path = possible_placeholder
                            break
                else:
                    # Download image or create placeholder (only if normal card doesn't exist)
                    image_path = download_image(character_name, card_number)
                    
                    # Create regular trading card
                    create_trading_card(card_number, character_name, image_path)
                
                # Handle secret card generation
                if secret_exists:
                    #print(f"  Secret card already exists, skipping...")
                    cards_skipped_secret += 1
                else:
                    # Create secret version of the image (only if secret card doesn't exist)
                    #print(f"  Creating secret version...")
                    secret_image_path = create_secret_image(image_path, character_name, card_number)
                    
                    # Create secret trading card
                    create_secret_trading_card(card_number, character_name, secret_image_path)
                
                cards_generated += 1
                
                # Add small delay to be respectful (only if we actually downloaded something)
                if not normal_exists or not secret_exists:
                    time.sleep(1)
    
    #print("\n" + "="*50)
    #print(f"Processed {cards_generated} unlocked cards!")
    #print(f"Skipped {cards_skipped_normal} existing normal cards")
    #print(f"Skipped {cards_skipped_secret} existing secret cards")
    #print("Cards saved in 'cards/' and 'cards_secret/' directories")
    #print("Images saved in 'images/' and 'images_secret/' directories")

if __name__ == "__main__":
    main()