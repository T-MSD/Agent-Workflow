import { useState } from 'react';
import { invokeAgent } from '../services/api';
import type { AskResult } from '../types/types';

interface AgentState {
  response: string;
  isLoading: boolean;
}

export function useAgent() {
  const [state, setState] = useState<AgentState>({
    response: '',
    isLoading: false,
  });

  const askAgent = async (prompt: string, conversationId?: string): Promise<AskResult> => {
    if (!prompt.trim()) {
      setState({ response: '', isLoading: false });
      return { ok: false, error: 'Please enter a prompt.' };
    }

    setState({ response: '', isLoading: true });

    try {
      const result = await invokeAgent(prompt, conversationId);
      setState({ response: result.response, isLoading: false });
      return { ok: true, text: result.response, conversationId: result.conversationId };
    } catch (err) {
      setState({ response: '', isLoading: false });
      console.error(err);
      return { ok: false, error: 'Agent failed to respond.' };
    }
  };

  return { ...state, askAgent };
}
