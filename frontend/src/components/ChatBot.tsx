// frontend/src/components/ChatBot.tsx
'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useAuth } from '../providers/AuthProvider';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageCircle,
  X,
  Send,
  Sparkles,
  Loader2,
  Minimize2,
  Maximize2,
} from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatResponse {
  response: string;
  conversation_id: string;
  tool_calls?: {
    tool_name: string;
    result: any;
  }[];
}

// Custom event for task updates
const TASK_UPDATE_EVENT = 'chatbot-task-update';

interface ChatBotProps {
  onTaskUpdate?: () => void;
}

const ChatBot: React.FC<ChatBotProps> = ({ onTaskUpdate }) => {
  const { user, token } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversation history from localStorage on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedMessages = localStorage.getItem(`chatbot-messages-${user?.id}`);
      const savedConversationId = localStorage.getItem(`chatbot-conversation-${user?.id}`);
      
      if (savedMessages) {
        try {
          const parsed = JSON.parse(savedMessages);
          // Convert timestamp strings back to Date objects
          setMessages(parsed.map((m: any) => ({
            ...m,
            timestamp: new Date(m.timestamp)
          })));
        } catch (e) {
          console.error('Failed to load chat history:', e);
        }
      }
      
      if (savedConversationId) {
        setConversationId(savedConversationId);
      }
    }
  }, [user?.id]);

  // Save conversation history to localStorage
  useEffect(() => {
    if (typeof window !== 'undefined' && messages.length > 0) {
      localStorage.setItem(`chatbot-messages-${user?.id}`, JSON.stringify(messages));
    }
  }, [messages, user?.id]);

  // Save conversation ID
  useEffect(() => {
    if (typeof window !== 'undefined' && conversationId) {
      localStorage.setItem(`chatbot-conversation-${user?.id}`, conversationId);
    }
  }, [conversationId, user?.id]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Notify parent component to refresh tasks
  const notifyTaskUpdate = useCallback(() => {
    // Dispatch custom event for any listening components
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent(TASK_UPDATE_EVENT));
    }
    // Call parent callback if provided
    if (onTaskUpdate) {
      onTaskUpdate();
    }
  }, [onTaskUpdate]);

  // Check if response indicates a task modification
  const isTaskModification = (response: string, toolCalls?: any[]): boolean => {
    const modificationKeywords = [
      '[OK] Task added',
      '[Done]',
      '[Deleted]',
      'Task added',
      'Task complete',
      'Task delete',
      'task added',
      'task complete',
      'task delete'
    ];
    
    // Check response text
    if (modificationKeywords.some(keyword => response.toLowerCase().includes(keyword.toLowerCase()))) {
      return true;
    }
    
    // Check tool calls
    if (toolCalls && toolCalls.length > 0) {
      const modificationTools = ['add_task', 'complete_task', 'delete_task', 'update_task'];
      return toolCalls.some(tc => modificationTools.includes(tc?.tool_name));
    }
    
    return false;
  };

  const sendMessage = async () => {
    if (!input.trim() || !user) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    // Check for "new chat" command locally
    const messageLower = input.trim().toLowerCase();
    if (['new chat', 'fresh chat', 'start over', 'clear chat', 'reset chat'].includes(messageLower)) {
      // Clear conversation immediately
      clearHistory();
      // Still send to backend for consistency but use the cleared state
    }

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/${user.id}/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            message: userMessage.content,
            conversation_id: conversationId || undefined,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to send message');
      }

      const data: ChatResponse = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setConversationId(data.conversation_id);

      // Check if this was a task modification and trigger real-time update
      if (isTaskModification(data.response, data.tool_calls)) {
        console.log('Task modification detected, triggering real-time update...');
        // Small delay to let the message appear first
        setTimeout(() => {
          notifyTaskUpdate();
        }, 500);
      }
    } catch (error: any) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    setIsMinimized(false);
  };

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  const clearHistory = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(`chatbot-messages-${user?.id}`);
      localStorage.removeItem(`chatbot-conversation-${user?.id}`);
    }
    setMessages([]);
    setConversationId(null);
  };

  return (
    <>
      {/* Floating Chat Button */}
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-50 w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-full shadow-lg shadow-purple-500/30 flex items-center justify-center transition-all duration-300"
      >
        {isOpen ? (
          <X className="w-7 h-7" />
        ) : (
          <MessageCircle className="w-7 h-7" />
        )}
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{
              opacity: 1,
              y: 0,
              scale: 1,
              height: isMinimized ? 'auto' : '600px',
            }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="fixed bottom-24 right-6 z-50 w-96 max-w-[calc(100vw-3rem)] bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden flex flex-col"
            style={{ minHeight: isMinimized ? 'auto' : '600px' }}
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">TaskMaster AI</h3>
                  <p className="text-xs text-white/80">Your intelligent assistant</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {messages.length > 0 && (
                  <button
                    onClick={clearHistory}
                    className="p-2 hover:bg-white/20 rounded-lg transition-colors text-white/80 hover:text-white text-xs"
                    title="Clear conversation history"
                  >
                    Clear
                  </button>
                )}
                <button
                  onClick={toggleMinimize}
                  className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                  title={isMinimized ? 'Expand' : 'Minimize'}
                >
                  {isMinimized ? (
                    <Maximize2 className="w-5 h-5 text-white" />
                  ) : (
                    <Minimize2 className="w-5 h-5 text-white" />
                  )}
                </button>
                <button
                  onClick={toggleChat}
                  className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5 text-white" />
                </button>
              </div>
            </div>

            {!isMinimized && (
              <>
                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-gray-800/50">
                  {messages.length === 0 ? (
                    <div className="text-center py-8">
                      <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 rounded-full flex items-center justify-center">
                        <Sparkles className="w-8 h-8 text-purple-500" />
                      </div>
                      <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                        Hi! I'm TaskMaster AI 👋
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                        I can help you manage your tasks with natural language
                      </p>
                      
                      {/* Capabilities Table */}
                      <div className="w-full max-w-sm mx-auto mb-4">
                        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                          <div className="bg-gradient-to-r from-purple-600 to-blue-600 px-4 py-3">
                            <h5 className="font-semibold text-white text-sm">What I Can Do</h5>
                          </div>
                          <div className="divide-y divide-gray-200 dark:divide-gray-700">
                            <div className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                              <div className="flex items-start gap-3">
                                <span className="text-lg">✅</span>
                                <div className="text-left">
                                  <p className="text-sm font-medium text-gray-900 dark:text-white">Create Tasks</p>
                                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">"Add a task to buy groceries"</p>
                                </div>
                              </div>
                            </div>
                            <div className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                              <div className="flex items-start gap-3">
                                <span className="text-lg">📋</span>
                                <div className="text-left">
                                  <p className="text-sm font-medium text-gray-900 dark:text-white">View Tasks</p>
                                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">"Show my pending tasks"</p>
                                </div>
                              </div>
                            </div>
                            <div className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                              <div className="flex items-start gap-3">
                                <span className="text-lg">✓</span>
                                <div className="text-left">
                                  <p className="text-sm font-medium text-gray-900 dark:text-white">Complete Tasks</p>
                                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">"Mark task as done"</p>
                                </div>
                              </div>
                            </div>
                            <div className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                              <div className="flex items-start gap-3">
                                <span className="text-lg">🗑️</span>
                                <div className="text-left">
                                  <p className="text-sm font-medium text-gray-900 dark:text-white">Delete Tasks</p>
                                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">"Remove completed tasks"</p>
                                </div>
                              </div>
                            </div>
                            <div className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                              <div className="flex items-start gap-3">
                                <span className="text-lg">✏️</span>
                                <div className="text-left">
                                  <p className="text-sm font-medium text-gray-900 dark:text-white">Update Tasks</p>
                                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">"Change task priority"</p>
                                </div>
                              </div>
                            </div>
                            <div className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                              <div className="flex items-start gap-3">
                                <span className="text-lg">💡</span>
                                <div className="text-left">
                                  <p className="text-sm font-medium text-gray-900 dark:text-white">Get Help</p>
                                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">"Help me organize my day"</p>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <p className="text-xs text-gray-500 dark:text-gray-500">
                        Just type naturally and I'll help you! 🚀
                      </p>
                    </div>
                  ) : (
                    <>
                      {messages.map((message, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className={`flex ${
                            message.role === 'user' ? 'justify-end' : 'justify-start'
                          }`}
                        >
                          <div
                            className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                              message.role === 'user'
                                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                                : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700'
                            }`}
                          >
                            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                            <p
                              className={`text-xs mt-1 ${
                                message.role === 'user'
                                  ? 'text-white/70'
                                  : 'text-gray-500 dark:text-gray-400'
                              }`}
                            >
                              {message.timestamp.toLocaleTimeString([], {
                                hour: '2-digit',
                                minute: '2-digit',
                              })}
                            </p>
                          </div>
                        </motion.div>
                      ))}
                      {loading && (
                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="flex justify-start"
                        >
                          <div className="bg-white dark:bg-gray-800 rounded-2xl px-4 py-3 border border-gray-200 dark:border-gray-700">
                            <div className="flex items-center gap-2">
                              <Loader2 className="w-4 h-4 animate-spin text-purple-600" />
                              <span className="text-sm text-gray-600 dark:text-gray-400">
                                Thinking...
                              </span>
                            </div>
                          </div>
                        </motion.div>
                      )}
                      <div ref={messagesEndRef} />
                    </>
                  )}
                </div>

                {/* Input */}
                <div className="p-4 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Ask me anything about your tasks..."
                      className="flex-1 px-4 py-3 bg-gray-100 dark:bg-gray-800 border-0 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 dark:text-white"
                      disabled={loading}
                    />
                    <button
                      onClick={sendMessage}
                      disabled={loading || !input.trim()}
                      className="p-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-400 text-white rounded-xl transition-all duration-300 disabled:cursor-not-allowed"
                    >
                      <Send className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default ChatBot;
