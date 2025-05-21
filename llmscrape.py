import json
import nest_asyncio
from scrapegraphai.graphs import SmartScraperGraph

nest_asyncio.apply()

# Replace with your Codestral API key
CODESTRAL_API_KEY = "YOUR_CODESTRAL_API_KEY"

graph_config = {
    "llm": {
        "provider": "codestral",
        "api_key": CODESTRAL_API_KEY,
        "model": "codestral-latest",  # Replace with the exact Codestral model name if needed
        "temperature": 0,
        "api_base": "https://codestral.mistral.ai/v1/chat/completions",
    },
    "verbose": True,
}

url = "https://blog.devops.dev/a-beginners-guide-to-ssh-what-it-is-and-how-to-use-it-27c118fec3d4?gi=7574a013cbf2"

prompt = (
    "You are a smart web cleaner. Extract only the **main content** from this page (text, images, links). "
    "Ignore headers, navbars, sidebars, ads, scripts, styles. "
    "Return a clean, minimal HTML page with just readable content, valid tags, no JS or external styles. "
    "Wrap everything in a complete <html><head><meta charset='UTF-8'></head><body>...</body></html> structure. "
    "Use basic <div>, <p>, <img>, <a> tags. Return only valid HTML."
)

smart_scraper_graph = SmartScraperGraph(
    prompt=prompt,
    source=url,
    config=graph_config,
)

# Run the scraper
html_result = smart_scraper_graph.run()

# Save to file
with open("plain_site.html", "w", encoding="utf-8") as f:
    f.write(html_result if isinstance(html_result, str) else str(html_result))

print("Clean HTML generated and saved as 'plain_site.html'")
