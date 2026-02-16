#!/usr/bin/env python3
"""
Simple HTTP API for Bag Module (no FastAPI/uvicorn required)
Uses Python's built-in http.server
"""
import json
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.bag.service import BagModule

bag = BagModule()

# User mapping (for testing)
USER_MAP = {
    "fazaasro@gmail.com": "faza",
    "gabriela.servitya@gmail.com": "gaby"
}

class BagHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def get_user(self, headers):
        """Get user from headers (simulating Cloudflare Access)"""
        email = headers.get('CF-Access-Authenticated-User-Email')
        if not email:
            email = headers.get('X-Test-User')
        return USER_MAP.get(email)
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        user_id = self.get_user(self.headers)
        if not user_id:
            self.send_json({'error': 'Not authenticated'}, 401)
            return
        
        # Health check
        if path == '/health':
            self.send_json({'status': 'ok', 'module': 'bag'})
            return
        
        # Get transactions
        if path == '/api/v1/bag/transactions':
            category = query.get('category', [None])[0]
            limit = int(query.get('limit', [50])[0])
            transactions = bag.get_transactions(user_id, category=category, limit=limit)
            self.send_json({'transactions': transactions})
            return
        
        # Get runway
        if path == '/api/v1/bag/runway':
            balance = query.get('balance', [None])[0]
            if balance:
                balance = float(balance)
            result = bag.calculate_runway(user_id, balance)
            self.send_json(result)
            return
        
        # Detect subscriptions
        if path == '/api/v1/bag/subscriptions/detect':
            patterns = bag.detect_subscriptions(user_id)
            self.send_json({'patterns': patterns})
            return
        
        # Get budget status
        if path.startswith('/api/v1/bag/budgets/'):
            budget_id = path.split('/')[-1]
            if '/status' in path:
                result = bag.get_budget_status(budget_id)
                self.send_json(result)
                return
        
        self.send_json({'error': 'Not found'}, 404)
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        user_id = self.get_user(self.headers)
        if not user_id:
            self.send_json({'error': 'Not authenticated'}, 401)
            return
        
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON'}, 400)
            return
        
        # Create transaction
        if path == '/api/v1/bag/transactions':
            result = bag.create_transaction(data, user_id)
            self.send_json(result, 201)
            return
        
        # Update split
        if '/split' in path:
            parts = path.split('/')
            if len(parts) >= 5:
                txn_id = parts[-2]
                result = bag.update_split(
                    txn_id,
                    data.get('split_type', 'solo'),
                    user_id,
                    data.get('faza_portion'),
                    data.get('gaby_portion')
                )
                self.send_json(result)
                return
        
        # Create subscription
        if path == '/api/v1/bag/subscriptions':
            result = bag.add_subscription(data, user_id)
            self.send_json(result, 201)
            return
        
        # Create budget
        if path == '/api/v1/bag/budgets':
            result = bag.create_budget(data, user_id)
            self.send_json(result, 201)
            return
        
        self.send_json({'error': 'Not found'}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

def run_server(port=8000):
    server = HTTPServer(('127.0.0.1', port), BagHandler)
    print(f"🚀 Bag API server running on http://127.0.0.1:{port}")
    print(f"   - Health:    GET  /health")
    print(f"   - Transactions: GET/POST /api/v1/bag/transactions")
    print(f"   - Runway:    GET  /api/v1/bag/runway")
    print(f"   - Budgets:   GET/POST /api/v1/bag/budgets")
    print("")
    print("Test with:")
    print(f'  curl -H "X-Test-User: fazaasro@gmail.com" http://localhost:{port}/api/v1/bag/transactions')
    print("")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
