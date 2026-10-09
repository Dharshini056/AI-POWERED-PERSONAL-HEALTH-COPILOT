import React, { useState } from 'react';
import { 
  Sparkles, 
  AlertTriangle, 
  FileText, 
  Pill, 
  Activity, 
  Calendar, 
  ArrowRight, 
  Languages, 
  CheckCircle2, 
  Stethoscope, 
  Clock,
  ShieldCheck,
  ChevronRight
} from 'lucide-react';
import OverviewCards from './OverviewCards';
import HealthTimeline from './HealthTimeline';
import MedicationCards from './MedicationCards';
import LabOverview from './LabOverview';

export default function DashboardView({ 
  profile, 
  timeline, 
  selectedLanguage, 
  setSelectedLanguage,
  onNavigate,
  onViewOCR 
}) {
  const stats = profile?.stats || {};
  const medications = profile?.medications || [];
  const labResults = profile?.lab_results || [];
  const diagnoses = profile?.diagnoses || [];
  const events = profile?.medical_events || [];

  // Abnormal lab findings
  const abnormalLabs = labResults.filter((l) =>
    ['Below reference range', 'Above reference range', 'High', 'Low', 'Critical'].includes(l.status)
  );

  return (
    <div className="space-y-6">
      
      {/* Hero Welcome & AI Health Summary Card */}
      <div className="bg-gradient-to-r from-teal-800 via-teal-700 to-slate-900 rounded-2xl p-6 sm:p-8 text-white shadow-md relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="flex items-center space-x-2">
            <span className="bg-teal-500/20 text-teal-300 text-[11px] font-bold px-3 py-1 rounded-full border border-teal-400/30 flex items-center space-x-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>AI PERSONAL HEALTH COPILOT</span>
            </span>
            <span className="text-xs text-teal-200">Patient: <strong>{profile?.patient?.name || 'Arun Kumar'} (42 Y, Male)</strong></span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
            Understand your health. Organize your records. Stay informed.
          </h1>

          <p className="text-xs sm:text-sm text-teal-100 leading-relaxed max-w-2xl">
            Ingest prescriptions, laboratory reports, and hospital records with multilingual OCR in English & Tamil. 
            Automated entity extraction transforms fragmented files into a unified FHIR-ready health timeline.
          </p>

          {/* Multilingual Summary Box */}
          <div className="pt-2">
            <div className="bg-teal-950/70 border border-teal-600/40 rounded-xl p-4 text-xs backdrop-blur-xs">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-teal-300 flex items-center space-x-1.5">
                  <Languages className="w-4 h-4 text-teal-400" />
                  <span>AI Clinical Summary ({selectedLanguage === 'Tamil' ? 'தமிழ் சுருக்கம்' : 'English Overview'}):</span>
                </span>
                <span className="text-[11px] text-teal-200 font-mono">
                  {stats.total_documents || 0} Records Processed
                </span>
              </div>

              <p className="text-slate-200 leading-relaxed font-sans">
                {selectedLanguage === 'Tamil' ? (
                  "இந்த போர்டலில் அருண் குமார் என்பவரின் மருத்துவ ஆவணங்கள், இரத்தப் பரிசோதனை அறிக்கைகள் மற்றும் மருந்துச் சீட்டுகள் வெற்றிகரமாக பகுப்பாய்வு செய்யப்பட்டுள்ளன. கண்டறியப்பட்ட தகவல்கள் கீழே விரிவாக பட்டியலிடப்பட்டுள்ளன. மருத்துவ முடிவுகளுக்கு உங்கள் மருத்துவரை அணுகவும்."
                ) : (
                  `Consolidated profile includes ${medications.length} active prescription orders, ${labResults.length} laboratory observations (${abnormalLabs.length} outside reference interval), and ${diagnoses.length} clinical conditions from your uploaded records.`
                )}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 1. Overview Metric Cards */}
      <OverviewCards stats={stats} onNavigate={onNavigate} />

      {/* 2. AI Insights & Important Findings */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-amber-50 border border-amber-200 text-amber-700 flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900">AI Health Insights & Important Findings</h2>
              <p className="text-xs text-slate-500">Key observations extracted from your uploaded medical documents</p>
            </div>
          </div>

          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700">
            {abnormalLabs.length + diagnoses.length} Findings
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          {/* Finding 1: Abnormal Labs */}
          <div className="bg-amber-50/40 border border-amber-200 rounded-xl p-4 space-y-2">
            <div className="flex items-center space-x-2 text-amber-900 font-bold text-xs">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
              <span>Laboratory Reference Interval Notice</span>
            </div>
            <p className="text-xs text-slate-700 leading-relaxed">
              {abnormalLabs.length > 0 ? (
                <>
                  Found <strong>{abnormalLabs.length} parameter(s)</strong> outside standard reference ranges: {' '}
                  {abnormalLabs.map((l) => `${l.test_name} (${l.value} ${l.unit})`).join(', ')}. 
                  Discuss these results with your physician for comprehensive clinical interpretation.
                </>
              ) : (
                "All documented laboratory parameters fall within their normal physiological reference limits."
              )}
            </p>
          </div>

          {/* Finding 2: Diagnoses & Conditions */}
          <div className="bg-teal-50/40 border border-teal-200 rounded-xl p-4 space-y-2">
            <div className="flex items-center space-x-2 text-teal-900 font-bold text-xs">
              <Stethoscope className="w-4 h-4 text-teal-600 shrink-0" />
              <span>Documented Clinical Conditions</span>
            </div>
            <p className="text-xs text-slate-700 leading-relaxed">
              {diagnoses.length > 0 ? (
                <>
                  Recorded conditions include: <strong>{diagnoses.map((d) => d.name).join(', ')}</strong>. 
                  Maintenance therapy is active under prescription surveillance.
                </>
              ) : (
                "No chronic conditions currently flagged in uploaded files."
              )}
            </p>
          </div>
        </div>
      </div>

      {/* 3. Recent Health Activity & Latest Events */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center">
              <Calendar className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900">Recent Health Activity</h2>
              <p className="text-xs text-slate-500">Latest medical events, visits, and reports</p>
            </div>
          </div>

          <button
            onClick={() => onNavigate('timeline')}
            className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center space-x-1 cursor-pointer"
          >
            <span>View Full Timeline</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="divide-y divide-slate-100 mt-2">
          {events.slice(0, 4).map((ev, idx) => (
            <div key={idx} className="py-3.5 flex items-center justify-between gap-4">
              <div className="flex items-center space-x-3">
                <div className="w-9 h-9 rounded-lg bg-teal-50 border border-teal-100 text-teal-700 flex items-center justify-center text-xs font-bold shrink-0">
                  {ev.event_type?.substring(0, 2).toUpperCase() || 'EV'}
                </div>
                <div>
                  <h3 className="text-xs font-bold text-slate-900">{ev.title}</h3>
                  <p className="text-[11px] text-slate-500">{ev.facility_name} • {ev.doctor_name}</p>
                </div>
              </div>

              <span className="text-xs font-mono text-slate-500 bg-slate-50 px-2 py-1 rounded border border-slate-200 shrink-0">
                {ev.event_date || 'Recent'}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 4. Medications Quick Overview */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Pill className="w-5 h-5 text-blue-600" />
            <span>Medication Overview</span>
          </h2>
          <button
            onClick={() => onNavigate('medications')}
            className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center space-x-1 cursor-pointer"
          >
            <span>Explore All Medications</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <MedicationCards medications={medications.slice(0, 3)} selectedLanguage={selectedLanguage} />
      </div>

      {/* 5. Lab Overview */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Activity className="w-5 h-5 text-teal-600" />
            <span>Lab Test Values & Analysis</span>
          </h2>
          <button
            onClick={() => onNavigate('labs')}
            className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center space-x-1 cursor-pointer"
          >
            <span>Explore All Lab Reports</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <LabOverview labResults={labResults} selectedLanguage={selectedLanguage} />
      </div>

      {/* 6. Health Timeline */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
            <Calendar className="w-5 h-5 text-teal-600" />
            <span>Chronological Timeline Preview</span>
          </h2>
          <button
            onClick={() => onNavigate('timeline')}
            className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center space-x-1 cursor-pointer"
          >
            <span>Full Interactive Timeline</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <HealthTimeline timelineEvents={timeline} onSelectDocument={onViewOCR} />
      </div>

    </div>
  );
}
