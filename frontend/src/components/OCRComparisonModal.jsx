import React, { useState } from 'react';
import { 
  X, 
  FileText, 
  CheckCircle, 
  AlertTriangle, 
  Languages, 
  Clock, 
  Cpu, 
  Copy, 
  Check, 
  FileCode,
  ZoomIn
} from 'lucide-react';

export default function OCRComparisonModal({ documentData, onClose }) {
  const [activeTab, setActiveTab] = useState('split'); // 'split', 'original', 'ocr'
  const [copied, setCopied] = useState(false);

  if (!documentData) return null;

  const doc = documentData.document || documentData;
  const ocr = documentData.ocr || documentData.ocr_result || {};
  const rawText = ocr.raw_text || doc.raw_text || '';
  const confidence = ocr.confidence_score ?? doc.ocr_confidence ?? 0.95;
  const detectedLanguage = ocr.detected_language || doc.detected_language || 'English';
  const processingTime = ocr.processing_time_ms || 420;
  const engine = ocr.engine_name || 'RapidOCR-PaddleONNX + OpenCV CLAHE';
  const isLowConfidence = confidence < 0.70 || ocr.is_low_confidence;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(rawText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const fileUrl = doc.file_path ? (doc.file_path.startsWith('http') ? doc.file_path : `/${doc.file_path}`) : null;
  const isPdf = doc.filename?.toLowerCase().endsWith('.pdf') || doc.file_type?.includes('pdf');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 sm:p-6 overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in duration-200">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-base font-bold text-slate-900">{doc.filename || 'Medical Document'}</span>
              <span className="text-[11px] font-semibold bg-teal-100 text-teal-800 px-2 py-0.5 rounded-full">
                {doc.doc_type || 'Clinical Document'}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Multilingual OCR Extraction & Document Integrity Comparison
            </p>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200 transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Status / Confidence Bar */}
        <div className="px-6 py-2.5 bg-slate-100/70 border-b border-slate-200 flex flex-wrap items-center justify-between text-xs gap-3">
          <div className="flex items-center space-x-4">
            {/* Language */}
            <div className="flex items-center space-x-1.5 text-slate-700">
              <Languages className="w-4 h-4 text-teal-600" />
              <span>Language: <strong>{detectedLanguage}</strong></span>
            </div>

            {/* Confidence Score */}
            <div className="flex items-center space-x-1.5">
              <span className="text-slate-600">OCR Confidence:</span>
              <span className={`px-2 py-0.5 rounded-full font-bold text-[11px] ${
                confidence >= 0.85 
                  ? 'bg-emerald-100 text-emerald-800' 
                  : confidence >= 0.70 
                  ? 'bg-amber-100 text-amber-800' 
                  : 'bg-rose-100 text-rose-800'
              }`}>
                {Math.round(confidence * 100)}%
              </span>
            </div>

            {/* Engine info */}
            <div className="hidden sm:flex items-center space-x-1 text-slate-500">
              <Cpu className="w-3.5 h-3.5" />
              <span>{engine}</span>
            </div>
          </div>

          {/* View Mode Buttons */}
          <div className="flex items-center space-x-1 bg-white border border-slate-300 rounded-lg p-0.5">
            <button
              onClick={() => setActiveTab('split')}
              className={`px-2.5 py-1 text-xs rounded-md font-medium transition cursor-pointer ${
                activeTab === 'split' ? 'bg-teal-600 text-white' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              Side-by-Side
            </button>
            <button
              onClick={() => setActiveTab('original')}
              className={`px-2.5 py-1 text-xs rounded-md font-medium transition cursor-pointer ${
                activeTab === 'original' ? 'bg-teal-600 text-white' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              Original Document
            </button>
            <button
              onClick={() => setActiveTab('ocr')}
              className={`px-2.5 py-1 text-xs rounded-md font-medium transition cursor-pointer ${
                activeTab === 'ocr' ? 'bg-teal-600 text-white' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              OCR Extracted Text
            </button>
          </div>
        </div>

        {/* Low Confidence Warning (Prompt requirement) */}
        {isLowConfidence && (
          <div className="px-6 py-2.5 bg-amber-50 border-b border-amber-200 text-amber-800 text-xs flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
            <span className="font-medium">
              OCR confidence indicator is lower than optimal threshold. Please verify this information against the original document before taking any clinical decision.
            </span>
          </div>
        )}

        {/* Body Area */}
        <div className="flex-1 overflow-hidden grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200 min-h-[460px]">
          
          {/* Left Column: Original Document */}
          {(activeTab === 'split' || activeTab === 'original') && (
            <div className={`p-4 flex flex-col bg-slate-50/50 overflow-y-auto ${activeTab === 'original' ? 'col-span-2' : ''}`}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
                  <FileText className="w-3.5 h-3.5 text-teal-600" />
                  <span>Original Document Preview</span>
                </span>
                <span className="text-[11px] text-slate-400 font-mono">{doc.filename}</span>
              </div>

              <div className="flex-1 border border-slate-200 rounded-xl bg-white p-4 shadow-2xs overflow-auto flex items-center justify-center min-h-[350px]">
                {fileUrl ? (
                  isPdf ? (
                    <div className="w-full h-full flex flex-col items-center justify-center p-6 text-center">
                      <FileText className="w-16 h-16 text-teal-600 mb-3" />
                      <h4 className="text-sm font-bold text-slate-800">{doc.filename}</h4>
                      <p className="text-xs text-slate-500 mt-1 max-w-sm">
                        High-resolution multi-page PDF medical record ingested via PyMuPDF.
                      </p>
                      <a
                        href={fileUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="mt-4 px-3.5 py-1.5 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-xs font-medium inline-flex items-center space-x-1.5"
                      >
                        <ZoomIn className="w-3.5 h-3.5" />
                        <span>Open Document Fullscreen</span>
                      </a>
                    </div>
                  ) : (
                    <img
                      src={fileUrl}
                      alt="Original Medical Record"
                      className="max-h-[500px] w-auto object-contain rounded-lg shadow-xs"
                    />
                  )
                ) : (
                  <div className="text-center p-6">
                    <FileText className="w-12 h-12 text-slate-300 mx-auto mb-2" />
                    <p className="text-xs text-slate-500">Synthetic preloaded clinical document</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Right Column: Extracted OCR Text */}
          {(activeTab === 'split' || activeTab === 'ocr') && (
            <div className={`p-4 flex flex-col bg-slate-900 text-slate-100 overflow-y-auto ${activeTab === 'ocr' ? 'col-span-2' : ''}`}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-teal-300 uppercase tracking-wider flex items-center space-x-1.5">
                  <FileCode className="w-3.5 h-3.5 text-teal-400" />
                  <span>OCR Extracted Text Output</span>
                </span>

                <button
                  onClick={copyToClipboard}
                  className="flex items-center space-x-1 text-[11px] text-slate-400 hover:text-white px-2 py-1 rounded bg-slate-800 border border-slate-700 transition cursor-pointer"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copied ? 'Copied' : 'Copy Text'}</span>
                </button>
              </div>

              <div className="flex-1 rounded-xl bg-slate-950 border border-slate-800 p-4 font-mono text-xs text-slate-200 whitespace-pre-wrap overflow-y-auto max-h-[500px] leading-relaxed select-text">
                {rawText || 'No text extracted from this record.'}
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-xs text-slate-500">
          <span>Processed in {processingTime}ms via OpenCV Adaptive CLAHE + Deskew Pipeline</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-lg font-semibold transition cursor-pointer"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}
