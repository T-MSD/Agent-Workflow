import { useState } from 'react';
import { invokeAgent } from '../services/api';

interface AgentState {
  response: string;
  isLoading: boolean;
}

export function useAgent() {
  const [state, setState] = useState<AgentState>({
    response: '',
    isLoading: false,
  });

  const askAgent = async (prompt: string): Promise<string> => {
    if (!prompt.trim()) {
      setState({ response: '', isLoading: false});
      return '';
    }

    setState({ response: '', isLoading: true});

    try {
      const result = await invokeAgent(prompt);
      setState({ response: result, isLoading: false});
      return result;
    } catch (err) {
      setState({ response: '', isLoading: false});
      console.error(err);
      return 'Agent failed to respond.';
    }
  };

  return { ...state, askAgent };
}
