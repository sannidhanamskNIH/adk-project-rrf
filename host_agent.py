"""
UMLS RRF Host Agent
A FastAPI-based host that wraps the UMLSAgent to provide a REST API for medical terminology analysis.
"""

import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from umls_agent import UMLSAgent

# Initialize the agent with the data file relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RRF_FILE = os.path.join(BASE_DIR, 'MRDEF.RRF')
agent = UMLSAgent(RRF_FILE)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load and parse the RRF file into memory when the server starts."""
    print(f"🚀 Initializing UMLS Agent Host...")
    if not os.path.exists(RRF_FILE):
        print(f"❌ Error: {RRF_FILE} not found. Please ensure the data file is in the correct directory.")
    else:
        success = agent.read_file()
        if success:
            print(f"✅ Data loaded successfully: {agent.total_records:,} records processed.")
        else:
            print("❌ Failed to parse RRF file during startup.")
    yield

app = FastAPI(
    title="UMLS RRF Agent Host",
    description="A hosted API service for analyzing and querying UMLS RRF medical terminology data.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Google Cloud Shell environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows access from cloudshell.dev domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Service health and overview."""
    return {
        "service": "UMLS RRF Agent Host",
        "status": "online" if agent.total_records > 0 else "initializing/error",
        "records_loaded": agent.total_records,
        "unique_concepts": len(agent.concepts)
    }

@app.get("/stats")
async def get_stats():
    """Retrieve comprehensive statistics about the loaded UMLS data."""
    if agent.total_records == 0:
        raise HTTPException(status_code=503, detail="Agent data is not loaded.")
    return agent.get_statistics()

@app.get("/concept/{cui}")
async def get_concept_details(cui: str):
    """Fetch all definitions and metadata for a specific Concept Unique Identifier (CUI)."""
    records = agent.concepts.get(cui)
    if not records:
        raise HTTPException(status_code=404, detail=f"Concept ID '{cui}' not found in the dataset.")
    return {
        "cui": cui,
        "record_count": len(records),
        "data": records
    }

@app.get("/samples")
async def get_samples(limit: int = Query(5, gt=0, le=100)):
    """Get a sample of concepts for verification and testing."""
    samples = agent.get_sample_records(limit)
    return [{"cui": cui, "definitions": records} for cui, records in samples]

@app.get("/search")
async def search_concepts(q: str = Query(..., min_length=3), limit: int = 20):
    """Search for concepts by keyword."""
    return agent.search_definitions(q, limit)

@app.get("/ui", response_class=HTMLResponse)
async def get_ui():
    """Serves a two-pane dashboard for interacting with the Agent."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>UMLS Agent Dashboard</title>
        <style>
            body { font-family: sans-serif; display: flex; height: 100vh; margin: 0; background: #f4f4f9; }
            #sidebar { width: 300px; background: #2c3e50; color: white; padding: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.1); }
            #content { flex: 1; padding: 40px; overflow-y: auto; }
            button { display: block; width: 100%; padding: 12px; margin-bottom: 10px; border: none; 
                     background: #34495e; color: white; text-align: left; cursor: pointer; border-radius: 4px; }
            button:hover { background: #465c71; }
            input { width: calc(100% - 24px); padding: 10px; margin-bottom: 10px; border-radius: 4px; border: none; }
            pre { background: white; padding: 20px; border-radius: 8px; border: 1px solid #ddd; white-space: pre-wrap; word-wrap: break-word; }
            h2 { margin-top: 0; color: #2c3e50; }
        </style>
    </head>
    <body>
        <div id="sidebar">
            <h3>UMLS Explorer</h3>
            <button onclick="fetchApi('/')">🏠 Service Health</button>
            <button onclick="fetchApi('/stats')">📊 Statistics</button>
            <button onclick="fetchApi('/samples')">🧪 Sample Data</button>
            <hr>
            <input type="text" id="searchInput" placeholder="Search keywords...">
            <button onclick="search()">🔍 Search Concepts</button>
        </div>
        <div id="content">
            <h2>Result</h2>
            <div id="status">Select an API from the left to view data.</div>
            <pre id="result">{}</pre>
        </div>
        <script>
            async function fetchApi(path) {
                const resDisplay = document.getElementById('result');
                const status = document.getElementById('status');
                status.innerText = "Loading " + path + "...";
                try {
                    const response = await fetch(path);
                    const data = await response.json();
                    resDisplay.innerText = JSON.stringify(data, null, 2);
                    status.innerText = "Showing results for: " + path;
                } catch (e) {
                    resDisplay.innerText = "Error: " + e;
                }
            }
            async function search() {
                const query = document.getElementById('searchInput').value;
                if (!query) return alert("Enter a search term");
                fetchApi('/search?q=' + encodeURIComponent(query));
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    # Default to port 8501 to match your requirements
    port = int(os.environ.get("PORT", 8501))
    print(f"📡 Starting UMLS Agent Host on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
