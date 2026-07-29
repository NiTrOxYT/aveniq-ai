/**
 * AVENIQ AI — Multi-Tenant Project Isolation Engine
 */

import { Project } from './types';

export class ProjectEngine {
  private projects: Map<string, Project> = new Map();

  public createProject(orgId: string, name: string, description?: string): Project {
    const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    const projectId = `proj_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    const project: Project = {
      id: projectId,
      orgId,
      name,
      slug,
      description,
      createdAt: new Date().toISOString(),
    };

    this.projects.set(projectId, project);
    return project;
  }

  public getProject(projectId: string): Project | undefined {
    return this.projects.get(projectId);
  }

  public listProjects(orgId: string): Project[] {
    const result: Project[] = [];
    for (const p of this.projects.values()) {
      if (p.orgId === orgId) result.push(p);
    }
    return result;
  }
}
