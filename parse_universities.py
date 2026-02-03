import re
import json
import os

def parse_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex patterns based on previous grep findings
    # Name: <h2 class="MuiTypography-root MuiTypography-body1 css-6u83f5">Name</h2>
    # Location container: <div class="MuiStack-root css-a8n6v4"> ... </div>
    # Inside location container: <span>Country&nbsp;• </span> <span>City</span>
    # Website: <a ... href="URL" target="_blank">... University website</a>
    # Places: ...Available places... <span ...>X</span>
    # Fields: ...Study fields... <div ...>Tags...</div>

    universities = []
    
    # Split by list items or university blocks to keep data grouped
    # <li class="MuiPaper-root ..."> contains one university
    
    items = content.split('<li class="MuiPaper-root')
    
    # Split by list items (universities)
    # The structure is <li class="MuiPaper-root ..."> ...content... </li>
    items = content.split('<li class="MuiPaper-root')

    for item in items[1:]:  # Skip the first split result which is before the first li
        
        # 1. Extract Common Data
        # Name
        name = "Unknown University"
        name_match = re.search(r'<h2[^>]*>(.*?)</h2>', item, re.DOTALL)
        if name_match:
            name = name_match.group(1).strip()
            
        # City & Country
        city = "Unknown"
        country = "Unknown"
        # Structure: <span>Country&nbsp;• </span><span>City</span>
        # Note: The bullet is often inside the first span with a non-breaking space
        location_match = re.search(r'<span[^>]*>([^<]+)&nbsp;• </span>\s*<span[^>]*>([^<]+)</span>', item)
        if location_match:
            country = location_match.group(1).strip()
            city = location_match.group(2).strip()
        else:
             # Fallback if bullet is separate (just in case)
             location_match_2 = re.search(r'<span[^>]*>([^<]+)</span>\s*•\s*<span[^>]*>([^<]+)</span>', item)
             if location_match_2:
                 country = location_match_2.group(1).replace("&nbsp;", "").strip()
                 city = location_match_2.group(2).replace("&nbsp;", "").strip()

        # URL
        url = "#"
        # Try finding the link with specifically "University website" text
        # Try finding the link with specifically "University website" text
        if "University website" in item:
            # The URL should be the last href before the text "University website"
            part_before = item.split("University website")[0]
            hrefs = re.findall(r'href="([^"]+)"', part_before)
            if hrefs:
                url = hrefs[-1]
        
        # Fallback: if URL is still "#", generate a Google Search URL
        if url == "#":
             # Create a search query URL
             query = f"{name} {city} official website"
             import urllib.parse
             encoded_query = urllib.parse.quote(query)
             url = f"https://www.google.com/search?q={encoded_query}"

        # 2. Extract Fields WITH Places
        # We need to find the inner agreement blocks and extract (Field Name, Places) from each.
        # Inner blocks start with <div class="MuiPaper-root MuiPaper-outlined ... css-hcbwp5">
        
        agreement_blocks = item.split('css-hcbwp5">')
        
        fields_data = [] # List of { "name": ..., "places": ... }

        if len(agreement_blocks) > 1:
            for agreement in agreement_blocks[1:]:
                # Extract Field Name
                # Usually in <p ... css-ctqe4l">Name</p>
                # But filter out "Available agreements" etc.
                field_name = "Unknown Field"
                
                # Try to find the field name specifically associated with the chip
                # <div class="MuiStack-root css-1ecrycj"> ... <p ...>Field</p></div>
                field_match = re.search(r'<div class="MuiStack-root css-1ecrycj">.*?<p class="MuiTypography-root MuiTypography-body1 css-ctqe4l">([^<]+)</p>', agreement, re.DOTALL)
                
                if field_match:
                    field_name = field_match.group(1).strip()
                else:
                    # Fallback: look for any p tag with that class, exclude keywords
                    simple_fields = re.findall(r'<p class="MuiTypography-root MuiTypography-body1 css-ctqe4l">([^<]+)</p>', agreement)
                    for f in simple_fields:
                        f_clean = f.strip()
                        if "Available agreements" not in f_clean and "Recruitment" not in f_clean and "Filters:" not in f_clean:
                            field_name = f_clean
                            break # Assume the first valid one is the field name
                
                if field_name == "Unknown Field":
                    continue # Skip if we can't identify a field
                    
                # Clean up
                field_name = field_name.replace("not further defined", "").strip()

                # Extract Language
                # Look for the language chip in this agreement block
                # The language chip usually contains "English", "Spanish", "German", "French", "Italian", "Portuguese" or "(B1)", "(B2)"
                # Pattern: <span class="MuiChip-label ...">Language Text</span>
                language_req = "Unknown"
                
                # Find all chips in this agreement block
                chips = re.findall(r'<span class="MuiChip-label MuiChip-labelSmall css-4y436t">([^<]+)</span>', agreement)
                
                for chip_text in chips:
                    # Filter out non-language chips
                    if any(l in chip_text for l in ["English", "Spanish", "German", "French", "Italian", "Portuguese", "B1", "B2", "C1"]) and "Degree" not in chip_text and "Winter" not in chip_text and "Summer" not in chip_text:
                        language_req = chip_text
                        break

                # Extract Places for THIS agreement
                places = "?"
                # New pattern for places based on HTML inspection:
                # <div class="MuiStack-root css-ucy7j4"> ... 
                # <div class="..."> <span class="MuiTypography-root MuiTypography-h4 css-1p9u8ia">3</span> <span ...>/</span> <span ...>4</span> </div>
                
                # We want the SECOND number (Total places), not the first (Available places which might be 0 if closed)
                # Looking at HTML: <span class="MuiTypography-root MuiTypography-h4 css-1p9u8ia">0</span> <span ...>/</span> <span class="MuiTypography-root MuiTypography-body1 css-7ykxnw">1</span>
                
                places_match = re.search(r'<span class="MuiTypography-root MuiTypography-h4[^"]*">\d+</span>\s*<span[^>]*>/\s*</span>\s*<span[^>]*>(\d+)</span>', agreement)
                
                if places_match:
                     places = places_match.group(1)
                else:
                    # Fallback: maybe just one number?
                    simple_match = re.search(r'<span class="MuiTypography-root MuiTypography-h4[^"]*">(\d+)</span>', agreement)
                    if simple_match:
                         # If there is no slash, this might be the total. 
                         # But wait, looking at the HTML "0 / 1", the first is available, second is total.
                         # If we only find one number, and it matches the first pattern, it's the available count (which is wrong for "Total Slots").
                         # Let's try to find the second span specifically.
                         pass

                    # Try a broader search for the slash pattern
                    broad_match = re.search(r'>(\d+)\s*</span>\s*<span[^>]*>/\s*</span>\s*<span[^>]*>(\d+)\s*</span>', agreement)
                    if broad_match:
                        places = broad_match.group(2)

                fields_data.append({
                    "name": field_name,
                    "places": places,
                    "language": language_req
                })

        universities.append({
            "name": name,
            "country": country,
            "city": city,
            "url": url,
            "fields": fields_data # Now a list of objects
        })

    return universities

all_universities = []
# if os.path.exists('MobiTUL.html'):
#     all_universities.extend(parse_file('MobiTUL.html'))
if os.path.exists('MobiTUL2.html'):
    all_universities.extend(parse_file('MobiTUL2.html'))

print(json.dumps(all_universities, indent=2))
