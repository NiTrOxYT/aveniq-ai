/**
 * AVENIQ AI — Background Queue Worker & Dead-Letter Queue (DLQ) Engine
 */

export interface QueueJob {
  id: string;
  orgId: string;
  projectId?: string;
  workflowId: string;
  payload: Record<string, any>;
  attempts: number;
  maxRetries: number;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'dlq';
  enqueuedAt: string;
  startedAt?: string;
  completedAt?: string;
  error?: string;
}

export class BackgroundQueueWorker {
  private queue: QueueJob[] = [];
  private dlq: QueueJob[] = [];
  private activeJobs: Map<string, QueueJob> = new Map();
  private maxConcurrency: number = 10;

  public enqueue(orgId: string, workflowId: string, payload: Record<string, any>, projectId?: string): QueueJob {
    const job: QueueJob = {
      id: `job_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      orgId,
      projectId,
      workflowId,
      payload,
      attempts: 0,
      maxRetries: 3,
      status: 'queued',
      enqueuedAt: new Date().toISOString(),
    };

    this.queue.push(job);
    return job;
  }

  public async processNext(handler: (job: QueueJob) => Promise<void>): Promise<QueueJob | null> {
    if (this.queue.length === 0 || this.activeJobs.size >= this.maxConcurrency) {
      return null;
    }

    const job = this.queue.shift()!;
    job.status = 'processing';
    job.attempts += 1;
    job.startedAt = new Date().toISOString();
    this.activeJobs.set(job.id, job);

    try {
      await handler(job);
      job.status = 'completed';
      job.completedAt = new Date().toISOString();
    } catch (err: any) {
      job.error = err.message || 'Job processing error';
      if (job.attempts < job.maxRetries) {
        job.status = 'queued';
        this.queue.push(job); // Re-queue for retry
      } else {
        job.status = 'dlq';
        this.dlq.push(job); // Route to Dead-Letter Queue (DLQ)
      }
    } finally {
      this.activeJobs.delete(job.id);
    }

    return job;
  }

  public getStats(): { queued: number; active: number; dlq: number } {
    return {
      queued: this.queue.length,
      active: this.activeJobs.size,
      dlq: this.dlq.length,
    };
  }

  public getDlqJobs(): QueueJob[] {
    return [...this.dlq];
  }
}
