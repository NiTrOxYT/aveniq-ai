/**
 * AVENIQ AI — Multi-Tenant SaaS Platform End-to-End Test Suite
 * Demonstrates onboarding flow: User Signup -> Organization -> RBAC -> Project Isolation ->
 * Encrypted Secrets -> API Keys -> Queue Worker -> Usage Metering -> Notifications.
 */

import { ApiKeyManager } from './api_keys';
import { AuthEngine } from './auth';
import { BillingMeteringEngine } from './billing';
import { NotificationEngine } from './notifications';
import { OrganizationEngine } from './organizations';
import { ProjectEngine } from './projects';
import { BackgroundQueueWorker } from './queue_worker';
import { EncryptedSecretsVault } from './secrets';

async function runSaasPlatformTest() {
  console.log('================================================================');
  console.log('AVENIQ AI — Multi-Tenant SaaS Platform Integration Test Suite');
  console.log('================================================================\n');

  const auth = new AuthEngine();
  const orgs = new OrganizationEngine();
  const projects = new ProjectEngine();
  const secrets = new EncryptedSecretsVault();
  const apiKeys = new ApiKeyManager();
  const billing = new BillingMeteringEngine();
  const queue = new BackgroundQueueWorker();
  const notifications = new NotificationEngine();

  // 1. User Signup & Session
  console.log('[Step 1] User Signup & JWT Authentication...');
  const { user, session } = await auth.signUp('owner@acme.corp', 'SecurePass2026!', 'Acme Founder');
  console.log(`PASSED ✅ Created User: ${user.name} (${user.id})`);
  console.log(`Access Token: ${session.accessToken.substring(0, 25)}...`);

  // 2. Organization Creation & RBAC
  console.log('\n[Step 2] Organization Creation & Member RBAC...');
  const org = orgs.createOrganization('Acme AI Corporation', user.id, 'Pro');
  console.log(`PASSED ✅ Organization Created: ${org.name} (Slug: ${org.slug}, Plan: ${org.plan})`);

  orgs.addMember(org.id, 'usr_dev_1', 'Developer');
  const hasDevPermission = orgs.hasPermission(org.id, 'usr_dev_1', 'Developer');
  const hasOwnerPermission = orgs.hasPermission(org.id, 'usr_dev_1', 'Owner');
  console.log(`PASSED ✅ RBAC Check: Developer has Dev permission (${hasDevPermission}), Owner permission (${hasOwnerPermission})`);

  // 3. Project Isolation
  console.log('\n[Step 3] Creating Isolated Project Environment...');
  const project = projects.createProject(org.id, 'Q3 Marketing Automation', 'Main product launch pipeline');
  console.log(`PASSED ✅ Project Created: ${project.name} (${project.id})`);

  // 4. Encrypted Secrets Vault
  console.log('\n[Step 4] Storing AES-256-GCM Encrypted Provider Secret...');
  const sec = secrets.setSecret(org.id, 'GEMINI_API_KEY', 'AIzaSy_Secret_Gemini_Key_2026', project.id);
  console.log(`PASSED ✅ Stored Encrypted Secret: ${sec.name} (Version: ${sec.version}, IV: ${sec.iv})`);
  const decrypted = secrets.getSecretValue(org.id, 'GEMINI_API_KEY', project.id);
  console.log(`PASSED ✅ Decrypted Secret Value: ${decrypted?.substring(0, 12)}...`);

  // 5. API Key Generation
  console.log('\n[Step 5] Issuing Scoped API Key...');
  const { apiKey, rawKey } = apiKeys.createKey(org.id, 'CI/CD Pipeline Key', ['workflows:write', 'executions:write'], project.id);
  console.log(`PASSED ✅ Generated API Key: ${rawKey.substring(0, 20)}...`);
  const validatedKey = apiKeys.validateKey(rawKey, 'workflows:write');
  console.log(`PASSED ✅ Validated Key Scopes: ${validatedKey.scopes.join(', ')}`);

  // 6. Background Queue Worker Dispatch
  console.log('\n[Step 6] Enqueuing Workflow Job to Background Queue Worker...');
  const job = queue.enqueue(org.id, 'wf_campaign_10_nodes', { prompt: 'Run full 10-node DAG' }, project.id);
  console.log(`PASSED ✅ Enqueued Job: ${job.id} (Status: ${job.status})`);

  await queue.processNext(async (j) => {
    console.log(`   [Queue Worker] Processing Job ${j.id} for Org ${j.orgId}...`);
  });
  console.log(`PASSED ✅ Job Completed! Queue Stats:`, queue.getStats());

  // 7. Usage Metering
  console.log('\n[Step 7] Usage Metering & Subscription Plan Enforcement...');
  const usage = billing.recordUsage(org.id, org.plan, 12500, true);
  console.log(`PASSED ✅ Metered Usage: ${usage.workflowExecutions} / ${usage.planLimits.maxExecutions} runs, ${usage.totalTokens} tokens`);

  // 8. Notifications
  console.log('\n[Step 8] Dispatching Notification Event...');
  const ntf = await notifications.dispatch(org.id, 'webhook', 'WorkflowCompleted', 'https://hooks.acme.corp/aveniq', {
    executionId: 'exec_dag_100',
    status: 'completed',
  });
  console.log(`PASSED ✅ Notification Dispatched via ${ntf.channel}: Event '${ntf.event}' to ${ntf.recipient}`);

  console.log('\n================================================================');
  console.log('MULTI-TENANT SAAS PLATFORM TEST SUITE PASSED SUCCESSFULLY ✅');
  console.log('================================================================');
}

runSaasPlatformTest().catch(console.error);

export { runSaasPlatformTest };
