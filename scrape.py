import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def clean_html(soup):
    for tag in soup(["script", "style", "iframe", "noscript", "svg", "footer", "aside", "form", "meta", "link"]):
        tag.decompose()
    return soup

def save_image(img_url, base_url, output_dir):
    full_url = urljoin(base_url, img_url)
    parsed = urlparse(full_url)
    file_name = os.path.basename(parsed.path) or 'image.jpg'
    local_path = os.path.join('images', file_name)
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)

    try:
        img_data = requests.get(full_url, timeout=5).content
        with open(os.path.join(output_dir, local_path), 'wb') as f:
            f.write(img_data)
        return local_path
    except:
        return None

def rebuild_website_clean(base_url, output_dir='rebuilt_site'):
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Fetch and parse the HTML
    html = requests.get(base_url).text
    soup = BeautifulSoup(html, 'html.parser')
    soup = clean_html(soup)

    # Step 2: Extract content sections
    main = soup.find('main') or soup.body
    header = soup.find('header')
    nav = soup.find('nav')

    # Step 3: Rewrite image URLs and download them
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            new_path = save_image(src, base_url, output_dir)
            if new_path:
                img['src'] = new_path

    # Step 4: Rebuild minimal HTML
    html_output = ['<html><head><meta charset="UTF-8"><title>Minimal Site</title></head><body style="font-family: sans-serif; max-width: 800px; margin: auto;">']

    if header:
        html_output.append(f"<header>{header.decode_contents()}</header>")

    if nav:
        html_output.append(f"<nav>{nav.decode_contents()}</nav>")

    html_output.append("<main>")
    html_output.append(main.decode_contents())
    html_output.append("</main>")

    html_output.append("</body></html>")

    # Step 5: Save HTML
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_output))

    print(f"Cleaned website saved to {output_dir}/index.html")

# Usage
if __name__ == '__main__':
    url = input("Enter the website URL: ")
    rebuild_website_clean(url)

