const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  // Configuration
  const startUrl = 'https://redplanetlabs.com/docs/~/index.html';
  const outputDir = './raw_html';
  const imgDir = './images';
  const maxPages = 200;
  
  // Ensure directories exist
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
  if (!fs.existsSync(imgDir)) fs.mkdirSync(imgDir, { recursive: true });
  
  // Track progress
  const visitedUrls = new Set();
  const urlsToVisit = [startUrl];
  const urlToFilename = new Map();
  let pageCounter = 0;
  
  console.log('Starting Puppeteer scraper...');
  
  // Launch browser
  const browser = await puppeteer.launch({
    headless: "new",  // Use new headless mode
  });
  
  try {
    const page = await browser.newPage();
    
    // Set a realistic viewport and user agent
    await page.setViewport({ width: 1366, height: 768 });
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
    
    // Process pages until no more URLs to visit or reached limit
    while (urlsToVisit.length > 0 && visitedUrls.size < maxPages) {
      const currentUrl = urlsToVisit.shift();
      
      // Skip if already visited
      if (visitedUrls.has(currentUrl)) continue;
      visitedUrls.add(currentUrl);
      
      // Generate a filename for this URL
      const pageId = pageCounter++;
      const filename = `page_${pageId.toString().padStart(3, '0')}.html`;
      urlToFilename.set(currentUrl, filename);
      
      console.log(`[${visitedUrls.size}/${maxPages}] Processing: ${currentUrl} -> ${filename}`);
      
      try {
        // Navigate to the page and wait for content to load
        await page.goto(currentUrl, { 
          waitUntil: 'networkidle2',
          timeout: 30000
        });
        
        // Give additional time for any dynamic rendering
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Expand all sections if needed
        await expandAllSections(page);
        
        // Save the full HTML content
        const content = await page.content();
        fs.writeFileSync(path.join(outputDir, filename), content);
        
        // Also save a screenshot for reference
        await page.screenshot({ 
          path: path.join(imgDir, `screenshot_${pageId.toString().padStart(3, '0')}.png`),
          fullPage: true 
        });
        
        // Extract all documentation links from the page
        const links = await page.evaluate(() => {
          return Array.from(document.querySelectorAll('a[href]'))
            .map(a => a.href)
            .filter(href => {
              // Filter for documentation links
              return href.includes('redplanetlabs.com/docs/') && 
                     !href.includes('mailto:') &&
                     !href.startsWith('javascript:');
            });
        });
        
        // Add new links to the queue
        for (const link of links) {
          // Normalize the URL (remove hash fragments if needed)
          const normalizedLink = link.split('#')[0];
          if (!visitedUrls.has(normalizedLink) && !urlsToVisit.includes(normalizedLink)) {
            urlsToVisit.push(normalizedLink);
          }
        }
        
      } catch (error) {
        console.error(`Error processing ${currentUrl}:`, error.message);
      }
      
      // Be respectful to the server
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    // Save the URL to filename mapping for the Python script
    const urlMap = {};
    for (const [url, filename] of urlToFilename.entries()) {
      urlMap[url] = filename;
    }
    fs.writeFileSync('url_mapping.json', JSON.stringify(urlMap, null, 2));
    
    console.log(`Finished scraping. Visited ${visitedUrls.size} pages.`);
    
  } finally {
    await browser.close();
  }
})();

// Helper function to expand collapsible sections
async function expandAllSections(page) {
  try {
    // This is a generic approach - you'll need to customize based on Red Planet Labs' site structure
    // For example, clicking on all collapse buttons or expanding all accordion sections
    
    // Example: Click all elements with a certain class (modify selector as needed)
    const expandButtons = await page.$$('.expandable-section-button');
    for (const button of expandButtons) {
      await button.click();
      await new Promise(resolve => setTimeout(resolve, 300)); // Brief delay between clicks
    }
    
    // You might need to scroll the page to load lazy content
    await autoScroll(page);
    
  } catch (error) {
    console.log('Error expanding sections:', error.message);
  }
}

// Helper function to scroll the page
async function autoScroll(page) {
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      const distance = 100;
      const timer = setInterval(() => {
        const scrollHeight = document.body.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;
        
        if (totalHeight >= scrollHeight) {
          clearInterval(timer);
          resolve();
        }
      }, 100);
    });
  });
}