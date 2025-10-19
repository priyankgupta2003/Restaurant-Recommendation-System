/**
 * Custom hook for chat functionality
 */

import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiService } from '@/services/api';
import { ChatRequest, ChatResponse, Message } from '@/types/chat';

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);

  const sendMessageMutation = useMutation({
    mutationFn: (request: ChatRequest) => apiService.sendMessage(request),
    onSuccess: (response: ChatResponse) => {
      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setSessionId(response.session_id);
    },
  });

  const sendMessage = useCallback(
    async (content: string, location?: any, preferences?: any) => {
      // Add user message immediately
      const userMessage: Message = {
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Send to backend
      const request: ChatRequest = {
        message: content,
        session_id: sessionId,
        location,
        preferences,
      };

      return sendMessageMutation.mutateAsync(request);
    },
    [sessionId, sendMessageMutation]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    if (sessionId) {
      apiService.clearSession(sessionId).catch(console.error);
    }
    setSessionId(undefined);
  }, [sessionId]);

  return {
    messages,
    sessionId,
    sendMessage,
    clearMessages,
    isLoading: sendMessageMutation.isPending,
    error: sendMessageMutation.error,
    lastResponse: sendMessageMutation.data,
  };
}

