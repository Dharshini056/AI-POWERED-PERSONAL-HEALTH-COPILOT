import React, { useState, useRef, useEffect } from 'react';
import { 
  MessageSquare, 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  ShieldAlert, 
  Languages, 
  Loader2, 
  FileCheck2,
  HelpCircle,
  Stethoscope
} from 'lucide-react';
import { sendChatMessage } from '../services/api';

const QUICK_PROMPTS = [
  'What medicines are mentioned in my prescription?',
  'What are my abnormal lab values?',
  'Explain my blood report in simple language.',
  'Show my recent medical history.',
  'Translate my report into Tamil.',
  'What should I ask my doctor about this report?'
];

export default function HealthCopilotChat({ selectedLanguage = 'English' }) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content: "Hello Arun! I am your AI Personal Health Copilot. I can help you understand your uploaded prescriptions, explain your lab tests in simple terms, or prepare questions for your doctor. How can I assist you today?",
      sources: ["Clinical Context Engine"]
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputText;
    if (!text || !text.trim() || isLoading) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text.trim()
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(text.trim(), selectedLanguage);
      const botMessage = {
        id: `bot-${Date.now()}`,
        role: 'assistant',
        content: response.reply,
        sources: response.sources || ['Uploaded Medical Records'],
        disclaimer: response.disclaimer
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: `bot-err-${Date.now()}`,
          role: 'assistant',
          content: "I couldn't find that information in your uploaded records or encountered a processing issue. Please verify your connection or re-upload your document.",
          sources: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs flex flex-col h-[700px] overflow-hidden">
      
      {/* Header */}
      <div className="p-4 sm:p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-500 flex items-center justify-center text-white shadow-xs">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
              <span>Ask your Health Copilot</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            </h2>
            <p className="text-xs text-slate-500">
              Grounded exclusively on your uploaded medical records • Multi-turn conversational AI
            </p>
          </div>
        </div>

        <div className="hidden sm:flex items-center space-x-2 text-xs text-teal-800 bg-teal-50 px-2.5 py-1 rounded-lg border border-teal-200">
          <Languages className="w-3.5 h-3.5" />
          <span>Responding in: <strong>{selectedLanguage}</strong></span>
        </div>
      </div>

      {/* Suggested Quick Prompt Chips */}
      <div className="px-4 py-2.5 bg-slate-100/60 border-b border-slate-200 overflow-x-auto no-scrollbar">
        <div className="flex items-center space-x-2 whitespace-nowrap">
          <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center shrink-0">
            <Sparkles className="w-3 h-3 text-amber-500 mr-1" />
            Suggested:
          </span>
          {QUICK_PROMPTS.map((prompt, i) => (
            <button
              key={i}
              onClick={() => handleSendMessage(prompt)}
              disabled={isLoading}
              className="text-xs bg-white hover:bg-teal-50 hover:text-teal-700 text-slate-700 px-3 py-1 rounded-full border border-slate-200 hover:border-teal-300 transition shadow-2xs shrink-0 cursor-pointer disabled:opacity-50"
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Body */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-slate-50/30">
        {messages.map((msg) => {
          const isUser = msg.role === 'user';
          return (
            <div
              key={msg.id}
              className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}
            >
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                isUser ? 'bg-teal-600 text-white' : 'bg-slate-800 text-teal-300'
              }`}>
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 text-xs leading-relaxed ${
                isUser 
                  ? 'bg-teal-600 text-white shadow-xs rounded-tr-xs' 
                  : 'bg-white text-slate-800 border border-slate-200 shadow-2xs rounded-tl-xs space-y-2'
              }`}>
                <div className="whitespace-pre-wrap font-sans text-xs sm:text-[13px]">{msg.content}</div>

                {/* Grounding Source Badges */}
                {!isUser && msg.sources && msg.sources.length > 0 && (
                  <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center gap-1.5 text-[10px] text-slate-500">
                    <span className="font-semibold text-slate-600 flex items-center">
                      <FileCheck2 className="w-3 h-3 text-teal-600 mr-1" />
                      Grounded Sources:
                    </span>
                    {msg.sources.map((src, sIdx) => (
                      <span key={sIdx} className="bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded font-mono">
                        {src}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex items-center space-x-3 text-slate-500 text-xs">
            <div className="w-8 h-8 rounded-lg bg-slate-800 text-teal-300 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl px-4 py-3 shadow-2xs flex items-center space-x-2">
              <Loader2 className="w-4 h-4 text-teal-600 animate-spin" />
              <span>Analyzing uploaded medical records...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Persistent Medical Disclaimer (Prompt Requirement) */}
      <div className="px-4 py-2 bg-amber-50/70 border-t border-amber-200 text-amber-900 text-[11px] flex items-center justify-center space-x-1.5">
        <ShieldAlert className="w-3.5 h-3.5 text-amber-600 shrink-0" />
        <span>This AI provides informational support and does not replace professional medical advice. Always consult your doctor.</span>
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="p-3 sm:p-4 bg-white border-t border-slate-200 flex items-center space-x-2"
      >
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Ask a question about your medicines, lab values, or medical history..."
          disabled={isLoading}
          className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-slate-800 placeholder-slate-400 focus:outline-hidden focus:border-teal-500 focus:bg-white"
        />
        <button
          type="submit"
          disabled={!inputText.trim() || isLoading}
          className="bg-teal-600 hover:bg-teal-700 text-white p-2.5 sm:px-4 sm:py-2.5 rounded-xl font-semibold text-xs sm:text-sm transition flex items-center space-x-1.5 disabled:opacity-40 cursor-pointer shadow-xs"
        >
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline">Send</span>
        </button>
      </form>

    </div>
  );
}
