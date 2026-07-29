/**
 * AVENIQ AI — Multi-Tenant Authentication Engine
 */

import { User } from './types';

export interface SessionToken {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export class AuthEngine {
  private users: Map<string, User> = new Map();
  private userEmails: Map<string, string> = new Map(); // email -> userId
  private refreshTokens: Set<string> = new Set();

  public async signUp(email: string, password: string, name: string): Promise<{ user: User; session: SessionToken }> {
    if (this.userEmails.has(email.toLowerCase())) {
      throw new Error(`User with email '${email}' already exists.`);
    }

    const userId = `usr_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const user: User = {
      id: userId,
      email: email.toLowerCase(),
      name,
      passwordHash: `sha256_${Date.now()}_${password}`,
      emailVerified: false,
      createdAt: new Date().toISOString(),
    };

    this.users.set(userId, user);
    this.userEmails.set(email.toLowerCase(), userId);

    const session = this.createSession(userId);
    return { user, session };
  }

  public async signIn(email: string, password: string): Promise<{ user: User; session: SessionToken }> {
    const userId = this.userEmails.get(email.toLowerCase());
    if (!userId) throw new Error('Invalid email or password.');

    const user = this.users.get(userId)!;
    if (!user.passwordHash) throw new Error('Invalid authentication method.');

    const session = this.createSession(userId);
    return { user, session };
  }

  public async signInOAuth(provider: 'google' | 'github', oauthId: string, email: string, name: string): Promise<{ user: User; session: SessionToken }> {
    let userId = this.userEmails.get(email.toLowerCase());
    let user: User;

    if (!userId) {
      userId = `usr_oauth_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
      user = {
        id: userId,
        email: email.toLowerCase(),
        name,
        emailVerified: true,
        avatarUrl: `https://avatars.example.com/${provider}/${oauthId}`,
        createdAt: new Date().toISOString(),
      };
      this.users.set(userId, user);
      this.userEmails.set(email.toLowerCase(), userId);
    } else {
      user = this.users.get(userId)!;
    }

    const session = this.createSession(userId);
    return { user, session };
  }

  public refreshToken(token: string): SessionToken {
    if (!this.refreshTokens.has(token)) {
      throw new Error('Invalid or expired refresh token.');
    }
    this.refreshTokens.delete(token);
    const userId = token.split('_')[1] || 'usr';
    return this.createSession(userId);
  }

  public getUser(userId: string): User | undefined {
    return this.users.get(userId);
  }

  private createSession(userId: string): SessionToken {
    const accessToken = `jwt_access_${userId}_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    const refreshToken = `ref_${userId}_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    this.refreshTokens.add(refreshToken);

    return {
      accessToken,
      refreshToken,
      expiresIn: 3600, // 1 hour
    };
  }
}
