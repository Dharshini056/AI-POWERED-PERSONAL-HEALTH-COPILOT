import React, { useState } from 'react';
import { 
  Pill, 
  Clock, 
  Calendar, 
  AlertTriangle, 
  Utensils, 
  FileCheck, 
  Search,
  ShieldAlert
} from 'lucide-react';

export default function MedicationCards({ medications, selectedLanguage = 'English' }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredMeds = (medications || []).filter((m) =>
    m.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.instructions?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 tracking-tight flex items-center space-x-2">
            <Pill className="w-5 h-5 text-blue-600" />
            <span>Medication Summary & Orders</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Prescription dosages, frequencies, and instructions extracted from uploaded clinical records.
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search medications..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-hidden focus:border-blue-500 focus:bg-white"
          />
        </div>
      </div>

      {/* Mandatory Safety Warning (Prompt Section 8 & 19) */}
      <div className="my-5 p-3.5 rounded-xl bg-amber-50/80 border border-amber-200 text-amber-900 text-xs flex items-start space-x-3">
        <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-0.5">
          <p className="font-bold text-amber-950">Safety Guidance & Clinical Verification Notice</p>
          <p className="text-amber-800 leading-relaxed">
            Verify medication name, dose, and instructions against the original prescription before taking or changing any medication. 
            This AI assistant does not recommend starting, stopping, or altering medications. Always consult your prescribing physician.
          </p>
        </div>
      </div>

      {/* Grid of Medication Cards */}
      {filteredMeds.length === 0 ? (
        <div className="text-center py-12 bg-slate-50/50 rounded-xl border border-dashed border-slate-200">
          <Pill className="w-10 h-10 text-slate-300 mx-auto mb-2" />
          <h3 className="text-sm font-semibold text-slate-700">No Medications Extracted Yet</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Upload a prescription or discharge summary, or click "Demo Mode" in the top bar to inspect preloaded medications.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredMeds.map((med, idx) => (
            <div
              key={idx}
              className="bg-white rounded-xl border border-slate-200 hover:border-blue-300 hover:shadow-md transition-all p-5 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[10px] font-bold text-blue-700 uppercase tracking-widest bg-blue-50 px-2 py-0.5 rounded-md border border-blue-200">
                    Medication
                  </span>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                    {med.route || 'Oral'}
                  </span>
                </div>

                <h3 className="text-base font-bold text-slate-900 group-hover:text-blue-600 transition">
                  {med.name}
                </h3>

                <div className="mt-3 space-y-2 text-xs">
                  {/* Dose */}
                  <div className="flex items-center justify-between text-slate-600 pb-1.5 border-b border-slate-100">
                    <span className="text-slate-400">Dose / Strength:</span>
                    <strong className="text-slate-800 text-sm font-bold">{med.dose || 'Standard'}</strong>
                  </div>

                  {/* Frequency */}
                  <div className="flex items-center justify-between text-slate-600 pb-1.5 border-b border-slate-100">
                    <span className="text-slate-400 flex items-center space-x-1">
                      <Clock className="w-3.5 h-3.5 text-blue-500 mr-1" />
                      <span>Frequency:</span>
                    </span>
                    <span className="font-semibold text-slate-800">{med.frequency || 'Once daily'}</span>
                  </div>

                  {/* Duration */}
                  <div className="flex items-center justify-between text-slate-600 pb-1.5 border-b border-slate-100">
                    <span className="text-slate-400 flex items-center space-x-1">
                      <Calendar className="w-3.5 h-3.5 text-emerald-500 mr-1" />
                      <span>Duration:</span>
                    </span>
                    <span className="font-semibold text-slate-800">{med.duration || 'As prescribed'}</span>
                  </div>

                  {/* Food Instructions */}
                  <div className="flex items-center justify-between text-slate-600 pt-0.5">
                    <span className="text-slate-400 flex items-center space-x-1">
                      <Utensils className="w-3.5 h-3.5 text-amber-500 mr-1" />
                      <span>Meal Timing:</span>
                    </span>
                    <span className="font-semibold text-teal-700 bg-teal-50 px-2 py-0.5 rounded-md border border-teal-200 text-[11px]">
                      {med.instructions || med.before_after_food || 'After food'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Source Document Tag */}
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                <span className="truncate max-w-[200px]">
                  Source: <strong>{med.source_document || 'Prescription Document'}</strong>
                </span>
                <FileCheck className="w-3.5 h-3.5 text-emerald-500" />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
