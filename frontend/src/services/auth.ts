"""
Authentication service for managing auth tokens and user session.
"""

import { apiClient } from './api';

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user_info';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: UserInfo;
}

export interface UserInfo {
  user_id: string;
  email: string;
  name: string;
  role: string;
}

class AuthService {
  login(credentials: LoginRequest): Promise<LoginResponse> {
    // TODO: Implement login endpoint call
    throw new Error('Login not implemented');
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  }

  getUser(): UserInfo | null {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  }

  setUser(user: UserInfo): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export const authService = new AuthService();
