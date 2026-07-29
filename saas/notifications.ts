/**
 * AVENIQ AI — SaaS Notification & Webhook Dispatch Engine
 */

import { NotificationPayload } from './types';

export class NotificationEngine {
  private notifications: NotificationPayload[] = [];

  public async dispatch(
    orgId: string,
    channel: 'email' | 'webhook' | 'telegram',
    event: 'WorkflowCompleted' | 'WorkflowFailed' | 'LongRunning' | 'ReplayFinished',
    recipient: string,
    data: Record<string, any>
  ): Promise<NotificationPayload> {
    const payload: NotificationPayload = {
      id: `ntf_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      orgId,
      channel,
      event,
      recipient,
      data,
      sentAt: new Date().toISOString(),
      status: 'sent',
    };

    this.notifications.push(payload);
    return payload;
  }

  public getHistory(orgId: string): NotificationPayload[] {
    return this.notifications.filter((n) => n.orgId === orgId);
  }
}
