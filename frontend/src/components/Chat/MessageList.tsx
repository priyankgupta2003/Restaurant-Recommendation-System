/**
 * Message list component
 */

'use client';

import React, { useEffect, useRef } from 'react';
import { Message } from '@/types/chat';
import { User, Bot } from 'lucide-react';

interface MessageListProps {
  messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        <div className="text-center p-8">
          <Bot size={48} className="mx-auto mb-4 opacity-50" />
          <h2 className="text-xl font-semibold mb-2">Welcome! 👋</h2>
          <p className="text-sm">Ask me to find restaurants near you.</p>
          <div className="mt-6 text-left max-w-md mx-auto">
            <p className="text-sm font-medium mb-2">Try asking:</p>
            <ul className="text-sm space-y-1 text-gray-500">
              <li>• "Find me Italian restaurants nearby"</li>
              <li>• "Show me cheap sushi places"</li>
              <li>• "Best rated restaurants in San Francisco"</li>
              <li>• "Vegan-friendly cafes with outdoor seating"</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex gap-3 ${
            message.role === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          {message.role === 'assistant' && (
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white">
              <Bot size={18} />
            </div>
          )}
          <div
            className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              message.role === 'user'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            <p
              className={`text-xs mt-1 ${
                message.role === 'user' ? 'text-primary-100' : 'text-gray-500'
              }`}
            >
              {new Date(message.timestamp).toLocaleTimeString()}
            </p>
          </div>
          {message.role === 'user' && (
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-700">
              <User size={18} />
            </div>
          )}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

