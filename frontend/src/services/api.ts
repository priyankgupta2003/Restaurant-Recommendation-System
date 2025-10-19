/**
 * API service for backend communication
 */

import axios, { AxiosInstance } from 'axios';
import { ChatRequest, ChatResponse } from '@/types/chat';
import { Restaurant, RestaurantSearchParams } from '@/types/restaurant';

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Chat endpoints
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await this.client.post<ChatResponse>('/api/v1/chat', request);
    return response.data;
  }

  async getSession(sessionId: string): Promise<any> {
    const response = await this.client.get(`/api/v1/chat/session/${sessionId}`);
    return response.data;
  }

  async clearSession(sessionId: string): Promise<void> {
    await this.client.delete(`/api/v1/chat/session/${sessionId}`);
  }

  // Restaurant endpoints
  async searchRestaurants(params: RestaurantSearchParams): Promise<{
    restaurants: Restaurant[];
    total: number;
  }> {
    const response = await this.client.post('/api/v1/restaurants/search', params);
    return response.data;
  }

  async getRestaurantDetails(
    restaurantId: string,
    includeReviews: boolean = true
  ): Promise<Restaurant> {
    const response = await this.client.get(`/api/v1/restaurants/${restaurantId}`, {
      params: { include_reviews: includeReviews },
    });
    return response.data;
  }

  async getNearbyRestaurants(
    latitude: number,
    longitude: number,
    radius: number = 5000,
    limit: number = 20
  ): Promise<{ restaurants: Restaurant[]; total: number }> {
    const response = await this.client.get('/api/v1/restaurants/nearby', {
      params: { latitude, longitude, radius, limit },
    });
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await this.client.get('/api/v1/health');
    return response.data;
  }
}

export const apiService = new APIService();

