import React, { useState } from 'react';
import { 
  Calendar, 
  FileText, 
  Pill, 
  Activity, 
  ChevronRight, 
  ChevronDown, 
  Clock, 
  Building2, 
  User, 
  Stethoscope, 
  CheckCircle2,
  ExternalLink
} from 'lucide-react';

export default function HealthTimeline({ timelineEvents, onSelectDocument }) {
  const [expandedId, setExpandedId] = useState(null);
  const [filterType, setFilterType] = useState('all');

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const filteredEvents = (timelineEvents || []).filter((ev) => {
    if (filterType === 'all') return true;
    return ev.category?.toLowerCase().includes(filterType.toLowerCase());
  });

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 tracking-tight flex items-center space-x-2">
            <Calendar className="w-5 h-5 text-teal-600" />
            <span>Unified Health Timeline</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Chronological personal health journey generated automatically from uploaded medical records.
          </p>
        </div>

        {/* Filter Chips */}
        <div className="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-lg text-xs">
          <button
            onClick={() => setFilterType('all')}
            className={`px-2.5 py-1 rounded-md font-medium transition cursor-pointer ${
              filterType === 'all' ? 'bg-white text-slate-900 shadow-2xs font-semibold' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            All Events
          </button>
          <button
            onClick={() => setFilterType('Prescription')}
            className={`px-2.5 py-1 rounded-md font-medium transition cursor-pointer ${
              filterType === 'Prescription' ? 'bg-white text-blue-700 shadow-2xs font-semibold' : 'text-slate-600 hover:text-blue-700'
            }`}
          >
            Prescriptions
          </button>
          <button
            onClick={() => setFilterType('Laboratory')}
            className={`px-2.5 py-1 rounded-md font-medium transition cursor-pointer ${
              filterType === 'Laboratory' ? 'bg-white text-teal-700 shadow-2xs font-semibold' : 'text-slate-600 hover:text-teal-700'
            }`}
          >
            Labs
          </button>
          <button
            onClick={() => setFilterType('Discharge')}
            className={`px-2.5 py-1 rounded-md font-medium transition cursor-pointer ${
              filterType === 'Discharge' ? 'bg-white text-indigo-700 shadow-2xs font-semibold' : 'text-slate-600 hover:text-indigo-700'
            }`}
          >
            Discharges
          </button>
        </div>
      </div>

      {/* Timeline View */}
      {filteredEvents.length === 0 ? (
        <div className="text-center py-12 bg-slate-50/50 rounded-xl border border-dashed border-slate-200 mt-6">
          <Calendar className="w-10 h-10 text-slate-300 mx-auto mb-2" />
          <h3 className="text-sm font-semibold text-slate-700">No Timeline Events Recorded</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Upload documents or load Demo Mode to automatically assemble your chronological health story.
          </p>
        </div>
      ) : (
        <div className="mt-8 relative pl-6 sm:pl-8 border-l-2 border-teal-200 space-y-8">
          {filteredEvents.map((item, idx) => {
            const isExpanded = expandedId === item.id;
            const details = item.details || {};
            const medications = details.medications || [];
            const labResults = details.lab_results || [];
            const diagnoses = details.diagnoses || [];
            const procedures = details.procedures || [];

            return (
              <div key={item.id || idx} className="relative group">
                {/* Node circle on timeline line */}
                <div className="absolute -left-[31px] sm:-left-[39px] top-1.5 w-5 h-5 rounded-full bg-white border-4 border-teal-600 group-hover:scale-125 transition-transform shadow-xs" />

                {/* Event Card */}
                <div 
                  className={`bg-white rounded-xl border transition-all ${
                    isExpanded 
                      ? 'border-teal-400 shadow-md ring-2 ring-teal-100' 
                      : 'border-slate-200 hover:border-teal-300 hover:shadow-xs'
                  }`}
                >
                  <div 
                    onClick={() => toggleExpand(item.id)}
                    className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between cursor-pointer gap-3 select-none"
                  >
                    <div className="flex items-start sm:items-center space-x-3">
                      <div className="w-10 h-10 rounded-lg bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-700 shrink-0">
                        {item.category?.includes('Prescription') ? (
                          <Pill className="w-5 h-5 text-blue-600" />
                        ) : item.category?.includes('Lab') ? (
                          <Activity className="w-5 h-5 text-teal-600" />
                        ) : (
                          <FileText className="w-5 h-5 text-indigo-600" />
                        )}
                      </div>

                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-xs font-bold text-teal-800 bg-teal-50 px-2 py-0.5 rounded-md border border-teal-200 font-mono">
                            {item.event_date || '2026'}
                          </span>
                          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                            {item.category || 'Medical Record'}
                          </span>
                        </div>
                        <h3 className="text-sm font-bold text-slate-900 mt-1">{item.title}</h3>
                        <p className="text-xs text-slate-500 mt-0.5 line-clamp-1">{item.summary}</p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3 text-xs text-slate-500 self-end sm:self-center">
                      <span className="hidden md:inline font-mono text-[11px] bg-slate-50 px-2 py-1 rounded border border-slate-200">
                        {item.filename}
                      </span>
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-teal-600" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-slate-400" />
                      )}
                    </div>
                  </div>

                  {/* Expanded Event Details */}
                  {isExpanded && (
                    <div className="px-5 pb-5 pt-2 border-t border-slate-100 bg-slate-50/40 rounded-b-xl space-y-4 text-xs animate-in fade-in duration-150">
                      
                      {/* Clinical Diagnoses */}
                      {diagnoses.length > 0 && (
                        <div>
                          <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider flex items-center space-x-1.5 mb-1.5">
                            <Stethoscope className="w-3.5 h-3.5 text-indigo-600" />
                            <span>Clinical Impression & Diagnoses:</span>
                          </span>
                          <div className="flex flex-wrap gap-1.5">
                            {diagnoses.map((d, dIdx) => (
                              <span key={dIdx} className="bg-indigo-50 text-indigo-800 border border-indigo-200 px-2.5 py-1 rounded-md font-medium text-xs">
                                {d.name}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Extracted Medications */}
                      {medications.length > 0 && (
                        <div>
                          <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider flex items-center space-x-1.5 mb-1.5">
                            <Pill className="w-3.5 h-3.5 text-blue-600" />
                            <span>Prescribed Medications ({medications.length}):</span>
                          </span>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {medications.map((m, mIdx) => (
                              <div key={mIdx} className="bg-white p-2.5 rounded-lg border border-slate-200 flex items-center justify-between">
                                <div>
                                  <strong className="text-slate-900">{m.name}</strong>
                                  <p className="text-[11px] text-slate-500">{m.dose} • {m.frequency}</p>
                                </div>
                                <span className="text-[10px] font-medium bg-blue-50 text-blue-700 px-2 py-0.5 rounded">
                                  {m.instructions || 'After food'}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Laboratory Tests */}
                      {labResults.length > 0 && (
                        <div>
                          <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider flex items-center space-x-1.5 mb-1.5">
                            <Activity className="w-3.5 h-3.5 text-teal-600" />
                            <span>Laboratory Measurements:</span>
                          </span>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {labResults.map((l, lIdx) => {
                              const isAbnormal = ['Below reference range', 'Above reference range', 'High', 'Low'].includes(l.status);
                              return (
                                <div key={lIdx} className="bg-white p-2.5 rounded-lg border border-slate-200 flex items-center justify-between">
                                  <div>
                                    <strong className="text-slate-800">{l.test_name}</strong>
                                    <p className="text-[11px] font-mono text-slate-600">{l.value} {l.unit} (Ref: {l.reference_range})</p>
                                  </div>
                                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                                    isAbnormal ? 'bg-amber-100 text-amber-800 border border-amber-200' : 'bg-emerald-100 text-emerald-800'
                                  }`}>
                                    {l.status}
                                  </span>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}

                      {/* Procedures */}
                      {procedures.length > 0 && (
                        <div>
                          <span className="font-bold text-slate-700 uppercase text-[10px] tracking-wider flex items-center space-x-1.5 mb-1.5">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                            <span>Procedures Documented:</span>
                          </span>
                          {procedures.map((p, pIdx) => (
                            <div key={pIdx} className="bg-emerald-50 text-emerald-900 border border-emerald-200 p-2.5 rounded-lg">
                              <strong>{p.procedure}</strong> — {p.hospital} ({p.date})
                            </div>
                          ))}
                        </div>
                      )}

                      {/* View Raw Document Button */}
                      {onSelectDocument && item.document_id && (
                        <div className="pt-2 flex justify-end">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              onSelectDocument(item.document_id);
                            }}
                            className="inline-flex items-center space-x-1.5 text-xs font-semibold text-teal-700 hover:text-teal-900 cursor-pointer"
                          >
                            <span>Inspect Full OCR & Document View</span>
                            <ExternalLink className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      )}

                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
