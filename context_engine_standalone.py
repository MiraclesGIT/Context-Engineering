#!/usr/bin/env python3
"""
Context Engineering FastAPI Demo Server
=======================================

FastAPI version of the Context Engineering Framework demo for proper ingress compatibility.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import json
from typing import Dict, Any, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Context Engineering Framework",
    description="A Comprehensive Contextual AI Engine",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReasoningRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class ReasoningResponse(BaseModel):
    success: bool
    query: str
    response: str
    confidence: int
    processing_time: str
    components_used: int
    reasoning_trace: list

@app.get("/health")
@app.head("/health")
async def health_check():
    """Health check endpoint for Kubernetes ingress."""
    return {
        "status": "healthy",
        "service": "context-engineering-demo",
        "version": "1.0.0",
        "timestamp": time.time()
    }

@app.get("/api/status")
async def get_status():
    """Get system status."""
    return {
        "status": "operational",
        "components": 6,
        "version": "1.0.0"
    }

@app.get("/api/demo")
async def get_demo_info():
    """Get demo API information."""
    return {
        "message": "Context Engineering Demo API",
        "endpoints": [
            "/health - Health check",
            "/api/status - System status",
            "/api/reason - Process reasoning queries"
        ]
    }

@app.post("/api/reason", response_model=ReasoningResponse)
async def process_reasoning(request: ReasoningRequest):
    """Process reasoning requests."""
    try:
        query = request.query
        
        # Mock processing (same as original demo)
        response_data = ReasoningResponse(
            success=True,
            query=query,
            response=f"🧠 Context Engineering Demo Response: This query '{query}' has been processed through our comprehensive contextual framework integrating multiple research components. The system demonstrates multi-layered reasoning combining symbolic processing, neural field dynamics, quantum semantics, and progressive complexity management to provide contextually-aware responses.",
            confidence=87,
            processing_time="1.23",
            components_used=5,
            reasoning_trace=[
                "✓ Understanding phase - Query parsed and contextualized",
                "✓ Information extraction - Key concepts identified", 
                "✓ Pattern highlighting - Relevant patterns matched",
                "✓ Reasoning application - Multi-step inference executed",
                "✓ Validation - Response coherence verified"
            ]
        )
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
@app.get("/api/demo-ui", response_class=HTMLResponse)
async def serve_demo_page():
    """Serve the main demo HTML page."""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Context Engineering Demo</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container { 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 { 
            color: #4a5568; 
            text-align: center; 
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle { 
            text-align: center; 
            color: #718096; 
            margin-bottom: 30px;
            font-size: 1.2em;
        }
        .demo-section { 
            margin: 30px 0; 
            padding: 20px; 
            border-left: 4px solid #667eea;
            background: #f8f9ff;
        }
        textarea { 
            width: 100%; 
            height: 100px; 
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
        }
        textarea:focus { 
            outline: none; 
            border-color: #667eea; 
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        button { 
            background: #667eea; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            font-size: 16px;
            font-weight: 600;
            transition: background 0.3s;
        }
        button:hover { 
            background: #5a6fd8; 
        }
        button:disabled { 
            background: #cbd5e0; 
            cursor: not-allowed; 
        }
        .result { 
            margin-top: 20px; 
            padding: 20px; 
            background: #edf2f7; 
            border-radius: 8px; 
            border-left: 4px solid #48bb78;
        }
        .error { 
            background: #fed7d7; 
            border-left-color: #e53e3e; 
        }
        .loading { 
            text-align: center; 
            color: #718096;
        }
        .component-list { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin: 20px 0;
        }
        .component { 
            padding: 15px; 
            border: 2px solid #e2e8f0; 
            border-radius: 8px; 
            background: white;
        }
        .component h4 { 
            margin: 0 0 10px 0; 
            color: #4a5568; 
        }
        .metrics { 
            display: flex; 
            gap: 20px; 
            flex-wrap: wrap; 
        }
        .metric { 
            padding: 10px 15px; 
            background: #edf2f7; 
            border-radius: 6px; 
            text-align: center; 
        }
        .metric-value { 
            font-size: 1.5em; 
            font-weight: bold; 
            color: #667eea; 
        }
        .metric-label { 
            font-size: 0.9em; 
            color: #718096; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Context Engineering</h1>
        <div class="subtitle">
            A Comprehensive Contextual AI Engine<br>
            <em>Integrating Research from IBM Zurich, Princeton ICML, Indiana University, Singapore-MIT & Shanghai AI Lab</em>
        </div>
        
        <div class="demo-section">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3>🚀 Interactive Demo</h3>
                <div>
                    <button onclick="startTour()" class="tour-btn">📖 Start Guided Tour</button>
                    <button onclick="showWorkflows()" class="workflow-btn">⚡ Example Workflows</button>
                </div>
            </div>
            
            <div id="tourOverlay" style="display: none;" class="tour-overlay">
                <div class="tour-content">
                    <h4 id="tourTitle">Welcome to Context Engineering</h4>
                    <p id="tourText">This framework integrates cutting-edge research from 6 leading institutions...</p>
                    <div class="tour-controls">
                        <button onclick="previousTourStep()">← Previous</button>
                        <span id="tourProgress">1/7</span>
                        <button onclick="nextTourStep()">Next →</button>
                        <button onclick="closeTour()" class="close-tour">✕ Close</button>
                    </div>
                </div>
            </div>
            
            <div id="workflowPanel" style="display: none;" class="workflow-panel">
                <h4>🔥 Pre-built Workflows - Click to Try</h4>
                <div class="workflow-grid">
                    <div class="workflow-card" onclick="loadWorkflow('research')">
                        <h5>🎓 Research Assistant</h5>
                        <p>Multi-step literature analysis and synthesis</p>
                    </div>
                    <div class="workflow-card" onclick="loadWorkflow('problem-solving')">
                        <h5>🧩 Complex Problem Solving</h5>
                        <p>Structured approach to challenging problems</p>
                    </div>
                    <div class="workflow-card" onclick="loadWorkflow('creative')">
                        <h5>💡 Creative Innovation</h5>
                        <p>Idea generation with contextual grounding</p>
                    </div>
                    <div class="workflow-card" onclick="loadWorkflow('technical')">
                        <h5>⚙️ Technical Analysis</h5>
                        <p>Deep technical understanding and explanation</p>
                    </div>
                </div>
            </div>
            
            <p><strong>Enter your query below or use the guided tour/workflows above:</strong></p>
            
            <div id="queryContainer">
                <textarea id="queryInput" placeholder="Enter your question or problem here...

🎯 Try these example queries:
• Research: 'Compare quantum computing approaches for optimization problems'
• Problem-Solving: 'How can we reduce carbon emissions in urban transportation?'
• Creative: 'Design a novel approach to remote team collaboration'
• Technical: 'Explain the architecture trade-offs in microservices vs monolith'"></textarea>
                
                <div class="query-suggestions" id="querySuggestions">
                    <strong>Quick Examples:</strong>
                    <button class="suggestion-btn" onclick="loadSuggestion('What are the implications of quantum supremacy for cryptography?')">Quantum & Crypto</button>
                    <button class="suggestion-btn" onclick="loadSuggestion('How might AGI development impact economic structures?')">AGI Economics</button>
                    <button class="suggestion-btn" onclick="loadSuggestion('Design a framework for ethical AI decision-making')">AI Ethics Framework</button>
                </div>
            </div>
            
            <br>
            <button onclick="processQuery()" id="processBtn">🔍 Process with Context Engine</button>
            
            <div id="result"></div>
        </div>
        
        <div class="demo-section">
            <h3>📊 System Status</h3>
            <div id="statusInfo">Loading system status...</div>
        </div>
        
        <div class="demo-section">
            <h3>🏗️ Architecture Components</h3>
            <div class="component-list">
                <div class="component">
                    <h4>🧠 Cognitive Tools (IBM Zurich)</h4>
                    <p>Structured reasoning through modular cognitive operations: Understand → Extract → Highlight → Apply → Validate</p>
                </div>
                <div class="component">
                    <h4>🌊 Neural Fields (Shanghai AI Lab)</h4>
                    <p>Dynamic field evolution with pattern injection and attractor formation for emergent behaviors</p>
                </div>
                <div class="component">
                    <h4>🧮 Memory Systems (Singapore-MIT MEM1)</h4>
                    <p>Efficient memory-reasoning synergy with intelligent consolidation and retrieval</p>
                </div>
                <div class="component">
                    <h4>🔣 Symbolic Processing (Princeton ICML)</h4>
                    <p>Three-stage symbolic processing: Abstraction → Induction → Retrieval for complex reasoning</p>
                </div>
                <div class="component">
                    <h4>⚛️ Quantum Semantics (Indiana University)</h4>
                    <p>Observer-dependent meaning actualization with semantic superposition and context collapse</p>
                </div>
                <div class="component">
                    <h4>📈 Progressive Complexity</h4>
                    <p>Adaptive cognitive architecture scaling: Atom → Molecule → Cell → Organ → Neural System → Neural Field</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function processQuery() {
            const query = document.getElementById('queryInput').value.trim();
            const resultDiv = document.getElementById('result');
            const processBtn = document.getElementById('processBtn');
            
            if (!query) {
                alert('Please enter a query first!');
                return;
            }
            
            processBtn.disabled = true;
            processBtn.textContent = '⏳ Processing...';
            
            resultDiv.innerHTML = '<div class="loading">🧠 Processing your query through the contextual engine...</div>';
            
            try {
                const response = await fetch('/api/reason', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <div class="result">
                            <h4>🎯 Result</h4>
                            <p><strong>Query:</strong> ${query}</p>
                            <p><strong>Response:</strong> ${result.response}</p>
                            <div class="metrics">
                                <div class="metric">
                                    <div class="metric-value">${result.confidence}%</div>
                                    <div class="metric-label">Confidence</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-value">${result.processing_time}s</div>
                                    <div class="metric-label">Processing Time</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-value">${result.components_used}</div>
                                    <div class="metric-label">Components Used</div>
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `<div class="result error"><strong>Error:</strong> ${result.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result error"><strong>Error:</strong> ${error.message}</div>`;
            }
            
            processBtn.disabled = false;
            processBtn.textContent = '🔍 Process with Context Engine';
        }
        
        async function loadStatus() {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();
                
                const statusDiv = document.getElementById('statusInfo');
                statusDiv.innerHTML = `
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">${status.components}</div>
                            <div class="metric-label">Active Components</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${status.status}</div>
                            <div class="metric-label">Engine Status</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${status.version}</div>
                            <div class="metric-label">Version</div>
                        </div>
                    </div>
                `;
            } catch (error) {
                document.getElementById('statusInfo').innerHTML = '<p>Status loading failed</p>';
            }
        }
        
        // Load status on page load
        loadStatus();
        
        // Allow Enter key to submit
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                processQuery();
            }
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)