/**
 * AVENIQ AI — Unified Provider Event Taxonomy & Event Translation Pipeline
 * Normalizes vendor-specific event frames (Hermes JSON-RPC, OpenAI SSE, Anthropic SSE)
 * into standardized AVENIQ execution events for workflow telemetry.
 */

export type AveniqEventType =
  | 'NodeStarted'
  | 'Thinking'
  | 'Token'
  | 'ToolCall'
  | 'ToolResult'
  | 'Progress'
  | 'Completed'
  | 'Failed'
  | 'Cancelled';

export interface AveniqEvent {
  type: AveniqEventType;
  executionId: string;
  workflowId?: string;
  nodeId?: string;
  provider: string;
  model?: string;
  timestamp: string;
  content?: string;
  metadata?: Record<string, any>;
  error?: {
    code: string;
    message: string;
    retryable: boolean;
  };
}

export interface HermesRawEventPayload {
  text?: string;
  delta?: string;
  status?: string;
  tool_id?: string;
  name?: string;
  arguments?: any;
  result?: any;
  error?: any;
  session_id?: string;
  token_stats?: {
    input_tokens?: number;
    output_tokens?: number;
    total_tokens?: number;
  };
  [key: string]: any;
}

/**
 * Event Mapper: Converts raw Hermes events into unified AVENIQ event model
 */
export class HermesEventTranslator {
  public static translate(
    rawType: string,
    rawPayload: HermesRawEventPayload,
    context: { executionId: string; workflowId?: string; nodeId?: string; model?: string }
  ): AveniqEvent | null {
    const timestamp = new Date().toISOString();
    const common = {
      executionId: context.executionId,
      workflowId: context.workflowId,
      nodeId: context.nodeId,
      provider: 'hermes',
      model: context.model || rawPayload.model || 'hermes-agent',
      timestamp,
    };

    switch (rawType) {
      case 'message.start':
        return {
          ...common,
          type: 'NodeStarted',
          content: 'Hermes execution node started',
        };

      case 'thinking.delta':
      case 'reasoning.delta':
        const thinkText = rawPayload.text || rawPayload.delta || '';
        if (!thinkText) return null;
        return {
          ...common,
          type: 'Thinking',
          content: thinkText,
        };

      case 'message.delta':
        const tokenText = rawPayload.text || rawPayload.delta || '';
        if (!tokenText) return null;
        return {
          ...common,
          type: 'Token',
          content: tokenText,
        };

      case 'tool.start':
        return {
          ...common,
          type: 'ToolCall',
          content: rawPayload.name || 'tool',
          metadata: {
            toolId: rawPayload.tool_id,
            arguments: rawPayload.arguments || {},
          },
        };

      case 'tool.complete':
        return {
          ...common,
          type: 'ToolResult',
          content: typeof rawPayload.result === 'string' ? rawPayload.result : JSON.stringify(rawPayload.result || {}),
          metadata: {
            toolId: rawPayload.tool_id,
            name: rawPayload.name,
            result: rawPayload.result,
            error: rawPayload.error,
          },
        };

      case 'status.update':
        return {
          ...common,
          type: 'Progress',
          content: rawPayload.text || rawPayload.status || '',
          metadata: rawPayload,
        };

      case 'message.complete':
        if (rawPayload.status === 'error' || rawPayload.error) {
          return {
            ...common,
            type: 'Failed',
            content: rawPayload.text || 'Hermes execution turn failed',
            error: {
              code: 'HERMES_TURN_ERROR',
              message: rawPayload.error || rawPayload.text || 'Hermes execution error',
              retryable: true,
            },
          };
        }
        return {
          ...common,
          type: 'Completed',
          content: rawPayload.text || '',
          metadata: {
            tokenStats: rawPayload.token_stats,
            usage: rawPayload.usage,
          },
        };

      case 'error':
        return {
          ...common,
          type: 'Failed',
          content: rawPayload.message || rawPayload.error || 'Hermes stream error',
          error: {
            code: rawPayload.code || 'HERMES_STREAM_ERROR',
            message: rawPayload.message || rawPayload.error || 'Stream error',
            retryable: true,
          },
        };

      default:
        return null;
    }
  }
}
