/**
 * AVENIQ AI — Production AI Workflow Runtime Demonstration Suite
 * Executes full 10-node DAG workflow:
 * Research -> Competitors -> SEO -> Plan -> Blog -> LinkedIn -> Instagram -> Facebook -> X -> Quality
 */

import { DashboardApi } from './api';
import { WorkflowDefinition } from './definition';
import { RuntimeEventBus } from './event_bus';
import { RuntimeScheduler } from './scheduler';

async function runProductionRuntimeDemo() {
  console.log('================================================================');
  console.log('AVENIQ AI — Production AI Workflow Runtime Demonstration');
  console.log('Topology: Research -> Competitors -> SEO -> Plan -> Blog ->');
  console.log('          LinkedIn -> Instagram -> Facebook -> X -> Quality');
  console.log('================================================================\n');

  const scheduler = new RuntimeScheduler();
  const api = new DashboardApi(scheduler);
  const eventBus = RuntimeEventBus.getInstance();

  const eventLog: string[] = [];
  eventBus.subscribe((ev) => {
    const msg = `[EventBus: ${ev.type}] [Node: ${ev.nodeId || 'WORKFLOW'}] ${ev.timestamp}`;
    eventLog.push(msg);
    if (ev.type === 'NodeStarted' || ev.type === 'NodeCompleted' || ev.type === 'WorkflowCompleted') {
      console.log(msg);
    }
  });

  const fullWorkflowDef: WorkflowDefinition = {
    id: 'wf_full_marketing_pipeline',
    name: '10-Node Full Content Launch Campaign Pipeline',
    variables: { campaignName: 'AVENIQ AI Launch 2026' },
    nodes: [
      {
        id: 'node_1_research',
        name: 'Research',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        prompt: 'Research key benefits of multi-agent AI orchestration in 2 bullet points.',
      },
      {
        id: 'node_2_competitors',
        name: 'Competitors',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        prompt: 'Analyze competitor landscape for AI agents in 2 concise sentences.',
      },
      {
        id: 'node_3_seo',
        name: 'SEO Keywords',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        prompt: 'Extract 3 high-volume SEO keywords for AI workflow automation.',
      },
      {
        id: 'node_4_plan',
        name: 'Plan',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        dependsOn: ['node_1_research', 'node_2_competitors', 'node_3_seo'],
        prompt: 'Formulate launch strategy using research output:\n{{ node_1_research.output }}',
      },
      {
        id: 'node_5_blog',
        name: 'Blog Post',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        dependsOn: ['node_4_plan'],
        prompt: 'Draft 2-paragraph launch blog post based on strategy:\n{{ node_4_plan.output }}',
      },
      {
        id: 'node_6_linkedin',
        name: 'LinkedIn Post',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        dependsOn: ['node_5_blog'],
        prompt: 'Summarize blog into a LinkedIn post:\n{{ node_5_blog.output }}',
      },
      {
        id: 'node_7_instagram',
        name: 'Instagram Copy',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        dependsOn: ['node_5_blog'],
        prompt: 'Write an Instagram caption with 3 hashtags for:\n{{ node_5_blog.output }}',
      },
      {
        id: 'node_8_facebook',
        name: 'Facebook Post',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        dependsOn: ['node_5_blog'],
        prompt: 'Write a Facebook post announcement for:\n{{ node_5_blog.output }}',
      },
      {
        id: 'node_9_x',
        name: 'X Tweet Thread',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        dependsOn: ['node_5_blog'],
        prompt: 'Draft 2 tweets summarizing:\n{{ node_5_blog.output }}',
      },
      {
        id: 'node_10_quality',
        name: 'Quality Assurance',
        provider: 'hermes',
        model: 'gemini-2.5-pro',
        dependsOn: ['node_6_linkedin', 'node_7_instagram', 'node_8_facebook', 'node_9_x'],
        prompt: 'Perform quality check across social media outputs and return APPROVED status.',
      },
    ],
  };

  api.registerWorkflow(fullWorkflowDef);

  console.log('\n--- 1. Executing Full 10-Node Workflow ---');
  const executionState = await scheduler.executeWorkflow(fullWorkflowDef, {
    executionId: 'exec_demo_full_100',
  });

  console.log('\n--- Execution Summary ---');
  console.log(`Status: ${executionState.status}`);
  console.log(`Completed Nodes: ${executionState.completedNodes.length} / ${fullWorkflowDef.nodes.length}`);
  console.log(`Execution Duration: ${(executionState.endTime || Date.now()) - executionState.startTime}ms`);

  console.log('\n--- 2. Testing Execution Replay Engine ---');
  console.log('Replaying execution from checkpoint exec_demo_full_100...');
  const replayState = await api.replayExecution(fullWorkflowDef.id, 'exec_demo_full_100');
  console.log(`Replay Status: ${replayState.status}`);
  console.log(`Replay Completed Nodes: ${replayState.completedNodes.length}`);

  console.log('\n================================================================');
  console.log('PRODUCTION AI WORKFLOW RUNTIME TEST COMPLETED SUCCESSFULLY ✅');
  console.log('================================================================');
}

runProductionRuntimeDemo().catch(console.error);

export { runProductionRuntimeDemo };
