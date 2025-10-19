/**
 * Main chat interface component
 */

'use client';

import React, { useState } from 'react';
import { useChat } from '@/hooks/useChat';
import { useLocation } from '@/hooks/useLocation';
import MessageList from './MessageList';
import InputBox from './InputBox';
import RestaurantList from '../Restaurant/RestaurantList';
import { Restaurant } from '@/types/restaurant';
import { MapPin, Loader2 } from 'lucide-react';

export default function ChatInterface() {
  const { messages, sendMessage, clearMessages, isLoading, lastResponse } = useChat();
  const { location, getCurrentLocation, setManualLocation } = useLocation();
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);

  const handleSendMessage = async (message: string) => {
    try {
      const response = await sendMessage(message, location);
      if (response?.restaurants) {
        setRestaurants(response.restaurants);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleClearChat = () => {
    clearMessages();
    setRestaurants([]);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Chat Section */}
      <div className="flex flex-col w-full lg:w-1/2 bg-white border-r">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b bg-primary-600 text-white">
          <div>
            <h1 className="text-xl font-bold">Restaurant Finder</h1>
            <p className="text-sm text-primary-100">AI-powered recommendations</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={getCurrentLocation}
              className="flex items-center gap-1 px-3 py-1 text-sm bg-white/20 rounded-lg hover:bg-white/30 transition"
            >
              <MapPin size={16} />
              {location ? 'Update' : 'Get'} Location
            </button>
            <button
              onClick={handleClearChat}
              className="px-3 py-1 text-sm bg-white/20 rounded-lg hover:bg-white/30 transition"
            >
              Clear Chat
            </button>
          </div>
        </div>

        {/* Location Status */}
        {location && (
          <div className="px-4 py-2 text-sm bg-green-50 text-green-700 border-b">
            📍 Location set: {location.address || `${location.latitude}, ${location.longitude}`}
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} />
        </div>

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-center justify-center gap-2 p-2 bg-gray-50 border-t text-gray-600">
            <Loader2 size={16} className="animate-spin" />
            <span className="text-sm">Finding restaurants...</span>
          </div>
        )}

        {/* Suggestions */}
        {lastResponse?.suggestions && lastResponse.suggestions.length > 0 && (
          <div className="p-3 border-t bg-gray-50">
            <p className="text-xs text-gray-500 mb-2">Suggestions:</p>
            <div className="flex flex-wrap gap-2">
              {lastResponse.suggestions.map((suggestion, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(suggestion)}
                  className="px-3 py-1 text-sm bg-white border rounded-full hover:bg-gray-100 transition"
                  disabled={isLoading}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="border-t bg-white">
          <InputBox onSend={handleSendMessage} disabled={isLoading} />
        </div>
      </div>

      {/* Restaurant Results Section */}
      <div className="hidden lg:block lg:w-1/2 overflow-auto bg-gray-50">
        {restaurants.length > 0 ? (
          <RestaurantList restaurants={restaurants} />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <p className="text-lg font-medium">No restaurants yet</p>
              <p className="text-sm">Ask me for restaurant recommendations!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

