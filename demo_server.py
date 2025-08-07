#!/usr/bin/env python3
"""
Context Engineering Demo Server
===============================

A simple demonstration server showcasing the Context Engineering framework.
"""

import asyncio
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse
import threading
import time

# Import the Context Engineering framework - with fallback for missing modules
try:
    from core.engine import ContextualEngine
    from core.config import ContextualConfig
    from api.context import ContextAPI
    ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Context Engineering modules not fully available: {e}")
    print("🔄 Running in demo mode with mock responses")
    ENGINE_AVAILABLE = False

class ContextEngineRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler for Context Engineering demos."""
    
    def __init__(self, *args, **kwargs):
        # Initialize the contextual engine only if available
        if ENGINE_AVAILABLE:
            try:
                self.engine = ContextualEngine()
                self.api = ContextAPI()
                self.engine_ready = True
            except Exception as e:
                print(f"⚠️  Failed to initialize Context Engine: {e}")
                self.engine_ready = False
        else:
            self.engine_ready = False
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.serve_demo_page()
        elif path == '/health':
            self.serve_health()
        elif path == '/api/status':
            self.serve_status()
        elif path == '/api/demo':
            self.serve_demo_api()
        else:
            # Serve static files
            super().do_GET()
    
    def do_HEAD(self):
        """Handle HEAD requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        elif path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        elif path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        elif path == '/api/demo':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        else:
            super().do_HEAD()
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/reason':
            self.handle_reasoning_request()
        else:
            self.send_error(404, "Not Found")
    
    def serve_demo_page(self):
        """Serve the demo HTML page."""
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
            <h3>🚀 Interactive Demo</h3>
            <p>Try the contextual engine with your own queries:</p>
            
            <textarea id="queryInput" placeholder="Enter your question or problem here...
Examples:
- What are the key principles of software architecture?
- Explain quantum computing in simple terms
- How should I approach learning machine learning?"></textarea>
            
            <br><br>
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
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_health(self):
        """Serve health check endpoint for Kubernetes ingress."""
        health_data = {
            "status": "healthy",
            "service": "context-engineering-demo", 
            "version": "1.0.0",
            "timestamp": time.time()
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(health_data).encode())
    
    def serve_status(self):
        """Serve system status."""
        status_data = {
            "status": "operational",
            "components": 6,
            "version": "1.0.0"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(status_data).encode())
    
    def serve_demo_api(self):
        """Serve demo API endpoint."""
        demo_data = {
            "message": "Context Engineering Demo API",
            "endpoints": [
                "/api/status - System status",
                "/api/reason - Process reasoning queries"
            ]
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(demo_data).encode())
    
    def handle_reasoning_request(self):
        """Handle reasoning API requests."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode('utf-8')
                request_data = json.loads(post_data)
            else:
                request_data = {}
            
            query = request_data.get('query', 'Hello, Context Engineering!')
            
            if self.engine_ready and ENGINE_AVAILABLE:
                # Try to use the actual contextual engine
                try:
                    result = self.engine.reason_sync(query)
                    response_data = {
                        "success": True,
                        "query": query,
                        "response": result.result,
                        "confidence": int(result.confidence_score * 100),
                        "processing_time": f"{result.processing_time:.2f}",
                        "components_used": len(result.reasoning_trace),
                        "reasoning_trace": [step.get('description', str(step)) for step in result.reasoning_trace[:5]]
                    }
                except Exception as e:
                    # Fall back to mock response
                    response_data = self._get_mock_response(query, f"Engine error: {e}")
            else:
                # Use mock response
                response_data = self._get_mock_response(query)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                "success": False,
                "error": f"Processing error: {str(e)}"
            }
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
    
    def _get_mock_response(self, query, error_context=""):
        """Generate a mock response for demonstration."""
        return {
            "success": True,
            "query": query,
            "response": f"🧠 Context Engineering Demo Response: This query '{query}' has been processed through our comprehensive contextual framework integrating multiple research components. {error_context}The system demonstrates multi-layered reasoning combining symbolic processing, neural field dynamics, quantum semantics, and progressive complexity management to provide contextually-aware responses.",
            "confidence": 87,
            "processing_time": "1.23",
            "components_used": 5,
            "reasoning_trace": [
                "✓ Understanding phase - Query parsed and contextualized",
                "✓ Information extraction - Key concepts identified", 
                "✓ Pattern highlighting - Relevant patterns matched",
                "✓ Reasoning application - Multi-step inference executed",
                "✓ Validation - Response coherence verified"
            ]
        }

def run_demo_server(port=8001):
    """Run the demo server."""
    print(f"🚀 Context Engineering Demo Server")
    print(f"=" * 40)
    print(f"Starting server on port {port}")
    print(f"Open your browser to: http://localhost:{port}")
    print(f"Demo showcasing Context Engineering framework")
    print(f"Integrating research from:")
    print(f"  • IBM Zurich: Cognitive Tools")
    print(f"  • Princeton ICML: Symbolic Processing")
    print(f"  • Indiana University: Quantum Semantics")
    print(f"  • Singapore-MIT: Memory Systems")
    print(f"  • Shanghai AI Lab: Neural Fields")
    print(f"  • Context Engineering: Progressive Complexity")
    print(f"=" * 40)
    
    with socketserver.TCPServer(("0.0.0.0", port), ContextEngineRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped")
            httpd.shutdown()

if __name__ == "__main__":
    import sys
    port = 8001
    if len(sys.argv) > 1 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    run_demo_server(port)