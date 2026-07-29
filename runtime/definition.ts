/**
 * AVENIQ AI — Declarative Workflow Definition Language Specification
 */

export interface WorkflowNodeDefinition {
  id: string;
  name?: string;
  provider?: string; // 'hermes' | 'gemini' | 'claude' | 'deepseek' | 'groq'
  model?: string;
  dependsOn?: string[];
  prompt: string;
  condition?: string; // e.g. "{{ research.output.length }} > 0"
  retries?: number;
  timeoutMs?: number;
  inputVariables?: Record<string, any>;
}

export interface WorkflowDefinition {
  id: string;
  name: string;
  description?: string;
  version?: string;
  variables?: Record<string, any>;
  nodes: WorkflowNodeDefinition[];
}
