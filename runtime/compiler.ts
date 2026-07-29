/**
 * AVENIQ AI — Workflow Compiler & Topological DAG Validation Engine
 */

import { WorkflowDefinition, WorkflowNodeDefinition } from './definition';

export interface ValidationError {
  code: string;
  message: string;
  nodeId?: string;
}

export interface CompiledWorkflowPlan {
  definition: WorkflowDefinition;
  executionBatches: WorkflowNodeDefinition[][]; // Topological parallel execution stages
  topologicalOrder: string[];
}

export class WorkflowCompiler {
  public static compile(def: WorkflowDefinition): CompiledWorkflowPlan {
    const errors = this.validate(def);
    if (errors.length > 0) {
      const errorMsgs = errors.map((e) => `[${e.code}] ${e.message}`).join('; ');
      throw new Error(`Workflow compilation failed: ${errorMsgs}`);
    }

    const nodeMap = new Map<string, WorkflowNodeDefinition>();
    def.nodes.forEach((n) => nodeMap.set(n.id, n));

    // Calculate in-degree for topological batch sorting (Kahn's Algorithm)
    const inDegree = new Map<string, number>();
    const dependentsMap = new Map<string, string[]>();

    def.nodes.forEach((n) => {
      inDegree.set(n.id, (n.dependsOn || []).length);
      dependentsMap.set(n.id, []);
    });

    def.nodes.forEach((n) => {
      (n.dependsOn || []).forEach((dep) => {
        if (!dependentsMap.has(dep)) dependentsMap.set(dep, []);
        dependentsMap.get(dep)!.push(n.id);
      });
    });

    const executionBatches: WorkflowNodeDefinition[][] = [];
    const topologicalOrder: string[] = [];

    let currentLevel = def.nodes.filter((n) => (inDegree.get(n.id) || 0) === 0);

    while (currentLevel.length > 0) {
      executionBatches.push(currentLevel);
      const nextLevel: WorkflowNodeDefinition[] = [];

      for (const node of currentLevel) {
        topologicalOrder.push(node.id);
        const dependents = dependentsMap.get(node.id) || [];
        for (const depId of dependents) {
          const newDegree = (inDegree.get(depId) || 1) - 1;
          inDegree.set(depId, newDegree);
          if (newDegree === 0) {
            nextLevel.push(nodeMap.get(depId)!);
          }
        }
      }
      currentLevel = nextLevel;
    }

    return {
      definition: def,
      executionBatches,
      topologicalOrder,
    };
  }

  public static validate(def: WorkflowDefinition): ValidationError[] {
    const errors: ValidationError[] = [];
    const nodeIds = new Set<string>();

    if (!def.id) errors.push({ code: 'MISSING_WORKFLOW_ID', message: 'Workflow definition must have an id' });
    if (!def.nodes || def.nodes.length === 0) {
      errors.push({ code: 'EMPTY_WORKFLOW', message: 'Workflow must contain at least one node' });
      return errors;
    }

    // 1. Check duplicate IDs & empty prompts
    def.nodes.forEach((n) => {
      if (!n.id) errors.push({ code: 'MISSING_NODE_ID', message: 'Workflow node missing id' });
      if (nodeIds.has(n.id)) {
        errors.push({ code: 'DUPLICATE_NODE_ID', message: `Duplicate node ID '${n.id}'`, nodeId: n.id });
      }
      nodeIds.add(n.id);

      if (!n.prompt || !n.prompt.trim()) {
        errors.push({ code: 'EMPTY_PROMPT', message: `Node '${n.id}' has empty prompt`, nodeId: n.id });
      }
    });

    // 2. Check missing dependencies
    def.nodes.forEach((n) => {
      (n.dependsOn || []).forEach((dep) => {
        if (!nodeIds.has(dep)) {
          errors.push({
            code: 'MISSING_DEPENDENCY',
            message: `Node '${n.id}' depends on missing node '${dep}'`,
            nodeId: n.id,
          });
        }
      });
    });

    // 3. Cycle Detection (DFS)
    const visited = new Set<string>();
    const recStack = new Set<string>();

    const dfs = (nodeId: string, path: string[]) => {
      visited.add(nodeId);
      recStack.add(nodeId);

      const node = def.nodes.find((n) => n.id === nodeId);
      if (node) {
        for (const dep of node.dependsOn || []) {
          if (!visited.has(dep)) {
            dfs(dep, [...path, dep]);
          } else if (recStack.has(dep)) {
            errors.push({
              code: 'CIRCULAR_DEPENDENCY',
              message: `Circular dependency detected: ${[...path, dep].join(' -> ')}`,
              nodeId,
            });
          }
        }
      }
      recStack.delete(nodeId);
    };

    def.nodes.forEach((n) => {
      if (!visited.has(n.id)) {
        dfs(n.id, [n.id]);
      }
    });

    return errors;
  }
}
