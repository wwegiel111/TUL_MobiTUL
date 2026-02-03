import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

def get_og_image(url):
    if not url or url == "#":
        return None
    try:
        # Set a user agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=3) as response:
            content = response.read().decode('utf-8', errors='ignore')
            
            # Look for og:image
            match = re.search(r'<meta\s+(?:property|name)=["\']og:image["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
            if match:
                return match.group(1)
            
            # Look for twitter:image
            match = re.search(r'<meta\s+(?:property|name)=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
            if match:
                return match.group(1)
                
    except Exception as e:
        # print(f"Error fetching {url}: {e}")
        pass
    return None

def process_university(uni):
    print(f"Fetching image for {uni['name']}...")
    image_url = get_og_image(uni.get('url'))
    uni['image'] = image_url
    return uni

def enrich_universities():
    with open('universities.json', 'r', encoding='utf-8') as f:
        universities = json.load(f)

    with ThreadPoolExecutor(max_workers=10) as executor:
        enriched_universities = list(executor.map(process_university, universities))

    with open('universities.json', 'w', encoding='utf-8') as f:
        json.dump(enriched_universities, f, indent=2)

if __name__ == "__main__":
    enrich_universities()
