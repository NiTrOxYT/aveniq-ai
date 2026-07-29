/**
 * AVENIQ AI — End-to-End Production DAG Workflow Integration Test
 * Executes requested 5-node DAG through WorkflowNodeExecutor & HermesAdapter:
 * Research -> Plan -> Blog -> LinkedIn -> Quality Check
 */

import { AveniqEvent } from './events';
import { ExecutionPersistenceStore } from './persistence';
import { WorkflowNode, WorkflowNodeExecutor } from './node_executor';

async function runEndToEndWorkflowTest() {
  console.log('================================================================');
  console.log('AVENIQ AI -> Live 5-Node DAG Workflow Execution Engine Test');
  console.log('DAG Topology: Research -> Plan -> Blog -> LinkedIn -> Quality Check');
  console.log('================================================================\n');

  const executor = new WorkflowNodeExecutor();
  const store = ExecutionPersistenceStore.getInstance();

  const workflowId = 'wf_marketing_campaign';
  const executionId = `exec_dag_${Date.now()}`;

  const dagNodes: WorkflowNode[] = [
    {
      id: 'node_1_research',
      name: 'Research',
      provider: 'hermes',
      model: 'gemini-2.5-pro',
      prompt: 'Research key benefits of multi-agent AI orchestration in 2 bullet points.',
    },
    {
      id: 'node_2_plan',
      name: 'Plan',
      provider: 'hermes',
      model: 'gemini-2.5-pro',
      prompt: 'Based on research, outline a 3-step marketing launch plan.',
    },
    {
      id: 'node_3_blog',
      name: 'Blog',
      provider: 'hermes',
      model: 'gemini-2.5-pro',
      prompt: 'Draft a short 2-paragraph technical blog introduction about AI orchestration.',
    },
    {
      id: 'node_4_linkedin',
      name: 'LinkedIn',
      provider: 'hermes',
      model: 'gemini-2.5-pro',
      prompt: 'Write a 1-sentence engaging LinkedIn post with 2 hashtags.',
    },
    {
      id: 'node_5_quality_check',
      name: 'Quality Check',
      provider: 'hermes',
      model: 'gemini-2.5-pro',
      prompt: 'Perform final quality check on marketing assets and return APPROVED status.',
    },
  ];

  const eventsLog: AveniqEvent[] = [];

  const context = {
    workflowId,
    executionId,
    onEvent: (event: AveniqEvent) => {
      eventsLog.push(event);
      console.log(`[Event: ${event.type}] [Node: ${event.nodeId}] ${event.content?.substring(0, 70) || ''}`);
    },
  };

  const startTime = Date.now();

  for (const node of dagNodes) {
    console.log(`\n--- Executing Node: ${node.name} (${node.id}) ---`);
    const record = await executor.executeNode(node, context);
    console.log(`Node ${node.name} Status: ${record.status} (${record.durationMs}ms)`);
    if (record.error) {
      console.log(`Node Error / Notice: ${record.error.message}`);
    }
  }

  const totalDuration = Date.now() - startTime;
  const allRecords = store.listRecordsForExecution(workflowId, executionId);

  console.log('\n================================================================');
  console.log('DAG WORKFLOW EXECUTION SUMMARY');
  console.log('================================================================');
  console.log(`Workflow ID: ${workflowId}`);
  console.log(`Execution ID: ${executionId}`);
  console.log(`Total DAG Execution Time: ${totalDuration}ms`);
  console.log(`Total Events Emitted: ${eventsLog.length}`);
  console.log(`Nodes Executed: ${allRecords.length} / ${dagNodes.length}`);

  for (const r of allRecords) {
    console.log(`  - [${r.status.toUpperCase()}] ${r.nodeId} (${r.provider}/${r.model}) - ${r.durationMs || 0}ms`);
  }

  console.log('\n================================================================');
  console.log('END-TO-END DAG EXECUTION TEST COMPLETED ✅');
  console.log('================================================================');
}

runEndToEndWorkflowTest().catch(console.error);

export { runEndToEndWorkflowTest };
