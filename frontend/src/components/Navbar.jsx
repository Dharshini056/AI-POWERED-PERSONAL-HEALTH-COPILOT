import React from 'react';
import { 
  Activity, 
  UploadCloud, 
  Calendar, 
  Pill, 
  FileText, 
  MessageSquare, 
  ShieldCheck, 
  Layers, 
  Sparkles,
  Globe,
  RotateCcw
} from 'lucide-react';

export default function Navbar({ 
  activeTab, 
  setActiveTab, 
  selectedLanguage, 
  setSelectedLanguage,
  onLoadDemo,
  onResetData,
  isDemoLoading
}) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'upload', label: 'Upload & OCR', icon: UploadCloud },
    { id: 'timeline', label: 'Health Timeline', icon: Calendar },
    { id: 'medications', label: 'Medications', icon: Pill },
    { id: 'labs', label: 'Lab Reports', icon: FileText },
    { id: 'chat', label: 'Ask Copilot', icon: MessageSquare },
    { id: 'abha', label: 'ABHA & FHIR', icon: ShieldCheck },
    { id: 'architecture', label: 'Architecture', icon: Layers },
  ];

  const languages = [
    { code: 'English', label: 'English' },
    { code: 'Tamil', label: 'தமிழ் (Tamil)' },
    { code: 'Hindi', label: 'हिन्दी (Hindi)' },
    { code: 'Telugu', label: 'తెలుగు (Telugu)' },
    { code: 'Malayalam', label: 'മലയാളം (Malayalam)' },
    { code: 'Kannada', label: 'ಕನ್ನಡ (Kannada)' },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
      {/* Top Banner */}
      <div className="bg-teal-900 text-teal-100 text-xs py-1.5 px-4 text-center flex items-center justify-between">
        <div className="flex items-center space-x-2 mx-auto">
          <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        </div>
        <div className="hidden lg:flex items-center space-x-2 text-teal-200 text-xs">
          <span>Mock ABHA: <strong className="text-white">91-4521-8934-1022</strong></span>
        </div>
      </div>

      {/* Main Header Row */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-500 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
              <Activity className="w-6 h-6 stroke-[2.5]" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-lg font-bold text-slate-900 tracking-tight">AI Personal Health Copilot</span>
                <span className="bg-teal-50 text-teal-700 text-[10px] font-semibold px-2 py-0.5 rounded-full border border-teal-200">
                  Multilingual OCR
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">Understand your health. Organize your records. Stay informed.</p>
            </div>
          </div>

          {/* Quick Actions (Language Selector & Demo Mode) */}
          <div className="flex items-center space-x-3">
            {/* Language Selector */}
            <div className="flex items-center bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-700">
              <Globe className="w-3.5 h-3.5 text-teal-600 mr-1.5" />
              <select 
                value={selectedLanguage} 
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="bg-transparent font-medium text-slate-800 focus:outline-hidden cursor-pointer"
              >
                {languages.map((l) => (
                  <option key={l.code} value={l.code}>{l.label}</option>
                ))}
              </select>
            </div>

            {/* Demo Mode Button */}
            <button
              onClick={onLoadDemo}
              disabled={isDemoLoading}
              className="flex items-center space-x-1.5 bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white text-xs font-semibold px-3.5 py-2 rounded-lg shadow-sm transition disabled:opacity-50 cursor-pointer"
              title="Preload 4 synthetic sample records (Prescriptions, Lab Reports, Bilingual English/Tamil)"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>{isDemoLoading ? 'Loading Demo...' : 'Demo Mode (1-Click)'}</span>
            </button>

            {/* Reset Button */}
            <button
              onClick={onResetData}
              className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition cursor-pointer"
              title="Reset all records to fresh state"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Navigation Tabs Bar */}
        <nav className="flex space-x-1 overflow-x-auto py-1.5 border-t border-slate-100 no-scrollbar">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-xs font-medium whitespace-nowrap transition cursor-pointer ${
                  isActive
                    ? 'bg-teal-50 text-teal-700 border border-teal-200/80 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-teal-600' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
