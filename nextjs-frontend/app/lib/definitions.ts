type Message = {
  type: 'system' | 'user' | 'steps';
  text?: string;
  isSpinner?: boolean;
  isImage?: boolean;
  src?: string;
  steps?: Step[];
};

type Step = [
  {
    tool: string;
    tool_input: string;
    log: string;
    type: string;
  },
  string
];
