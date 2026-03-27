import { useState, useEffect, useCallback } from 'react';
import { fetchConversations, deleteConversation as deleteConversationApi } from '../services/api';
import type { Conversation } from '../types/types';

export function useConversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadConversations = useCallback(async () => {
    try {
      const data = await fetchConversations();
      setConversations(data);
    } catch (err) {
      console.error('Failed to load conversations:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const removeConversation = async (id: string) => {
    try {
      await deleteConversationApi(id);
      setConversations((prev) => prev.filter((c) => c.id !== id));
      return true;
    } catch (err) {
      console.error('Failed to delete conversation:', err);
      return false;
    }
  };

  const addConversation = (conversation: Conversation) => {
    setConversations((prev) => [conversation, ...prev]);
  };

  const refreshConversations = () => {
    loadConversations();
  };

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  return {
    conversations,
    isLoading,
    removeConversation,
    addConversation,
    refreshConversations,
  };
}
