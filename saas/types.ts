/**
 * AVENIQ AI — Multi-Tenant SaaS Platform Core Types
 */

export type UserRole = 'Owner' | 'Admin' | 'Developer' | 'Viewer';

export type SubscriptionPlan = 'Free' | 'Pro' | 'Team' | 'Enterprise';

export interface User {
  id: string;
  email: string;
  name: string;
  passwordHash?: string;
  emailVerified: boolean;
  avatarUrl?: string;
  createdAt: string;
}

export interface OrganizationMember {
  userId: string;
  role: UserRole;
  joinedAt: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  ownerId: string;
  plan: SubscriptionPlan;
  members: OrganizationMember[];
  createdAt: string;
}

export interface Project {
  id: string;
  orgId: string;
  name: string;
  slug: string;
  description?: string;
  createdAt: string;
}

export interface EncryptedSecret {
  id: string;
  orgId: string;
  projectId?: string;
  name: string; // e.g. "GEMINI_API_KEY"
  encryptedValue: string; // Base64 AES-256-GCM payload
  iv: string;
  tag: string;
  version: number;
  updatedAt: string;
}

export interface ApiKey {
  id: string;
  orgId: string;
  projectId?: string;
  keyHash: string;
  keyPrefix: string; // "aq_live_..."
  name: string;
  scopes: string[];
  expiresAt?: string;
  lastUsedAt?: string;
  createdAt: string;
}

export interface UsageMeteringRecord {
  orgId: string;
  period: string; // "2026-07"
  workflowExecutions: number;
  totalTokens: number;
  activeUsers: number;
  storageBytes: number;
  planLimits: {
    maxExecutions: number;
    maxTokens: number;
    maxUsers: number;
  };
}

export interface NotificationPayload {
  id: string;
  orgId: string;
  channel: 'email' | 'webhook' | 'telegram';
  event: 'WorkflowCompleted' | 'WorkflowFailed' | 'LongRunning' | 'ReplayFinished';
  recipient: string;
  data: Record<string, any>;
  sentAt: string;
  status: 'sent' | 'failed';
}
