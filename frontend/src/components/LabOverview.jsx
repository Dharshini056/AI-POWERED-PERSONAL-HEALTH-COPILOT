import React, { useState } from 'react';
import { 
  Activity, 
  AlertTriangle, 
  CheckCircle, 
  HelpCircle, 
  FileText, 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Sparkles,
  Info
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid, 
  Cell 
} from 'recharts';

export default function LabOverview({ labResults, selectedLanguage = 'English' }) {
  const [filter, setFilter] = useState('all'); // 'all', 'abnormal', 'normal'

  const filteredLabs = (labResults || []).filter((lab) => {
    const isAbnormal = ['Below reference range', 'Above reference range', 'High', 'Low', 'Critical'].includes(lab.status);
    if (filter === 'abnormal') return isAbnormal;
    if (filter === 'normal') return !isAbnormal;
    return true;
  });

  const abnormalCount = (labResults || []).filter((l) =>
    ['Below reference range', 'Above reference range', 'High', 'Low', 'Critical'].includes(l.status)
  ).length;

  // Chart data formatting for numeric lab values
  const chartData = (labResults || [])
    .filter((l) => !isNaN(parseFloat(l.value)) && parseFloat(l.value) < 1000)
    .slice(0, 6)
    .map((l) => ({
      name: l.test_name.length > 14 ? l.test_name.substring(0, 12) + '...' : l.test_name,
      fullName: l.test_name,
      value: parseFloat(l.value),
      unit: l.unit || '',
      status: l.status,
      isAbnormal: ['Below reference range', 'Above reference range', 'High', 'Low'].includes(l.status),
    }));

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 tracking-tight flex items-center space-x-2">
            <Activity className="w-5 h-5 text-teal-600" />
            <span>Laboratory Results & Reference Range Analysis</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Biochemical values evaluated against laboratory reference intervals with non-diagnostic AI explanations.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-lg text-xs">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-md font-medium transition cursor-pointer ${
              filter === 'all' ? 'bg-white text-slate-900 shadow-2xs font-semibold' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            All Tests ({labResults?.length || 0})
          </button>
          <button
            onClick={() => setFilter('abnormal')}
            className={`px-3 py-1 rounded-md font-medium transition flex items-center space-x-1 cursor-pointer ${
              filter === 'abnormal' ? 'bg-amber-500 text-white shadow-2xs font-semibold' : 'text-slate-600 hover:text-amber-700'
            }`}
          >
            <AlertTriangle className="w-3 h-3" />
            <span>Out of Range ({abnormalCount})</span>
          </button>
          <button
            onClick={() => setFilter('normal')}
            className={`px-3 py-1 rounded-md font-medium transition cursor-pointer ${
              filter === 'normal' ? 'bg-white text-emerald-700 shadow-2xs font-semibold' : 'text-slate-600 hover:text-emerald-700'
            }`}
          >
            Normal ({(labResults?.length || 0) - abnormalCount})
          </button>
        </div>
      </div>

      {/* Safety Phrasing Banner (Mandatory Prompt Section 7 & 19) */}
      <div className="p-3.5 rounded-xl bg-sky-50 border border-sky-200 text-sky-950 text-xs flex items-start space-x-3">
        <Info className="w-5 h-5 text-sky-600 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <strong>Clinical Communication Rule:</strong> This value is outside the reference range shown in the report. 
          There can be several reasons for this result, and a healthcare professional should interpret it in context. 
          The Copilot strictly does not diagnose diseases or formulate treatment plans from a single lab test.
        </div>
      </div>

      {/* Recharts Visual Bar Graphic */}
      {chartData.length > 0 && (
        <div className="bg-slate-50/70 border border-slate-200 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
              <TrendingUp className="w-3.5 h-3.5 text-teal-600" />
              <span>Biochemical Value Overview</span>
            </span>
            <span className="text-[11px] text-slate-400">Values with units</span>
          </div>
          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} interval={0} />
                <YAxis tick={{ fontSize: 10, fill: '#64748b' }} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-slate-900 text-white p-2.5 rounded-lg text-xs shadow-lg">
                          <p className="font-bold">{data.fullName}</p>
                          <p className="text-teal-300 font-mono mt-0.5">
                            {data.value} {data.unit}
                          </p>
                          <p className={`text-[10px] mt-1 font-semibold ${data.isAbnormal ? 'text-amber-400' : 'text-emerald-400'}`}>
                            Status: {data.status}
                          </p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={entry.isAbnormal ? '#f59e0b' : '#0d9488'} 
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Grid of Lab Result Explanations */}
      {filteredLabs.length === 0 ? (
        <div className="text-center py-12 bg-slate-50/50 rounded-xl border border-dashed border-slate-200">
          <Activity className="w-10 h-10 text-slate-300 mx-auto mb-2" />
          <h3 className="text-sm font-semibold text-slate-700">No Lab Tests Found</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Upload a laboratory report or click "Demo Mode" to inspect preloaded blood panels.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredLabs.map((lab, idx) => {
            const isAbnormal = ['Below reference range', 'Above reference range', 'High', 'Low', 'Critical'].includes(lab.status);
            const isLow = lab.status?.toLowerCase().includes('below') || lab.status?.toLowerCase().includes('low');
            const explanation = (selectedLanguage === 'Tamil' && lab.explanation_ta) ? lab.explanation_ta : lab.explanation;

            return (
              <div
                key={idx}
                className={`rounded-xl border p-5 transition-all ${
                  isAbnormal
                    ? 'bg-amber-50/30 border-amber-200 hover:border-amber-300 hover:shadow-md'
                    : 'bg-white border-slate-200 hover:border-teal-300 hover:shadow-sm'
                }`}
              >
                {/* Header row */}
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">{lab.test_name}</h3>
                    <p className="text-[11px] text-slate-400 mt-0.5">Date: {lab.date || '18 Aug 2026'}</p>
                  </div>

                  <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full flex items-center space-x-1 ${
                    isAbnormal
                      ? 'bg-amber-100 text-amber-800 border border-amber-200'
                      : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                  }`}>
                    {isAbnormal ? (
                      isLow ? <TrendingDown className="w-3 h-3 text-amber-700" /> : <TrendingUp className="w-3 h-3 text-amber-700" />
                    ) : (
                      <CheckCircle className="w-3 h-3 text-emerald-700" />
                    )}
                    <span>{lab.status || 'Normal'}</span>
                  </span>
                </div>

                {/* Values row */}
                <div className="mt-4 flex items-baseline justify-between bg-white rounded-lg p-3 border border-slate-100">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-400">Measured Value</span>
                    <div className="text-xl font-bold text-slate-900 mt-0.5">
                      {lab.value} <span className="text-xs font-medium text-slate-500">{lab.unit}</span>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Reference Range</span>
                    <div className="text-xs font-semibold text-slate-700 mt-0.5 font-mono">
                      {lab.reference_range || 'Standard'}
                    </div>
                  </div>
                </div>

                {/* Non-Diagnostic Simple-Language Explanation */}
                <div className="mt-3.5 pt-3 border-t border-slate-100 text-xs text-slate-600 leading-relaxed bg-slate-50/60 p-3 rounded-lg">
                  <div className="flex items-center space-x-1.5 text-teal-800 font-semibold mb-1">
                    <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                    <span>AI Educational Insight ({selectedLanguage === 'Tamil' ? 'தமிழ் விளக்கம்' : 'Simple Language'}):</span>
                  </div>
                  <p className="text-[11px] text-slate-700">
                    {explanation || `This value is recorded in your report. Discuss with your doctor for clinical correlation.`}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
