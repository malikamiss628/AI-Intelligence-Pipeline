
from src.database.vector_store import delete_source, list_stored_sources

# Delete only the dummy test website
delete_source("https://example.com")

# Verify remaining sources
list_stored_sources()
