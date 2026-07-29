/**
 * AVENIQ AI — Multi-Tenant Organization & RBAC Engine
 */

import { Organization, OrganizationMember, SubscriptionPlan, UserRole } from './types';

export class OrganizationEngine {
  private orgs: Map<string, Organization> = new Map();

  public createOrganization(name: string, ownerId: string, plan: SubscriptionPlan = 'Free'): Organization {
    const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    const orgId = `org_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    const member: OrganizationMember = {
      userId: ownerId,
      role: 'Owner',
      joinedAt: new Date().toISOString(),
    };

    const org: Organization = {
      id: orgId,
      name,
      slug,
      ownerId,
      plan,
      members: [member],
      createdAt: new Date().toISOString(),
    };

    this.orgs.set(orgId, org);
    return org;
  }

  public addMember(orgId: string, userId: string, role: UserRole): Organization {
    const org = this.orgs.get(orgId);
    if (!org) throw new Error(`Organization '${orgId}' not found.`);

    if (org.members.some((m) => m.userId === userId)) {
      throw new Error(`User '${userId}' is already a member of organization.`);
    }

    org.members.push({
      userId,
      role,
      joinedAt: new Date().toISOString(),
    });

    return org;
  }

  public getMemberRole(orgId: string, userId: string): UserRole | undefined {
    const org = this.orgs.get(orgId);
    if (!org) return undefined;
    const member = org.members.find((m) => m.userId === userId);
    return member?.role;
  }

  public hasPermission(orgId: string, userId: string, requiredRole: UserRole): boolean {
    const role = this.getMemberRole(orgId, userId);
    if (!role) return false;

    const roleHierarchy: Record<UserRole, number> = {
      Owner: 4,
      Admin: 3,
      Developer: 2,
      Viewer: 1,
    };

    return roleHierarchy[role] >= roleHierarchy[requiredRole];
  }

  public getOrganization(orgId: string): Organization | undefined {
    return this.orgs.get(orgId);
  }
}
