"use client"

import { useState, useEffect, useRef } from 'react';


export default function Content() {
  const [messages, setMessages] = useState<Message[]>([
    { type: 'system', text: 'Hello! How can I help you today?' },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isModalOpen, setModalOpen] = useState(false);
  const [steps, setSteps] = useState<Step[]>([]);
  const [expandedSteps, setExpandedSteps] = useState<boolean[]>([]);
  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const chatBodyRef = useRef<HTMLDivElement>(null);
  const fileUploadRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!sessionStorage.getItem('uuid')) {
      const uuid = generateUUID();
      sessionStorage.setItem('uuid', uuid);
      console.log('Generated UUID:', uuid);
    } else {
      console.log('Existing UUID:', sessionStorage.getItem('uuid'));
    }
  }, []);

  const generateUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;

    const sessionId = sessionStorage.getItem('uuid');
    const newMessage = { type: 'user', text: inputValue.trim() };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInputValue('');

    const spinnerMessage: Message = { type: 'system', isSpinner: true };
    setMessages((prevMessages) => [...prevMessages, spinnerMessage]);

    try {
      const response = await fetch('http://localhost/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: newMessage.text, session_id: sessionId }),
        signal: new AbortController().signal,
      }).then((res) => res.json());

      setMessages((prevMessages) =>
        prevMessages.filter((msg) => !msg.isSpinner)
      );

      const responseMessage: Message = { type: 'system', text: response.response };
      setMessages((prevMessages) => [...prevMessages, responseMessage]);

      if (response.steps) {
        const stepsMessage: Message = { type: 'steps', steps: response.steps };
        setMessages((prevMessages) => [...prevMessages, stepsMessage]);
      }
    } catch (error) {
      setMessages((prevMessages) =>
        prevMessages.filter((msg) => !msg.isSpinner)
      );
      const errorMessage: Message = {
        type: 'system',
        text: error.name === 'AbortError'
          ? 'Request timed out. Please try again.'
          : 'An error occurred. Please try again.',
        isError: true,
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const imageMessage: Message = { type: 'user', isImage: true, src: e.target?.result as string };
        setMessages((prevMessages) => [...prevMessages, imageMessage]);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearChat = () => {
    setMessages([{ type: 'system', text: 'Hello! How can I help you today?' }]);
  };

  const showSteps = (steps: Step[]) => {
    setSteps(steps);
    setExpandedSteps(new Array(steps.length).fill(false));
    setModalOpen(true);
  };

  const toggleStep = (index: number) => {
    setExpandedSteps((prevExpandedSteps) =>
      prevExpandedSteps.map((expanded, i) => (i === index ? !expanded : expanded))
    );
  };

  const toggleDropdown = () => {
    setDropdownOpen(!isDropdownOpen);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-grow mt-20 mb-10">
        <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="border border-black p-6 rounded-lg shadow-lg">
            <div className="relative inline-block text-left mb-4">
              <button
                type="button"
                className="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                onClick={toggleDropdown}
              >
                Options
                <svg
                  className="-mr-1 ml-2 h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M5.293 9.293a1 1 0 011.414 0L10 12.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
              {isDropdownOpen && (
                <div
                  className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="options-menu"
                >
                  <div className="py-1" role="none">
                    <button
                      className="text-gray-700 block w-full text-left px-4 py-2 text-sm"
                      role="menuitem"
                      onClick={clearChat}
                    >
                      Clear Chat
                    </button>
                  </div>
                </div>
              )}
            </div>
            <div
              id="chat-body"
              className="mt-4 bg-gray-100 p-4 rounded-lg max-h-96 overflow-y-auto"
              ref={chatBodyRef}
            >
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message ${message.type}-message ${
                    message.isImage ? 'image-message' : ''
                  } ${message.isError ? 'error-message' : ''} mb-4 p-4 rounded border shadow flex`}
                  style={{
                    borderColor: message.isError ? 'red' : 'black',
                    color: message.isError ? 'white' : 'black',
                    backgroundColor: message.isError ? 'red' : 'white',
                    textAlign: message.type === 'user' ? 'right' : 'left',
                    marginLeft: message.type === 'user' ? 'auto' : '0',
                    marginRight: message.type === 'user' ? '0' : 'auto',
                    maxWidth: '80%',
                  }}
                >
                  <div className="flex-grow">
                    {message.isImage ? (
                      <img src={message.src} alt="User upload" />
                    ) : message.isSpinner ? (
                      <div className="flex justify-center items-center">
                        <div className="spinner"></div>
                      </div>
                    ) : (
                      message.text
                    )}
                  </div>
                  {message.type === 'steps' && (
                    <button
                      className="ml-2 text-blue-500 hover:text-blue-700 focus:outline-none"
                      onClick={() => showSteps(message.steps!)}
                    >
                      👁️
                    </button>
                  )}
                </div>
              ))}
            </div>
            <div className="mt-6 border-t border-gray-300 pt-4 flex items-center">
              <label
                htmlFor="file-upload"
                className="cursor-pointer text-gray-500 hover:text-gray-700 mr-2"
              >
                📂
              </label>
              <input
                id="file-upload"
                type="file"
                className="hidden"
                accept="image/*"
                ref={fileUploadRef}
                onChange={handleFileUpload}
              />
              <input
                id="chat-input"
                type="text"
                placeholder="Type a message..."
                className="w-full border border-gray-300 rounded-md px-4 py-2"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') handleSendMessage();
                }}
              />
              <button
                id="send-button"
                className="ml-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                onClick={handleSendMessage}
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
      {isModalOpen && (
        <div
          id="steps-modal"
          className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
        >
          <div className="relative top-20 mx-auto p-5 border w-2/3 shadow-lg rounded-md bg-white">
            <button
              className="close absolute top-2 right-2 text-gray-500 hover:text-gray-800"
              onClick={() => setModalOpen(false)}
            >
              &times;
            </button>
            <h3 className="text-lg font-semibold">Steps</h3>
            <div id="steps-content" className="mt-4">
              {steps.map((step, index) => (
                <div key={index} className="step mb-4">
                  <strong>Step {index + 1}:</strong><br />
                  <strong>Tool:</strong> {step[0].tool}<br />
                  <strong>Tool Input:</strong> {step[0].tool_input}<br />
                  <strong>Log:</strong> {step[0].log}<br />
                  <strong>Type:</strong> {step[0].type}<br />
                  <strong>Result:</strong>
                  <span className="result-content">
                    {expandedSteps[index] ? step[1] : step[1].substring(0, 100) + '...'}
                  </span>
                  <button
                    className="show-more-button ml-2 text-blue-500 hover:text-blue-700"
                    onClick={() => toggleStep(index)}
                  >
                    {expandedSteps[index] ? 'View Less' : 'View More'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

