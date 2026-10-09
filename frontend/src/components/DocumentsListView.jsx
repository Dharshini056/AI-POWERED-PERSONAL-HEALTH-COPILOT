import React from 'react';
import { 
  FileText, 
  Eye, 
  CheckCircle, 
  AlertTriangle, 
  Languages, 
  Calendar, 
  Download,
  FileCheck,
  FileSpreadsheet
} from 'lucide-react';

export default function DocumentsListView({ documents, onViewOCR, onUploadNew }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 tracking-tight flex items-center space-x-2">
            <FileText className="w-5 h-5 text-teal-600" />
            <span>Document Repository & OCR Index</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Browse all ingested prescriptions, lab panels, and discharge notes with verified OCR confidence metrics.
          </p>
        </div>

        <button
          onClick={onUploadNew}
          className="bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold px-4 py-2 rounded-lg transition shadow-2xs cursor-pointer"
        >
          + Upload Another Record
        </button>
      </div>

      {documents.length === 0 ? (
        <div className="text-center py-12 bg-slate-50/50 rounded-xl border border-dashed border-slate-200">
          <FileText className="w-10 h-10 text-slate-300 mx-auto mb-2" />
          <h3 className="text-sm font-semibold text-slate-700">No Documents Uploaded Yet</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Upload your first prescription or test report above, or click "Demo Mode" in the top bar.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {documents.map((doc) => {
            const confidence = doc.ocr_confidence ?? 0.95;
            const isLowConfidence = confidence < 0.70;

            return (
              <div
                key={doc.id}
                className="bg-white rounded-xl border border-slate-200 hover:border-teal-300 hover:shadow-md transition-all p-5 flex flex-col justify-between group"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[10px] font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded-md border border-teal-200 uppercase tracking-wider">
                      {doc.doc_type || 'Document'}
                    </span>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full flex items-center space-x-1 ${
                      confidence >= 0.85
                        ? 'bg-emerald-100 text-emerald-800'
                        : confidence >= 0.70
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-rose-100 text-rose-800'
                    }`}>
                      <span>OCR {Math.round(confidence * 100)}%</span>
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-slate-900 group-hover:text-teal-600 transition truncate" title={doc.filename}>
                    {doc.filename}
                  </h3>

                  <div className="mt-3 space-y-2 text-xs text-slate-600">
                    <div className="flex items-center justify-between pb-1.5 border-b border-slate-100">
                      <span className="text-slate-400">Language Detected:</span>
                      <strong className="text-slate-800">{doc.detected_language || 'English'}</strong>
                    </div>

                    <div className="flex items-center justify-between pb-1.5 border-b border-slate-100">
                      <span className="text-slate-400">Engine / Method:</span>
                      <span className="font-mono text-[11px] text-slate-700">RapidOCR PaddleONNX</span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Date Uploaded:</span>
                      <span className="text-slate-600 font-mono text-[11px]">{doc.created_at?.split(' ')[0] || '2026-08-12'}</span>
                    </div>
                  </div>

                  {isLowConfidence && (
                    <div className="mt-3 p-2 bg-amber-50 rounded-lg text-amber-800 text-[11px] flex items-center space-x-1 border border-amber-200">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      <span>Low confidence OCR. Verify against original.</span>
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                  <button
                    onClick={() => onViewOCR(doc)}
                    className="w-full flex items-center justify-center space-x-1.5 bg-slate-50 hover:bg-teal-50 hover:text-teal-700 text-slate-700 text-xs font-semibold py-2 rounded-lg border border-slate-200 hover:border-teal-300 transition cursor-pointer"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>View OCR & Compare Document</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
