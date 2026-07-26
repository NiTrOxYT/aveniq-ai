"""
REST API Router & Lightweight HTTP Server for AVENIQ Multi-Tenant Workspace Platform.
Exposes JSON endpoints for managing organizations, workspaces, user permissions, brand profiles, and quotas.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from workspace.organization.organization import OrganizationManager
from workspace.workspace.workspace_manager import WorkspaceManager
from workspace.users.permissions import User, Role, RBACEvaluator

org_mgr = OrganizationManager()
ws_mgr = WorkspaceManager()

# Default Org and Workspace for testing API
default_org = org_mgr.create_organization("Acme AI Corp", "Technology", "https://acme.ai")
default_ws = ws_mgr.create_workspace(default_org.organization_id, "Marketing", "SaaS Startup")

class WorkspaceAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/workspace" or path == "/workspaces":
            wss = [
                {
                    "workspace_id": w.workspace_id,
                    "organization_id": w.organization_id,
                    "name": w.name,
                    "template": w.template
                } for w in ws_mgr.list_workspaces()
            ]
            self._send_json(200, {"workspaces": wss})
        elif path == "/organization" or path == "/organizations":
            orgs = [
                {
                    "organization_id": o.organization_id,
                    "name": o.name,
                    "industry": o.industry,
                    "website": o.website
                } for o in org_mgr.list_organizations()
            ]
            self._send_json(200, {"organizations": orgs})
        elif path == "/users":
            self._send_json(200, {"users": [
                {"user_id": "usr_001", "name": "Alice Admin", "role": "Admin"},
                {"user_id": "usr_002", "name": "Bob Editor", "role": "Editor"}
            ]})
        elif path == "/workspace/health":
            self._send_json(200, {
                "status": "healthy",
                "platform": "AVENIQ Multi-Tenant Workspace & Organization Platform",
                "version": "1.0.0"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/workspace":
            new_ws = ws_mgr.create_workspace(default_org.organization_id, "Engineering", "Digital Agency")
            self._send_json(200, {
                "status": "Created",
                "workspace_id": new_ws.workspace_id,
                "name": new_ws.name,
                "template": new_ws.template
            })
        elif path == "/organization":
            new_org = org_mgr.create_organization("Stark Industries", "Defense Tech", "https://stark.com")
            self._send_json(200, {
                "status": "Created",
                "organization_id": new_org.organization_id,
                "name": new_org.name
            })
        elif path == "/users":
            self._send_json(200, {"status": "User created", "user_id": "usr_003", "role": "Editor"})
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8095):
    server_address = ("", port)
    httpd = HTTPServer(server_address, WorkspaceAPIHandler)
    print(f"Workspace REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
