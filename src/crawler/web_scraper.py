import asyncio
import aiohttp
import ssl
import certifi
from bs4 import BeautifulSoup


async def fetch_page(session, url):
    try:
        async with session.get(url, timeout=20) as response:
            response.raise_for_status()
            return await response.text()

    except Exception as error:
        print(f"Fetch error: {error}")
        return None



def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted website elements
    for element in soup([
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "aside",
        "noscript",
        "iframe",
        "svg"
    ]):
        element.decompose()

     # Extract the main Wikipedia article
    main_content = soup.select_one("#mw-content-text")

    if main_content:
        content = main_content
    else:
        content = soup.find("main") or soup.body or soup
 

    # Extract title
    title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else "No Title"
    )

    # Extract clean text
    text = content.get_text(separator=" ", strip=True)

    return {
        "title": title,
        "text": text
    }

async def scrape_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    ssl_context = ssl.create_default_context(
        cafile=certifi.where()
    )

    connector = aiohttp.TCPConnector(
        ssl=ssl_context
    )

    async with aiohttp.ClientSession(
        headers=headers,
        connector=connector
    ) as session:

        html = await fetch_page(session, url)

        if html is None:
            return None

        data = extract_text(html)

        return {
            "url": url,
            "title": data["title"],
            "text": data["text"]
        }


async def main():
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    result = await scrape_website(url)

    if result:
        print("\n--- WEBSITE DATA ---")
        print("URL:", result["url"])
        print("Title:", result["title"])
        print("\nContent Preview:")
        print(result["text"][:500])


if __name__ == "__main__":
    asyncio.run(main())