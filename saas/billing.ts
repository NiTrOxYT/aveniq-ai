/**
 * AVENIQ AI — SaaS Usage Metering & Billing Plan Engine
 */

import { SubscriptionPlan, UsageMeteringRecord } from './types';

export class BillingMeteringEngine {
  private records: Map<string, UsageMeteringRecord> = new Map(); // orgId:period -> UsageMeteringRecord

  private planLimits: Record<SubscriptionPlan, { maxExecutions: number; maxTokens: number; maxUsers: number }> = {
    Free: { maxExecutions: 100, maxTokens: 100000, maxUsers: 3 },
    Pro: { maxExecutions: 5000, maxTokens: 10000000, maxUsers: 10 },
    Team: { maxExecutions: 25000, maxTokens: 50000000, maxUsers: 50 },
    Enterprise: { maxExecutions: 1000000, maxTokens: 1000000000, maxUsers: 1000 },
  };

  public recordUsage(orgId: string, plan: SubscriptionPlan, tokens: number = 0, isExecution: boolean = true): UsageMeteringRecord {
    const period = new Date().toISOString().substring(0, 7); // "YYYY-MM"
    const key = `${orgId}:${period}`;

    let record = this.records.get(key);
    if (!record) {
      record = {
        orgId,
        period,
        workflowExecutions: 0,
        totalTokens: 0,
        activeUsers: 1,
        storageBytes: 1024 * 1024,
        planLimits: this.planLimits[plan],
      };
      this.records.set(key, record);
    }

    if (isExecution) {
      if (record.workflowExecutions >= record.planLimits.maxExecutions) {
        throw new Error(`Plan limit reached: Organization has exceeded monthly workflow execution quota (${record.planLimits.maxExecutions} runs). Upgrade plan to continue.`);
      }
      record.workflowExecutions += 1;
    }

    record.totalTokens += tokens;
    return record;
  }

  public getUsage(orgId: string): UsageMeteringRecord | undefined {
    const period = new Date().toISOString().substring(0, 7);
    return this.records.get(`${orgId}:${period}`);
  }
}
