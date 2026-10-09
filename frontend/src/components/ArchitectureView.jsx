import React from 'react';
import { 
  Layers, 
  Upload, 
  Cpu, 
  Globe2, 
  FileCheck2, 
  Sparkles, 
  Database, 
  ShieldCheck, 
  ArrowDown, 
  ArrowRight,
  Code,
  Terminal,
  CheckCircle2
} from 'lucide-react';

export default function ArchitectureView() {
  const pipelineSteps = [
    {
      num: "01",
      title: "User / Web Application",
      tech: "React 19 • Vite • Tailwind CSS • Recharts",
      desc: "Responsive patient portal with drag-and-drop document upload, multilingual selector (English, Tamil, Hindi, Telugu, Malayalam, Kannada), and 1-Click Demo Mode."
    },
    {
      num: "02",
      title: "Document Ingestion & Routing",
      tech: "FastAPI • PyMuPDF (fitz) • OpenCV (CLAHE / Deskew)",
      desc: "Multi-format ingestion (PDF, Scanned PDF, JPG, PNG). Detects digital selectable text vs scanned image. Preprocesses raster images with bilateral filtering and contrast enhancement."
    },
    {
      num: "03",
      title: "Multilingual OCR Engine",
      tech: "RapidOCR (PaddleOCR ONNX) • OpenCV Deskew",
      desc: "Extracts text from English, Tamil, and bilingual prescriptions. Computes OCR confidence score and flags low-confidence documents with verification alerts."
    },
    {
      num: "04",
      title: "Language & Script Detection",
      tech: "Unicode Block NLP • Regex Analyzer",
      desc: "Distinguishes English, Tamil, and bilingual (English + Tamil) scripts for tailored linguistic processing."
    },
    {
      num: "05",
      title: "Medical Entity Extraction",
      tech: "OpenAI GPT-4o-mini + Offline Medical NLP Rules Engine",
      desc: "Parses patient demographics, clinical diagnoses, medications (dose, frequency, route, duration, food timing), and laboratory test values into structured JSON."
    },
    {
      num: "06",
      title: "Reference Range & Safety Analysis",
      tech: "Standard Biochemical Bounds Engine",
      desc: "Compares lab results with normal reference intervals. Flags values above or below range with non-diagnostic educational explanations."
    },
    {
      num: "07",
      title: "AI Health Intelligence & Multilingual Output",
      tech: "Summary Generator • Tamil/Indic Translation Engine",
      desc: "Produces plain-language summaries in English and Tamil. Generates safe medication warnings and builds the unified chronological health timeline."
    },
    {
      num: "08",
      title: "Relational Persistence & FHIR / ABDM Standardization",
      tech: "SQLite 3 • HL7 FHIR R4 Bundles • Mock ABHA ID",
      desc: "Stores structured data in relational database tables. Exports standardized FHIR R4 resources (Patient, DocumentReference, Condition, MedicationRequest, Observation, Encounter)."
    }
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 sm:p-8 space-y-8">
      {/* Header */}
      <div className="pb-5 border-b border-slate-100">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center space-x-2">
          <Layers className="w-6 h-6 text-teal-600" />
          <span>System Architecture & End-to-End Processing Pipeline</span>
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Detailed technical architecture showing the ingestion, OCR, NLP extraction, safety guardrails, and ABDM standardization layers.
        </p>
      </div>

      {/* Visual Pipeline Flowchart */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-xl overflow-x-auto">
        <div className="text-center mb-6">
          <span className="text-xs font-mono font-bold text-teal-400 bg-teal-950 px-3 py-1 rounded-full border border-teal-800">
            SYSTEM DATAFLOW DIAGRAM
          </span>
        </div>

        <div className="max-w-3xl mx-auto space-y-4 text-xs font-mono">
          
          {/* Level 1 */}
          <div className="p-3.5 bg-slate-800 rounded-xl border border-teal-500/40 text-center font-bold text-teal-300">
            USER / WEB CLIENT (React + Vite + Tailwind CSS)
          </div>

          <div className="flex justify-center text-teal-400">
            <ArrowDown className="w-4 h-4 animate-bounce" />
          </div>

          {/* Level 2 */}
          <div className="p-3.5 bg-slate-800 rounded-xl border border-slate-700 text-center font-bold text-white">
            FASTAPI ASYNCHRONOUS INGESTION (Validation, Size check, Storage)
          </div>

          <div className="flex justify-center text-teal-400">
            <ArrowDown className="w-4 h-4" />
          </div>

          {/* Level 3: Split */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-3 bg-slate-850 rounded-lg border border-slate-700 text-center">
              <span className="text-teal-400 font-bold">DIGITAL PDF</span>
              <p className="text-[11px] text-slate-400 mt-1">Direct text extraction via PyMuPDF</p>
            </div>
            <div className="p-3 bg-slate-850 rounded-lg border border-slate-700 text-center">
              <span className="text-teal-400 font-bold">SCANNED / IMAGE</span>
              <p className="text-[11px] text-slate-400 mt-1">OpenCV CLAHE + Deskew + RapidOCR (PaddleONNX)</p>
            </div>
          </div>

          <div className="flex justify-center text-teal-400">
            <ArrowDown className="w-4 h-4" />
          </div>

          {/* Level 4 */}
          <div className="p-3.5 bg-slate-800 rounded-xl border border-slate-700 text-center font-bold text-white">
            MULTILINGUAL LANGUAGE & SCRIPT DETECTION (English, Tamil, Bilingual)
          </div>

          <div className="flex justify-center text-teal-400">
            <ArrowDown className="w-4 h-4" />
          </div>

          {/* Level 5 */}
          <div className="p-3.5 bg-teal-950/80 rounded-xl border border-teal-700 text-center font-bold text-teal-300">
            MEDICAL INFORMATION EXTRACTION (GPT-4o-mini + Deterministic Medical NLP)
          </div>

          <div className="flex justify-center text-teal-400">
            <ArrowDown className="w-4 h-4" />
          </div>

          {/* Level 6: Split branches */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-center text-[11px]">
            <div className="p-2.5 bg-slate-800 rounded-lg border border-slate-700">
              <strong className="text-teal-300 block">AI Summary & Explanations</strong>
              <span>Non-diagnostic, safe medical wording</span>
            </div>
            <div className="p-2.5 bg-slate-800 rounded-lg border border-slate-700">
              <strong className="text-teal-300 block">Unified Health Timeline</strong>
              <span>Chronological patient history</span>
            </div>
            <div className="p-2.5 bg-slate-800 rounded-lg border border-slate-700">
              <strong className="text-teal-300 block">Multilingual Output</strong>
              <span>English & Tamil presentation</span>
            </div>
          </div>

          <div className="flex justify-center text-teal-400">
            <ArrowDown className="w-4 h-4" />
          </div>

          {/* Level 7: Final ABDM/FHIR */}
          <div className="p-3.5 bg-gradient-to-r from-teal-900 to-emerald-900 rounded-xl border border-teal-500 text-center font-bold text-white">
            HEALTH PROFILE & FHIR R4 / ABDM DATA STANDARDIZATION
          </div>

        </div>
      </div>

      {/* Step by Step Breakdown Cards */}
      <div className="space-y-4">
        <h3 className="text-base font-bold text-slate-900">Architecture Components & Technology Stack</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {pipelineSteps.map((step) => (
            <div key={step.num} className="bg-slate-50 border border-slate-200 rounded-xl p-4.5 hover:border-teal-300 transition">
              <div className="flex items-center space-x-2.5 mb-2">
                <span className="w-7 h-7 rounded-lg bg-teal-600 text-white font-mono font-bold text-xs flex items-center justify-center shrink-0">
                  {step.num}
                </span>
                <div>
                  <h4 className="text-sm font-bold text-slate-900">{step.title}</h4>
                  <span className="text-[10px] font-mono font-semibold text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                    {step.tech}
                  </span>
                </div>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed mt-2 pl-9.5">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
