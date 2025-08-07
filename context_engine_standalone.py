#!/usr/bin/env python3
"""
Context Engineering - Modern Research Showcase
=============================================

A comprehensive, modern website showcasing the Context Engineering repository
with interactive diagrams, paradigm explanations, and visual demonstrations.
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
    title="Context Engineering Research Hub",
    description="Beyond Prompt Engineering - The Science of Context",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchQuery(BaseModel):
    topic: str
    paradigm: Optional[str] = None
    complexity_level: Optional[str] = "intermediate"

@app.get("/health")
@app.head("/health")
async def health_check():
    """Health check endpoint for Kubernetes ingress."""
    return {
        "status": "healthy",
        "service": "context-engineering-research",
        "version": "2.0.0",
        "timestamp": time.time()
    }

@app.get("/api/research-areas")
async def get_research_areas():
    """Get all research areas and paradigms."""
    return {
        "paradigms": [
            {
                "id": "biological_metaphor",
                "name": "Biological Metaphor",
                "description": "From atoms to neural fields - a progressive complexity framework",
                "levels": ["Atoms", "Molecules", "Cells", "Organs", "Neural Systems", "Neural Fields"],
                "color": "#4f46e5"
            },
            {
                "id": "field_theory",
                "name": "Neural Field Theory", 
                "description": "Context as continuous semantic landscapes with resonance and persistence",
                "concepts": ["Resonance", "Persistence", "Attractors", "Boundaries"],
                "color": "#059669"
            },
            {
                "id": "symbolic_mechanisms",
                "name": "Symbolic Mechanisms",
                "description": "Emergent symbol processing in LLMs through three-stage architecture",
                "stages": ["Symbol Abstraction", "Symbolic Induction", "Retrieval"],
                "color": "#dc2626"
            },
            {
                "id": "quantum_semantics", 
                "name": "Quantum Semantics",
                "description": "Observer-dependent meaning with non-classical contextuality",
                "principles": ["Superposition", "Measurement", "Non-Commutativity", "Contextuality"],
                "color": "#7c3aed"
            },
            {
                "id": "cognitive_tools",
                "name": "Cognitive Tools",
                "description": "Structured reasoning through modular cognitive operations",
                "operations": ["Understand", "Extract", "Highlight", "Apply", "Validate"],
                "color": "#ea580c"
            }
        ],
        "research_institutions": [
            {"name": "IBM Zurich", "focus": "Cognitive Tools Framework"},
            {"name": "Princeton ICML", "focus": "Symbolic Processing"},
            {"name": "Indiana University", "focus": "Quantum Semantics"},
            {"name": "Singapore-MIT", "focus": "Memory Systems"},
            {"name": "Shanghai AI Lab", "focus": "Neural Fields"}
        ]
    }

@app.post("/api/explore-paradigm")
async def explore_paradigm(query: ResearchQuery):
    """Explore a specific paradigm with examples."""
    
    paradigm_data = {
        "biological_metaphor": {
            "overview": "Context engineering progresses through biological complexity levels, from simple atomic prompts to sophisticated neural field dynamics.",
            "progression": [
                {"level": "Atoms", "description": "Single instructions and basic prompts", "example": "Translate 'hello' to French"},
                {"level": "Molecules", "description": "Few-shot examples and demonstrations", "example": "dog -> animal\ncar -> vehicle\nrose -> ?"},
                {"level": "Cells", "description": "Stateful memory and conversation persistence", "example": "Maintaining context across conversation turns"},
                {"level": "Organs", "description": "Multi-step workflows and agent orchestration", "example": "Research → Analyze → Synthesize → Present"},
                {"level": "Neural Systems", "description": "Cognitive tools extending reasoning capabilities", "example": "Using structured reasoning frameworks"},
                {"level": "Neural Fields", "description": "Continuous semantic landscapes with emergent properties", "example": "Context as resonating information medium"}
            ],
            "diagram_data": {
                "nodes": [
                    {"id": "atoms", "label": "Atoms", "level": 0, "color": "#fee2e2"},
                    {"id": "molecules", "label": "Molecules", "level": 1, "color": "#fef3c7"},
                    {"id": "cells", "label": "Cells", "level": 2, "color": "#d1fae5"},
                    {"id": "organs", "label": "Organs", "level": 3, "color": "#dbeafe"},
                    {"id": "neural_systems", "label": "Neural Systems", "level": 4, "color": "#e0e7ff"},
                    {"id": "neural_fields", "label": "Neural Fields", "level": 5, "color": "#f3e8ff"}
                ],
                "connections": [
                    {"source": "atoms", "target": "molecules"},
                    {"source": "molecules", "target": "cells"},
                    {"source": "cells", "target": "organs"},
                    {"source": "organs", "target": "neural_systems"},
                    {"source": "neural_systems", "target": "neural_fields"}
                ]
            }
        },
        "field_theory": {
            "overview": "Neural fields treat context as continuous semantic medium where information persists through resonance rather than explicit storage.",
            "key_concepts": [
                {"concept": "Resonance", "description": "Information patterns that align and reinforce each other", "visual": "wave_interference"},
                {"concept": "Persistence", "description": "Field states maintain activation patterns over time", "visual": "field_decay"},
                {"concept": "Attractors", "description": "Stable configurations that draw semantic patterns", "visual": "attractor_basin"},
                {"concept": "Boundaries", "description": "Permeable interfaces controlling information flow", "visual": "boundary_dynamics"}
            ],
            "field_equations": {
                "resonance": "R(t) = ∫ f₁(x,t) · f₂(x,t) dx",
                "persistence": "P(t) = P₀ · e^(-λt)",
                "attractor_strength": "A = ∇²φ + F(φ)",
                "boundary_permeability": "J = -D∇φ · n̂"
            },
            "applications": [
                "Long-term conversation memory",
                "Semantic coherence maintenance", 
                "Context compression without information loss",
                "Cross-domain knowledge transfer"
            ]
        },
        "symbolic_mechanisms": {
            "overview": "LLMs develop emergent three-stage symbolic architecture enabling abstract reasoning through variable manipulation.",
            "three_stages": [
                {
                    "stage": "Symbol Abstraction", 
                    "layer": "Early Layers",
                    "function": "Convert input tokens to abstract variables based on relations",
                    "example": "['dog', 'cat', 'dog'] → [A, B, A]"
                },
                {
                    "stage": "Symbolic Induction",
                    "layer": "Intermediate Layers", 
                    "function": "Recognize patterns over abstract variables",
                    "example": "[A, B, A] pattern recognition across instances"
                },
                {
                    "stage": "Retrieval",
                    "layer": "Later Layers",
                    "function": "Map abstract variables back to concrete tokens", 
                    "example": "A → 'dog' in current context"
                }
            ],
            "research_evidence": "Yang et al. (2025) demonstrated these mechanisms through causal mediation analysis",
            "implications": [
                "Design contexts emphasizing abstract patterns",
                "Leverage indirection for flexible reasoning",
                "Create transparent symbolic operations",
                "Support generalization across domains"
            ]
        },
        "quantum_semantics": {
            "overview": "Meaning exists in superposition until actualized through observer interaction, exhibiting non-classical contextuality.",
            "quantum_principles": [
                {
                    "principle": "Superposition",
                    "description": "Multiple interpretations exist simultaneously",
                    "equation": "|ψ⟩ = Σᵢ cᵢ|eᵢ⟩"
                },
                {
                    "principle": "Measurement", 
                    "description": "Context collapses superposition to specific meaning",
                    "equation": "|ψ_interpreted⟩ = O|ψ⟩/||O|ψ⟩||"
                },
                {
                    "principle": "Non-Commutativity",
                    "description": "Order of context application matters",
                    "equation": "[O_A, O_B] = O_A O_B - O_B O_A ≠ 0"
                },
                {
                    "principle": "Contextuality",
                    "description": "Bell inequality violations in meaning",
                    "equation": "|CHSH| > 2 (observed: 2.3-2.8)"
                }
            ],
            "semantic_degeneracy": {
                "formula": "P(perfect) ≈ (1/db)^K(M(SE))",
                "explanation": "Interpretation probability decreases exponentially with semantic complexity"
            },
            "applications": [
                "Bayesian interpretation sampling",
                "Ambiguity-aware context design", 
                "Non-classical context operations",
                "Observer-dependent meaning systems"
            ]
        },
        "cognitive_tools": {
            "overview": "Structured reasoning through modular cognitive operations that enhance LLM capabilities systematically.",
            "five_operations": [
                {"tool": "Understand", "purpose": "Comprehend the problem structure and requirements"},
                {"tool": "Extract", "purpose": "Identify relevant information and key concepts"},
                {"tool": "Highlight", "purpose": "Emphasize critical patterns and relationships"},
                {"tool": "Apply", "purpose": "Execute reasoning operations and transformations"},
                {"tool": "Validate", "purpose": "Verify results and check for consistency"}
            ],
            "research_source": "IBM Zurich demonstrated 26.7% → 43.3% improvement on AIME2024",
            "implementation": {
                "prompt_templates": "Cognitive tools as structured prompt templates",
                "tool_calls": "Operations encapsulated as callable functions",
                "reasoning_scaffolds": "Step-by-step cognitive frameworks",
                "verification_loops": "Built-in validation and backtracking"
            },
            "benefits": [
                "Transparent reasoning processes",
                "Improved problem-solving accuracy",
                "Modular and composable operations",
                "Reduces cognitive load on base model"
            ]
        }
    }
    
    if query.topic not in paradigm_data:
        raise HTTPException(status_code=404, detail="Paradigm not found")
    
    return {
        "success": True,
        "paradigm": query.topic,
        "data": paradigm_data[query.topic],
        "complexity_level": query.complexity_level,
        "timestamp": time.time()
    }

@app.get("/api/research-metrics")
async def get_research_metrics():
    """Get research metrics and statistics."""
    return {
        "repository_stats": {
            "research_papers": 1400,
            "institutions": 6,
            "paradigms": 5,
            "implementation_examples": 50,
            "active_contributors": 25
        },
        "performance_metrics": {
            "cognitive_tools_improvement": "26.7% → 43.3% (AIME2024)",
            "mem1_efficiency": "2x faster long-horizon tasks",
            "symbolic_mechanisms": "3-stage architecture identified",
            "quantum_contextuality": "2.3-2.8 CHSH violations",
            "field_theory_applications": "Continuous context beyond token limits"
        },
        "research_impact": {
            "arxiv_papers": 8,
            "icml_publications": 2,
            "industry_adoption": "Growing",
            "academic_citations": "Increasing"
        }
    }

@app.get("/", response_class=HTMLResponse)
async def serve_research_hub():
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
        .tour-btn, .workflow-btn {
            background: #48bb78;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-left: 10px;
        }
        .tour-btn:hover, .workflow-btn:hover {
            background: #38a169;
        }
        .tour-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .tour-content {
            background: white;
            padding: 30px;
            border-radius: 12px;
            max-width: 600px;
            margin: 20px;
            text-align: center;
        }
        .tour-controls {
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .tour-controls button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }
        .close-tour {
            background: #e53e3e !important;
            color: white !important;
        }
        .workflow-panel {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .workflow-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .workflow-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            cursor: pointer;
            transition: all 0.3s;
        }
        .workflow-card:hover {
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        .workflow-card h5 {
            margin: 0 0 8px 0;
            color: #4a5568;
        }
        .workflow-card p {
            margin: 0;
            font-size: 14px;
            color: #718096;
        }
        .query-suggestions {
            margin: 15px 0;
            padding: 15px;
            background: #edf2f7;
            border-radius: 8px;
        }
        .suggestion-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            margin: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        .suggestion-btn:hover {
            background: #5a6fd8;
        }
        .value-highlight {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .step-indicator {
            background: #48bb78;
            color: white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
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
            <div class="value-highlight">
                <strong>🎯 Value Proposition:</strong> This isn't just another AI model - it's a complete contextual reasoning system that combines 6 research breakthroughs into a unified framework for superior AI performance.
            </div>
            <div class="component-list">
                <div class="component">
                    <h4><span class="step-indicator">1</span> 🧠 Cognitive Tools (IBM Zurich)</h4>
                    <p><strong>Value:</strong> 5-stage structured reasoning (Understand → Extract → Highlight → Apply → Validate) ensures comprehensive problem analysis</p>
                    <p><em>Research Impact:</em> Modular cognitive operations with adaptive tool selection</p>
                </div>
                <div class="component">
                    <h4><span class="step-indicator">2</span> 🌊 Neural Fields (Shanghai AI Lab)</h4>
                    <p><strong>Value:</strong> Dynamic information processing with pattern injection and emergent behavior formation</p>
                    <p><em>Research Impact:</em> Field evolution with attractor dynamics for complex reasoning</p>
                </div>
                <div class="component">
                    <h4><span class="step-indicator">3</span> 🧮 Memory Systems (Singapore-MIT MEM1)</h4>
                    <p><strong>Value:</strong> Intelligent consolidation and retrieval for long-term contextual understanding</p>
                    <p><em>Research Impact:</em> Memory-reasoning synergy with adaptive budget management</p>
                </div>
                <div class="component">
                    <h4><span class="step-indicator">4</span> 🔣 Symbolic Processing (Princeton ICML)</h4>
                    <p><strong>Value:</strong> Three-stage symbolic reasoning (Abstraction → Induction → Retrieval) for logical coherence</p>
                    <p><em>Research Impact:</em> Pattern recognition with generalization and validation</p>
                </div>
                <div class="component">
                    <h4><span class="step-indicator">5</span> ⚛️ Quantum Semantics (Indiana University)</h4>
                    <p><strong>Value:</strong> Observer-dependent meaning resolution for context-aware interpretation</p>
                    <p><em>Research Impact:</em> Semantic superposition with measurement-based disambiguation</p>
                </div>
                <div class="component">
                    <h4><span class="step-indicator">6</span> 📈 Progressive Complexity</h4>
                    <p><strong>Value:</strong> Adaptive scaling from simple to complex reasoning (Atom→Molecule→Cell→Organ→System→Field)</p>
                    <p><em>Research Impact:</em> Performance-based auto-scaling with efficiency monitoring</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentTourStep = 0;
        const tourSteps = [
            {
                title: "Welcome to Context Engineering 🧠",
                text: "This framework integrates cutting-edge research from 6 leading institutions into a unified contextual AI system. Unlike traditional AI, this provides structured reasoning with full transparency."
            },
            {
                title: "Multi-Stage Cognitive Processing 🔄",
                text: "Every query goes through 5 cognitive stages: Understanding → Information Extraction → Pattern Highlighting → Reasoning Application → Validation. This ensures comprehensive analysis."
            },
            {
                title: "Research Integration Power 🎓",
                text: "We combine IBM Zurich's cognitive tools, Shanghai AI Lab's neural fields, Singapore-MIT's memory systems, Princeton's symbolic processing, Indiana University's quantum semantics, and progressive complexity management."
            },
            {
                title: "Dynamic Field Processing 🌊",
                text: "Neural fields create dynamic information landscapes where patterns emerge naturally. This allows for non-linear reasoning and creative problem-solving that traditional AI cannot achieve."
            },
            {
                title: "Adaptive Complexity Scaling 📈",
                text: "The system automatically scales from simple (Atom-level) to complex (Field-level) reasoning based on your query. Simple questions get fast answers, complex problems get deep analysis."
            },
            {
                title: "Transparent Reasoning 🔍",
                text: "Unlike black-box AI, you see exactly how conclusions are reached through reasoning traces, confidence scores, and component usage metrics. Full transparency builds trust."
            },
            {
                title: "Ready to Experience It? 🚀",
                text: "Try the workflows below or enter your own query. Watch as multiple research breakthroughs work together to provide superior contextual understanding."
            }
        ];
        
        const workflows = {
            'research': {
                query: "Analyze the current state of quantum computing and its implications for cryptographic security over the next decade",
                description: "Multi-step research analysis combining literature synthesis, trend analysis, and future implications"
            },
            'problem-solving': {
                query: "How can we design a sustainable urban transportation system that reduces emissions by 70% while maintaining accessibility and economic viability?",
                description: "Complex problem decomposition with constraint satisfaction and solution optimization"
            },
            'creative': {
                query: "Design an innovative approach to remote team collaboration that leverages emerging technologies while addressing current pain points in distributed work",
                description: "Creative ideation grounded in contextual understanding and practical constraints"
            },
            'technical': {
                query: "Explain the architectural trade-offs between microservices and monolithic systems, considering scalability, complexity, and team structure implications",
                description: "Deep technical analysis with multi-dimensional evaluation and practical recommendations"
            }
        };

        function startTour() {
            currentTourStep = 0;
            document.getElementById('tourOverlay').style.display = 'flex';
            updateTourContent();
        }
        
        function updateTourContent() {
            const step = tourSteps[currentTourStep];
            document.getElementById('tourTitle').textContent = step.title;
            document.getElementById('tourText').textContent = step.text;
            document.getElementById('tourProgress').textContent = `${currentTourStep + 1}/${tourSteps.length}`;
        }
        
        function nextTourStep() {
            if (currentTourStep < tourSteps.length - 1) {
                currentTourStep++;
                updateTourContent();
            }
        }
        
        function previousTourStep() {
            if (currentTourStep > 0) {
                currentTourStep--;
                updateTourContent();
            }
        }
        
        function closeTour() {
            document.getElementById('tourOverlay').style.display = 'none';
        }
        
        function showWorkflows() {
            const panel = document.getElementById('workflowPanel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        }
        
        function loadWorkflow(type) {
            const workflow = workflows[type];
            document.getElementById('queryInput').value = workflow.query;
            
            // Show workflow description
            const result = document.getElementById('result');
            result.innerHTML = `
                <div class="result" style="border-left-color: #667eea;">
                    <h4>🔥 Workflow Loaded: ${type.charAt(0).toUpperCase() + type.slice(1)}</h4>
                    <p><strong>Description:</strong> ${workflow.description}</p>
                    <p><strong>Query:</strong> "${workflow.query}"</p>
                    <p>Click "Process with Context Engine" to see this workflow in action!</p>
                </div>
            `;
            
            // Hide workflow panel
            document.getElementById('workflowPanel').style.display = 'none';
            
            // Scroll to query
            document.getElementById('queryContainer').scrollIntoView({ behavior: 'smooth' });
        }
        
        function loadSuggestion(query) {
            document.getElementById('queryInput').value = query;
        }

        async function processQuery() {
            const query = document.getElementById('queryInput').value.trim();
            const resultDiv = document.getElementById('result');
            const processBtn = document.getElementById('processBtn');
            
            if (!query) {
                alert('Please enter a query first! Try the guided tour or workflows above for examples.');
                return;
            }
            
            processBtn.disabled = true;
            processBtn.textContent = '⏳ Processing through 6 research components...';
            
            resultDiv.innerHTML = `
                <div class="loading">
                    <h4>🧠 Context Engineering in Action</h4>
                    <div style="text-align: left; margin: 15px 0;">
                        <div style="margin: 5px 0;">🔍 <strong>Stage 1:</strong> Understanding & parsing your query...</div>
                        <div style="margin: 5px 0;">📊 <strong>Stage 2:</strong> Extracting key information patterns...</div>
                        <div style="margin: 5px 0;">💡 <strong>Stage 3:</strong> Highlighting relevant knowledge...</div>
                        <div style="margin: 5px 0;">⚙️ <strong>Stage 4:</strong> Applying multi-component reasoning...</div>
                        <div style="margin: 5px 0;">✅ <strong>Stage 5:</strong> Validating response coherence...</div>
                    </div>
                    <p>Processing through neural fields, memory systems, and symbolic reasoning...</p>
                </div>
            `;
            
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
                            <h4>🎯 Contextual Analysis Complete</h4>
                            <div class="value-highlight">
                                <strong>🚀 This is what makes Context Engineering superior:</strong> Your query was processed through 6 integrated research components, providing deeper understanding than any single AI model.
                            </div>
                            <p><strong>Query:</strong> ${query}</p>
                            <p><strong>Response:</strong> ${result.response}</p>
                            <div class="metrics">
                                <div class="metric">
                                    <div class="metric-value">${result.confidence}%</div>
                                    <div class="metric-label">Confidence Score</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-value">${result.processing_time}s</div>
                                    <div class="metric-label">Processing Time</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-value">${result.components_used}/6</div>
                                    <div class="metric-label">Components Used</div>
                                </div>
                            </div>
                            <div style="margin-top: 15px;">
                                <h5>🔍 Reasoning Trace (Full Transparency):</h5>
                                <ul style="text-align: left;">
                                    ${result.reasoning_trace.map(step => `<li>${step}</li>`).join('')}
                                </ul>
                            </div>
                            <div style="margin-top: 15px; padding: 10px; background: #f8f9ff; border-radius: 6px;">
                                <strong>💡 Try another workflow or ask a follow-up question to see how the system maintains context!</strong>
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
                    <div class="value-highlight">
                        <strong>🔥 Live System Status:</strong> All research components are active and ready to process your queries with superior contextual understanding.
                    </div>
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">${status.components}</div>
                            <div class="metric-label">Research Components Active</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${status.status}</div>
                            <div class="metric-label">Engine Status</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${status.version}</div>
                            <div class="metric-label">Framework Version</div>
                        </div>
                    </div>
                    <p style="text-align: center; margin-top: 10px; font-size: 14px; color: #666;">
                        IBM Zurich + Princeton ICML + Indiana University + Singapore-MIT + Shanghai AI Lab + Context Engineering
                    </p>
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
        
        // Auto-start tour for new users (optional)
        setTimeout(() => {
            const hasVisited = localStorage.getItem('contextengine_visited');
            if (!hasVisited) {
                localStorage.setItem('contextengine_visited', 'true');
                startTour();
            }
        }, 2000);
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)