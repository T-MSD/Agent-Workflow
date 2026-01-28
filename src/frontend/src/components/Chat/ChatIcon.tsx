import ai_icon from '../../assets/ai_icon.svg';
import user_icon from '../../assets/user_icon.svg';
import type { MessageRole } from '../../types/messages';

interface ChatIconProps {
  role: MessageRole;
}

function ChatIcon({ role }: ChatIconProps) {
    const src = role === 'User' ? user_icon : ai_icon;

  return (
    <img
      src={src}
      style={{ filter: 'invert(1)' }}
      className={role === 'User' 
        ? 'w-9 h-9 ml-auto mb-2' 
        : 'w-8 h-8 mb-2'}
    />
  );
}

export default ChatIcon;
