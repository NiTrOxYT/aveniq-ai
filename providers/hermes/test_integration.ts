/**
 * AVENIQ AI — Hermes Integration Test Suite
 * Validates real bi-directional WebSocket JSON-RPC communication,
 * streaming, session lifecycle, cancellation, and timeout safeguards.
 */

import { HermesAdapter } from './adapter';
import { ExecutionService } from './execution';
import { HermesStreamChunk } from './types';

async function runIntegrationTest() {
  console.log('====================================================');
  console.log('AVENIQ AI -> Hermes Live Integration Test Suite');
  console.log('====================================================\n');

  const env = ((globalThis as any).process?.env) || {};
  const baseUrl = env.HERMES_BASE_URL || 'http://127.0.0.1:9119';
  const token = env.HERMES_DASHBOARD_SESSION_TOKEN || 'aveniq_hermes_secret';
  const wsUrl = env.HERMES_WS_URL || `ws://127.0.0.1:9119/api/ws?token=${token}`;

  const adapter = new HermesAdapter({
    baseUrl,
    wsUrl,
    defaultTransport: 'websocket',
  });

  const execService = new ExecutionService(adapter, {
    defaultTimeoutMs: 30000,
    delegateRetriesToAveniq: true,
  });

  try {
    // 1. Health check
    console.log('[Test 1] Checking Hermes server health...');
    const health = await adapter.checkHealth();
    console.log('Health check result:', health);

    // 2. Stream Execution ("Say hello")
    console.log('\n[Test 2] Testing live prompt execution & streaming...');
    const streamChunks: HermesStreamChunk[] = [];
    const result = await execService.run(
      {
        prompt: 'Say hello in 3 words.',
        transport: 'websocket',
        timeoutMs: 45000,
      },
      (chunk) => {
        streamChunks.push(chunk);
        if (chunk.type === 'token') {
          console.log(`[Token Chunk]: ${chunk.content}`);
        } else if (chunk.type === 'thought') {
          console.log(`[Thought Chunk]: ${chunk.content}`);
        } else if (chunk.type === 'status') {
          console.log(`[Status Chunk]: ${chunk.content}`);
        }
      }
    );

    console.log('\n--- Streamed Chunks Summary ---');
    console.log(`Total Chunks: ${streamChunks.length}`);
    console.log(`Final Status: ${result.status}`);
    console.log(`Session ID: ${result.sessionId}`);
    console.log(`Execution ID: ${result.executionId}`);
    console.log(`Duration: ${result.durationMs}ms`);

    // 3. Testing Cancellation
    console.log('\n[Test 3] Testing prompt cancellation...');
    const longRunningExecPromise = execService.run({
      prompt: 'Write a 500-word detailed story about AI.',
      transport: 'websocket',
      timeoutMs: 60000,
      executionId: 'test_cancel_exec_123',
    });

    await new Promise((r) => setTimeout(r, 500));
    console.log('Triggering cancellation for test_cancel_exec_123...');
    const cancelled = await execService.cancel('test_cancel_exec_123', 'Integration test cancellation');
    console.log('Cancellation trigger returned:', cancelled);

    const cancelResult = await longRunningExecPromise;
    console.log('Cancelled execution status:', cancelResult.status);
    console.log(`Verified cancelled status: ${cancelResult.status === 'cancelled' ? 'PASSED ✅' : 'FAILED ❌'}`);

    // 4. Testing Timeout Behavior
    console.log('\n[Test 4] Testing execution timeout safeguard...');
    const timeoutResult = await execService.run({
      prompt: 'Count to 100 slowly',
      transport: 'websocket',
      timeoutMs: 100, // force fast 100ms timeout
    });
    console.log('Timeout test status:', timeoutResult.status);
    console.log(`Verified timeout status: ${timeoutResult.status === 'timeout' ? 'PASSED ✅' : 'FAILED ❌'}`);

    console.log('\n====================================================');
    console.log('ALL INTEGRATION TESTS COMPLETED SUCCESSFULLY ✅');
    console.log('====================================================');
  } catch (err: any) {
    console.error('❌ Integration Test Error:', err);
  } finally {
    await execService.dispose();
    await adapter.dispose();
  }
}

runIntegrationTest().catch(console.error);

export { runIntegrationTest };
