import React from 'react';
import { 
  FileText, 
  Pill, 
  Activity, 
  Stethoscope, 
  Calendar, 
  AlertTriangle,
  ArrowUpRight 
} from 'lucide-react';

export default function OverviewCards({ stats, onNavigate }) {
  const cards = [
    {
      id: 'upload',
      title: 'Uploaded Documents',
      count: stats?.total_documents ?? 0,
      subtitle: 'Prescriptions, Labs & Summaries',
      icon: FileText,
      color: 'teal',
      badge: 'Multilingual OCR',
      badgeColor: 'bg-teal-50 text-teal-700 border-teal-200',
    },
    {
      id: 'medications',
      title: 'Active Medications',
      count: stats?.total_medications ?? 0,
      subtitle: 'Parsed dosages & food timings',
      icon: Pill,
      color: 'blue',
      badge: 'Verified Orders',
      badgeColor: 'bg-blue-50 text-blue-700 border-blue-200',
    },
    {
      id: 'labs',
      title: 'Laboratory Tests',
      count: stats?.total_lab_tests ?? 0,
      subtitle: `${stats?.abnormal_lab_tests ?? 0} outside reference range`,
      icon: Activity,
      color: 'amber',
      badge: stats?.abnormal_lab_tests ? `${stats.abnormal_lab_tests} Out of Range` : 'All Normal',
      badgeColor: stats?.abnormal_lab_tests ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200',
      hasAlert: Boolean(stats?.abnormal_lab_tests),
    },
    {
      id: 'timeline',
      title: 'Documented Diagnoses',
      count: stats?.total_diagnoses ?? 0,
      subtitle: 'Clinical conditions recorded',
      icon: Stethoscope,
      color: 'indigo',
      badge: 'Clinical Records',
      badgeColor: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    },
    {
      id: 'timeline',
      title: 'Health Events',
      count: stats?.total_events ?? 0,
      subtitle: 'Chronological timeline entries',
      icon: Calendar,
      color: 'emerald',
      badge: 'Timeline Synced',
      badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
      {cards.map((c) => {
        const Icon = c.icon;
        return (
          <div
            key={c.title}
            onClick={() => onNavigate && onNavigate(c.id)}
            className="bg-white rounded-xl border border-slate-200 p-4.5 hover:shadow-md hover:border-teal-300 transition-all cursor-pointer group relative overflow-hidden"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-700 group-hover:bg-teal-50 group-hover:text-teal-600 transition">
                <Icon className="w-5 h-5" />
              </div>
              <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${c.badgeColor} flex items-center space-x-1`}>
                {c.hasAlert && <AlertTriangle className="w-3 h-3 mr-0.5 text-amber-600 inline" />}
                <span>{c.badge}</span>
              </span>
            </div>

            <div>
              <div className="text-2xl font-bold text-slate-900 tracking-tight flex items-baseline justify-between">
                <span>{c.count}</span>
                <ArrowUpRight className="w-4 h-4 text-slate-300 group-hover:text-teal-600 transition" />
              </div>
              <h3 className="text-xs font-semibold text-slate-700 mt-1">{c.title}</h3>
              <p className="text-[11px] text-slate-400 mt-0.5">{c.subtitle}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
