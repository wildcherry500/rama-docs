import os
import json
import re
from bs4 import BeautifulSoup
import shutil
from urllib.parse import urljoin, urlparse
# Add debug print
print("BeautifulSoup processor starting...")

# Configuration
raw_html_dir = './raw_html'
output_dir = './processed_docs'
url_mapping_file = 'url_mapping.json'
base_url = 'https://redplanetlabs.com/docs/'
# Add debug print
print(f"Looking for HTML files in: {os.path.abspath(raw_html_dir)}")
print(f"Output directory: {os.path.abspath(output_dir)}")

# Check if directories exist
if not os.path.exists(raw_html_dir):
    print(f"ERROR: Raw HTML directory not found: {raw_html_dir}")
if not os.path.exists(url_mapping_file):
    print(f"ERROR: URL mapping file not found: {url_mapping_file}")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load URL mapping
with open(url_mapping_file, 'r') as f:
    url_mapping = json.load(f)

# Reverse mapping for looking up URLs by filename
filename_to_url = {v: k for k, v in url_mapping.items()}

# Process each HTML file
def process_file(filename):
    print(f"Processing {filename}")
    file_path = os.path.join(raw_html_dir, filename)
    
    # Skip if file doesn't exist
    if not os.path.exists(file_path):
        print(f"  File not found: {file_path}")
        return
    
    # Get the original URL for this file
    original_url = filename_to_url.get(filename, "")
    
    # Parse the HTML
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract the main content - modify these selectors based on the actual site structure
    main_content = soup.find('div', class_='main-content')
    if not main_content:
        main_content = soup.find('div', id='content')
    if not main_content:
        # Fallback to body if can't find content div
        main_content = soup.body
    
    if not main_content:
        print(f"  Could not find main content in {filename}")
        return
    
    # Extract title
    title_element = soup.find('title')
    title = title_element.text if title_element else "Untitled Document"
    
    # Clean title for filename
    clean_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    clean_title = re.sub(r'[-\s]+', '-', clean_title)
    
    # Create output filename
    output_filename = f"{filename.replace('.html', '')}_processed.md"
    output_path = os.path.join(output_dir, output_filename)
    
    # Process images
    process_images(main_content, original_url, filename)
    
    # Process links to point to other processed files
    process_links(main_content)
    
    # Create markdown content
    markdown_content = f"# {title}\n\n"
    markdown_content += f"Original URL: {original_url}\n\n"
    
    # Extract and add headings and paragraphs
    for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'code', 'ul', 'ol', 'table']):
        if element.name.startswith('h'):
            level = int(element.name[1])
            markdown_content += f"{'#' * level} {element.text.strip()}\n\n"
        elif element.name == 'p':
            markdown_content += f"{element.text.strip()}\n\n"
        elif element.name == 'pre' or element.name == 'code':
            code_text = element.text.strip()
            markdown_content += f"```\n{code_text}\n```\n\n"
        elif element.name == 'ul' or element.name == 'ol':
            for li in element.find_all('li'):
                markdown_content += f"* {li.text.strip()}\n"
            markdown_content += "\n"
        elif element.name == 'table':
            # Simple table handling
            markdown_content += "| "
            headers = element.find_all('th')
            if headers:
                markdown_content += " | ".join([h.text.strip() for h in headers])
                markdown_content += " |\n| "
                markdown_content += " | ".join(["---" for _ in headers])
                markdown_content += " |\n"
            
            for row in element.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if cells and not all(cell.name == 'th' for cell in cells):
                    markdown_content += "| "
                    markdown_content += " | ".join([cell.text.strip() for cell in cells])
                    markdown_content += " |\n"
            markdown_content += "\n"
    
    # Save the processed content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"  Saved to {output_path}")
    return output_path

def process_images(content, original_url, source_filename):
    """Extract and save images, updating their references"""
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    for img in content.find_all('img'):
        src = img.get('src', '')
        if not src:
            continue
        
        # Convert relative URL to absolute
        absolute_src = urljoin(original_url, src)
        
        # Generate a filename for the image
        img_filename = os.path.basename(urlparse(absolute_src).path)
        if not img_filename or img_filename == '':
            img_filename = f"image_{hash(absolute_src) % 10000}.png"
        
        # Reference to the screenshot taken during the Puppeteer phase
        source_base = source_filename.replace('.html', '')
        screenshot_path = f"./images/screenshot_{source_base[5:8]}.png"
        
        # Copy the screenshot to the images directory if it exists
        if os.path.exists(screenshot_path):
            dest_path = os.path.join(images_dir, img_filename)
            shutil.copy(screenshot_path, dest_path)
            print(f"  Copied image to {dest_path}")
        
        # Update the image reference
        img['src'] = f"images/{img_filename}"

def process_links(content):
    """Update links to point to processed files"""
    for link in content.find_all('a', href=True):
        href = link.get('href', '')
        if not href or href.startswith('#') or href.startswith('mailto:'):
            continue
        
        # Try to find the target file
        for url, filename in url_mapping.items():
            if url in href or href in url:
                # Update the link to point to the processed file
                processed_filename = filename.replace('.html', '_processed.md')
                link['href'] = processed_filename
                break

# Process all HTML files
def main():
    print("Starting BeautifulSoup processor...")
    
    files_processed = 0
    for filename in os.listdir(raw_html_dir):
        if filename.endswith('.html'):
            output_path = process_file(filename)
            if output_path:
                files_processed += 1
    
    print(f"Finished processing {files_processed} files.")
    
    # Create an index file with links to all processed documents
    create_index_file()

def create_index_file():
    """Create an index markdown file with links to all processed documents"""
    index_path = os.path.join(output_dir, 'index.md')
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# Red Planet Labs Documentation Index\n\n")
        
        for filename in sorted(os.listdir(output_dir)):
            if filename.endswith('_processed.md') and filename != 'index.md':
                # Try to extract a title
                doc_path = os.path.join(output_dir, filename)
                title = filename
                
                try:
                    with open(doc_path, 'r', encoding='utf-8') as doc_file:
                        first_line = doc_file.readline().strip()
                        if first_line.startswith('# '):
                            title = first_line[2:]
                except:
                    pass
                
                f.write(f"* [{title}]({filename})\n")
    
    print(f"Created index file at {index_path}")

if __name__ == "__main__":
    main()