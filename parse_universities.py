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
        url_match = re.search(r'href="([^"]+)"\s+target="_blank"[^>]*>.*?University website', item)
        if url_match:
            url = url_match.group(1)

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

                # Extract Places for THIS agreement
                places = "0"
                places_match = re.search(r'Available places</span><div><span[^>]*>(\d+)</span>\s*<span[^>]*>/\s*</span>\s*<span[^>]*>(\d+)</span>', agreement, re.DOTALL)
                if places_match:
                     places = places_match.group(2) # Total
                else:
                    simple_match = re.search(r'Available places</span>.*?<h6[^>]*>(\d+)</h6>', agreement, re.DOTALL)
                    if simple_match:
                        places = simple_match.group(1)

                fields_data.append({
                    "name": field_name,
                    "places": places
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
if os.path.exists('MobiTUL.html'):
    all_universities.extend(parse_file('MobiTUL.html'))
if os.path.exists('MobiTUL2.html'):
    all_universities.extend(parse_file('MobiTUL2.html'))

print(json.dumps(all_universities, indent=2))
