/**
 * Chat-related type definitions
 */

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  location?: Location;
  preferences?: UserPreferences;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  restaurants?: Restaurant[];
  suggestions?: string[];
  metadata?: Record<string, any>;
}

export interface Location {
  address?: string;
  latitude?: number;
  longitude?: number;
  city?: string;
  state?: string;
}

export interface UserPreferences {
  cuisine?: string;
  price_range?: string;
  dietary?: string[];
  [key: string]: any;
}

