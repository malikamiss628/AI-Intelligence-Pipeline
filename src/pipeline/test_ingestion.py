import asyncio

from src.pipeline.ingestion import ingest_website


async def main():
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    result = await ingest_website(url)

    print("\n--- INGESTION REPORT ---")

    if result:
        print("Status:", result["status"])
        print("Website:", result["url"])
        print("Title:", result["title"])
        print("Chunks stored:", result["chunks"])


if __name__ == "__main__":
    asyncio.run(main())
    