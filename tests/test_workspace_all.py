"""
Comprehensive Multi-Tenant Workspace Test Suite for AVENIQ Workspace Platform.
Tests TenantContext, OrganizationManager, WorkspaceManager, ProvisioningService, RBAC, BrandProfile, Credentials, and Quotas.
"""

import unittest
from workspace.context.tenant_context import TenantContext
from workspace.organization.organization import OrganizationManager
from workspace.workspace.workspace_manager import WorkspaceManager
from workspace.provisioning.service import ProvisioningService, TemplateLibrary
from workspace.users.permissions import User, Role, RBACEvaluator
from workspace.branding.brand_profile import BrandProfile, WorkspaceCredentialsManager
from workspace.quotas.quota_manager import WorkspaceQuotaManager, WorkspaceExporterImporter

class TestWorkspacePlatform(unittest.TestCase):
    def test_tenant_context(self):
        ctx = TenantContext(organization_id="org_001", workspace_id="ws_001")
        self.assertTrue(ctx.is_valid())

    def test_organization_and_workspace_managers(self):
        org_mgr = OrganizationManager()
        ws_mgr = WorkspaceManager()

        org = org_mgr.create_organization("Acme Corp")
        self.assertIsNotNone(org.organization_id)

        ws = ws_mgr.create_workspace(org.organization_id, "Marketing", "SaaS Startup")
        self.assertEqual(ws.organization_id, org.organization_id)
        self.assertEqual(ws.template, "SaaS Startup")

    def test_provisioning_and_templates(self):
        ctx = TenantContext("org_001", "ws_001")
        res = ProvisioningService.provision_workspace(ctx, "Digital Agency")
        self.assertEqual(res["status"], "Provisioned")
        self.assertIn("Company Brain", res["components_initialized"])

        tpl = TemplateLibrary.get_template("Digital Agency")
        self.assertEqual(tpl["primary_color"], "#EC4899")

    def test_rbac_permissions(self):
        admin = User(user_id="u1", email="a@a.com", name="Alice", role=Role.ADMIN)
        viewer = User(user_id="u2", email="v@v.com", name="Vince", role=Role.VIEWER)

        self.assertTrue(RBACEvaluator.has_permission(admin, "manage_workspaces"))
        self.assertFalse(RBACEvaluator.has_permission(viewer, "manage_workspaces"))
        self.assertTrue(RBACEvaluator.has_permission(viewer, "view_analytics"))

    def test_credentials_isolation(self):
        cred_mgr = WorkspaceCredentialsManager()
        cred_mgr.set_api_key("ws_001", "openai", "sk-ws1-key")
        cred_mgr.set_api_key("ws_002", "openai", "sk-ws2-key")

        self.assertEqual(cred_mgr.get_api_key("ws_001", "openai"), "sk-ws1-key")
        self.assertEqual(cred_mgr.get_api_key("ws_002", "openai"), "sk-ws2-key")

    def test_export_import(self):
        brand = BrandProfile(workspace_id="ws_001", brand_name="Stark AI")
        json_str = WorkspaceExporterImporter.export_workspace("ws_001", brand)
        imp = WorkspaceExporterImporter.import_workspace(json_str)
        self.assertEqual(imp["status"], "Imported")
        self.assertEqual(imp["workspace_id"], "ws_001")

if __name__ == "__main__":
    unittest.main()
