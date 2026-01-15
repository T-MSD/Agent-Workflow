import { useState } from 'react';
import { invokeAgent } from '../services/api';

interface AgentState {
  data: string;
  isLoading: boolean;
  error: string | null;
}

export function useAgent() {
  const [state, setState] = useState<AgentState>({
    data: '',
    isLoading: false,
    error: null,
  });

  const askAgent = async (prompt: string) => {
    if (!prompt.trim()) {
      setState({ data: '', isLoading: false, error: 'Please enter a prompt.' });
      return;
    }

    setState({ data: '', isLoading: true, error: null });

    try {
      const result = await invokeAgent(prompt);
      setState({ data: result, isLoading: false, error: null });
    } catch (err) {
      setState({ data: '', isLoading: false, error: 'Agent failed to respond.' });
      console.error(err);
    }
  };

  return { ...state, askAgent };
}