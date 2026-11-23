from src.crawler.web_scraper import scrape_website
from src.utils.chunking import chunk_text
from src.utils.embeddings import generate_embeddings
from src.database.vector_store import store_chunks


async def ingest_website(url: str):
    """
    Complete ingestion pipeline:
    URL -> Scraping -> Chunking -> Embeddings -> Vector DB
    """

    print(f"\nStarting ingestion: {url}")

    # 1. Scrape website
    print("\n[1/4] Scraping website...")

    website_data = await scrape_website(url)

    if not website_data:
        print("Scraping failed!")
        return None

    text = website_data.get("text", "")
    title = website_data.get("title", "No Title")

    if not text.strip():
        print("No text extracted from website.")
        return None

    print(f"Title: {title}")
    print(f"Extracted characters: {len(text)}")

    # 2. Chunk text
    print("\n[2/4] Chunking text...")

    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=100
    )

    if not chunks:
        print("No chunks generated.")
        return None

    print(f"Generated chunks: {len(chunks)}")

    # 3. Generate embeddings
    print("\n[3/4] Generating embeddings...")

    embeddings = generate_embeddings(chunks)

    print(f"Generated embeddings: {len(embeddings)}")

    # 4. Store in vector database
    print("\n[4/4] Storing in ChromaDB...")

    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source_url=url
    )

    print("\nINGESTION COMPLETED SUCCESSFULLY!")

    return {
        "url": url,
        "title": title,
        "chunks": len(chunks),
        "status": "success"
    }