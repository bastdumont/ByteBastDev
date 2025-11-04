"""
Web UI for ByteClaude
Provides web interface for workflow management and monitoring
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

try:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


class WebUIServer:
    """
    Web UI server for ByteClaude
    Provides REST API and web interface
    """

    def __init__(self, host: str = "localhost", port: int = 5000, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.executions: List[Dict[str, Any]] = []

        if FLASK_AVAILABLE:
            self.app = Flask(__name__)
            CORS(self.app)
            self._setup_routes()

    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route("/", methods=["GET"])
        def index():
            """Serve main page"""
            return self._get_html_content()

        @self.app.route("/api/workflows", methods=["GET"])
        def get_workflows():
            """Get all workflows"""
            return jsonify({
                "workflows": list(self.workflows.values()),
                "count": len(self.workflows)
            })

        @self.app.route("/api/workflows/<workflow_id>", methods=["GET"])
        def get_workflow(workflow_id):
            """Get specific workflow"""
            if workflow_id in self.workflows:
                return jsonify(self.workflows[workflow_id])
            return jsonify({"error": "Workflow not found"}), 404

        @self.app.route("/api/workflows", methods=["POST"])
        def create_workflow():
            """Create new workflow"""
            data = request.json
            workflow_id = f"workflow_{len(self.workflows) + 1}"
            
            self.workflows[workflow_id] = {
                "id": workflow_id,
                "name": data.get("name", "Unnamed"),
                "description": data.get("description", ""),
                "nodes": data.get("nodes", []),
                "connections": data.get("connections", []),
                "created_at": datetime.now().isoformat(),
                "status": "draft"
            }
            
            return jsonify(self.workflows[workflow_id]), 201

        @self.app.route("/api/workflows/<workflow_id>/execute", methods=["POST"])
        def execute_workflow(workflow_id):
            """Execute a workflow"""
            if workflow_id not in self.workflows:
                return jsonify({"error": "Workflow not found"}), 404

            execution = {
                "id": f"exec_{len(self.executions) + 1}",
                "workflow_id": workflow_id,
                "status": "running",
                "started_at": datetime.now().isoformat(),
                "tasks": [],
                "progress": 0
            }
            
            self.executions.append(execution)
            self.workflows[workflow_id]["status"] = "executing"
            
            return jsonify(execution), 202

        @self.app.route("/api/executions", methods=["GET"])
        def get_executions():
            """Get all executions"""
            return jsonify({
                "executions": self.executions,
                "count": len(self.executions)
            })

        @self.app.route("/api/executions/<execution_id>", methods=["GET"])
        def get_execution(execution_id):
            """Get execution details"""
            for execution in self.executions:
                if execution["id"] == execution_id:
                    return jsonify(execution)
            return jsonify({"error": "Execution not found"}), 404

        @self.app.route("/api/health", methods=["GET"])
        def health():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "workflows_count": len(self.workflows),
                "executions_count": len(self.executions)
            })

    def _get_html_content(self) -> str:
        """Get HTML content for main page"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ByteClaude - Workflow Management</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                header {
                    background: rgba(255,255,255,0.95);
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }
                h1 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
                .subtitle { color: #666; font-size: 1.1em; }
                
                .grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 30px;
                }
                
                .card {
                    background: rgba(255,255,255,0.95);
                    border-radius: 10px;
                    padding: 25px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }
                
                .card h2 { color: #667eea; margin-bottom: 15px; font-size: 1.5em; }
                
                .status-badge {
                    display: inline-block;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    font-weight: bold;
                    margin-top: 10px;
                }
                
                .status-healthy { background: #10b981; color: white; }
                .status-running { background: #f59e0b; color: white; }
                .status-draft { background: #6b7280; color: white; }
                
                .metric {
                    display: flex;
                    justify-content: space-between;
                    padding: 12px 0;
                    border-bottom: 1px solid #eee;
                    align-items: center;
                }
                
                .metric-value {
                    font-size: 2em;
                    color: #667eea;
                    font-weight: bold;
                }
                
                .button {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 1em;
                    margin-top: 15px;
                    transition: all 0.3s ease;
                }
                
                .button:hover { 
                    background: #764ba2;
                    transform: translateY(-2px);
                }
                
                .workflow-list, .execution-list {
                    max-height: 300px;
                    overflow-y: auto;
                }
                
                .item {
                    padding: 12px;
                    background: #f9fafb;
                    margin: 8px 0;
                    border-radius: 6px;
                    border-left: 4px solid #667eea;
                }
                
                .item-title { font-weight: bold; color: #333; }
                .item-meta { font-size: 0.9em; color: #666; margin-top: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>🚀 ByteClaude Workflow Manager</h1>
                    <p class="subtitle">Automated Development Framework - Web Interface</p>
                </header>
                
                <div class="grid">
                    <div class="card">
                        <h2>System Status</h2>
                        <div class="metric">
                            <span>Status</span>
                            <span class="status-badge status-healthy">Healthy</span>
                        </div>
                        <div class="metric">
                            <span>Workflows</span>
                            <span class="metric-value" id="workflows-count">0</span>
                        </div>
                        <div class="metric">
                            <span>Executions</span>
                            <span class="metric-value" id="executions-count">0</span>
                        </div>
                        <button class="button" onclick="refreshStatus()">Refresh</button>
                    </div>
                    
                    <div class="card">
                        <h2>Quick Actions</h2>
                        <p>Manage your workflows and executions</p>
                        <button class="button" onclick="createWorkflow()">Create Workflow</button>
                        <button class="button" onclick="loadWorkflows()">Load Workflows</button>
                    </div>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h2>Workflows</h2>
                        <div class="workflow-list" id="workflows-list">
                            <p>No workflows yet</p>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>Recent Executions</h2>
                        <div class="execution-list" id="executions-list">
                            <p>No executions yet</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                async function refreshStatus() {
                    try {
                        const response = await fetch('/api/health');
                        const data = await response.json();
                        document.getElementById('workflows-count').textContent = data.workflows_count;
                        document.getElementById('executions-count').textContent = data.executions_count;
                    } catch (error) {
                        console.error('Error:', error);
                    }
                }
                
                async function loadWorkflows() {
                    try {
                        const response = await fetch('/api/workflows');
                        const data = await response.json();
                        const list = document.getElementById('workflows-list');
                        
                        if (data.workflows.length === 0) {
                            list.innerHTML = '<p>No workflows yet</p>';
                            return;
                        }
                        
                        list.innerHTML = data.workflows.map(w => `
                            <div class="item">
                                <div class="item-title">${w.name}</div>
                                <div class="item-meta">${w.description || 'No description'}</div>
                                <div class="item-meta">Status: ${w.status}</div>
                            </div>
                        `).join('');
                    } catch (error) {
                        console.error('Error:', error);
                    }
                }
                
                async function createWorkflow() {
                    const name = prompt('Enter workflow name:');
                    if (!name) return;
                    
                    try {
                        const response = await fetch('/api/workflows', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                name: name,
                                description: 'New workflow',
                                nodes: [],
                                connections: []
                            })
                        });
                        
                        if (response.status === 201) {
                            alert('Workflow created successfully!');
                            loadWorkflows();
                            refreshStatus();
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Failed to create workflow');
                    }
                }
                
                // Load data on page load
                window.addEventListener('load', () => {
                    refreshStatus();
                    loadWorkflows();
                });
            </script>
        </body>
        </html>
        """

    def run(self):
        """Start the web server"""
        if not FLASK_AVAILABLE:
            print("Flask not installed. Install with: pip install flask flask-cors")
            return

        print(f"Starting ByteClaude Web UI on http://{self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=self.debug)


def create_web_ui(host: str = "localhost", port: int = 5000) -> WebUIServer:
    """Create and return a web UI server instance"""
    return WebUIServer(host, port)
