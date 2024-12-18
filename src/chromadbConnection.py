#DO one thing and do it well

import chromadb
from chromadb.config import DEFAULT_TENANT

client = chromadb.PersistentClient(path="/db/")