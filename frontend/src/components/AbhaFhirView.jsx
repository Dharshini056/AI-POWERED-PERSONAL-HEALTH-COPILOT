import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  QrCode, 
  Copy, 
  Check, 
  Database, 
  FileCode, 
  Network, 
  CheckCircle2, 
  ExternalLink,
  Layers,
  ArrowRight
} from 'lucide-react';
import { fetchAbhaProfile } from '../services/api';

export default function AbhaFhirView() {
  const [abhaData, setAbhaData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [activeSubTab, setActiveSubTab] = useState('mapping'); // 'mapping', 'json'

  useEffect(() => {
    loadAbha();
  }, []);

  const loadAbha = async () => {
    try {
      const data = await fetchAbhaProfile();
      setAbhaData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const copyJson = () => {
    if (!abhaData?.fhir?.bundle) return;
    navigator.clipboard.writeText(JSON.stringify(abhaData.fhir.bundle, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
        <ShieldCheck className="w-10 h-10 text-teal-600 animate-pulse mx-auto mb-3" />
        <p className="text-xs text-slate-500">Loading ABDM / FHIR R4 Health Architecture...</p>
      </div>
    );
  }

  const abha = abhaData?.abha || {};
  const fhir = abhaData?.fhir || {};
  const mappings = fhir.mappings || [];
  const resourceCounts = fhir.resource_counts || {};

  return (
    <div className="space-y-6">
      
      {/* ABHA Mock Digital ID Card */}
      <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 text-white rounded-2xl p-6 shadow-md border border-teal-700/50 relative overflow-hidden">
        {/* Background decorative watermark */}
        <div className="absolute right-0 bottom-0 opacity-10 pointer-events-none transform translate-x-10 translate-y-10">
          <ShieldCheck className="w-80 h-80" />
        </div>

        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <span className="bg-emerald-500/20 text-emerald-300 text-[11px] font-bold px-3 py-1 rounded-full border border-emerald-400/30 flex items-center space-x-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>DEMO / MOCK ABHA PROFILE (Sandbox Mode)</span>
              </span>
              <span className="text-xs text-teal-200">National Health Authority (NHA) Sandbox Standard</span>
            </div>

            <div>
              <p className="text-xs text-teal-200 font-medium">Ayushman Bharat Health Account (ABHA)</p>
              <h1 className="text-2xl sm:text-3xl font-mono font-bold tracking-wider text-white mt-0.5">
                {abha.abha_number || '91-4521-8934-1022'}
              </h1>
              <p className="text-xs font-mono text-teal-300 mt-1">
                ABHA Address: <strong>{abha.abha_address || 'arunkumar@sbx'}</strong>
              </p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2 text-xs">
              <div>
                <span className="text-teal-300 text-[10px] uppercase font-semibold">Full Name</span>
                <p className="font-bold text-white">{abha.full_name || 'Arun Kumar'}</p>
              </div>
              <div>
                <span className="text-teal-300 text-[10px] uppercase font-semibold">Gender & Age</span>
                <p className="font-bold text-white">{abha.gender}, 42 Y</p>
              </div>
              <div>
                <span className="text-teal-300 text-[10px] uppercase font-semibold">Date of Birth</span>
                <p className="font-bold text-white">{abha.date_of_birth || '1984-05-14'}</p>
              </div>
              <div>
                <span className="text-teal-300 text-[10px] uppercase font-semibold">State / Region</span>
                <p className="font-bold text-white">{abha.district}, {abha.state}</p>
              </div>
            </div>
          </div>

          {/* Mock QR Code Card */}
          <div className="bg-white text-slate-900 rounded-xl p-3.5 shadow-lg flex flex-col items-center shrink-0 border border-teal-200/50">
            <div className="w-28 h-28 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-center p-1">
              <QrCode className="w-24 h-24 text-slate-800" />
            </div>
            <span className="text-[10px] font-mono text-slate-500 mt-1.5 font-bold">MOCK SCAN QR</span>
            <span className="text-[9px] text-teal-700 bg-teal-50 px-1.5 py-0.5 rounded font-semibold mt-0.5">
              ABDM Sandbox
            </span>
          </div>
        </div>
      </div>

      {/* FHIR R4 Resource Mapping Section */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-100 gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900 tracking-tight flex items-center space-x-2">
              <Database className="w-5 h-5 text-teal-600" />
              <span>FHIR R4 & ABDM Standard Data Transformation</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Every document ingested via Multilingual OCR is normalized into interoperable HL7 FHIR R4 clinical resources.
            </p>
          </div>

          {/* Sub Tabs */}
          <div className="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-lg text-xs">
            <button
              onClick={() => setActiveSubTab('mapping')}
              className={`px-3 py-1 rounded-md font-medium transition cursor-pointer ${
                activeSubTab === 'mapping' ? 'bg-white text-slate-900 shadow-2xs font-semibold' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Resource Mapping Table
            </button>
            <button
              onClick={() => setActiveSubTab('json')}
              className={`px-3 py-1 rounded-md font-medium transition flex items-center space-x-1 cursor-pointer ${
                activeSubTab === 'json' ? 'bg-white text-teal-700 shadow-2xs font-semibold' : 'text-slate-600 hover:text-teal-700'
              }`}
            >
              <FileCode className="w-3.5 h-3.5 mr-1" />
              <span>FHIR R4 Bundle JSON</span>
            </button>
          </div>
        </div>

        {/* Resource Counter Badges */}
        <div className="mt-5 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5">
          {Object.entries(resourceCounts).map(([resType, count]) => (
            <div key={resType} className="bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-center">
              <span className="text-[10px] uppercase font-bold text-slate-400 block truncate">{resType}</span>
              <span className="text-base font-bold text-teal-700 mt-0.5 block">{count}</span>
            </div>
          ))}
        </div>

        {/* Tab 1: Mapping Table */}
        {activeSubTab === 'mapping' && (
          <div className="mt-6 overflow-x-auto border border-slate-200 rounded-xl">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                  <th className="py-3 px-4">Medical Document Element</th>
                  <th className="py-3 px-4">Standard FHIR R4 Resource</th>
                  <th className="py-3 px-4">ABDM Interoperability Purpose</th>
                  <th className="py-3 px-4">Generated Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {mappings.map((m, idx) => (
                  <tr key={idx} className="hover:bg-teal-50/20 transition">
                    <td className="py-3 px-4 font-semibold text-slate-900">{m.document_element}</td>
                    <td className="py-3 px-4 font-mono font-bold text-teal-700">
                      <span className="bg-teal-50 border border-teal-200 px-2 py-0.5 rounded">
                        {m.fhir_resource}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-600">{m.purpose}</td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center space-x-1 text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full font-medium text-[11px]">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        <span>Ready</span>
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Tab 2: Interactive FHIR JSON Bundle */}
        {activeSubTab === 'json' && (
          <div className="mt-6 bg-slate-950 text-slate-100 rounded-xl border border-slate-800 p-4">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800 text-xs">
              <span className="font-mono text-teal-400 font-semibold flex items-center space-x-2">
                <FileCode className="w-4 h-4" />
                <span>HL7 FHIR R4 Document Bundle (JSON)</span>
              </span>

              <button
                onClick={copyJson}
                className="flex items-center space-x-1 text-xs text-slate-300 hover:text-white bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-lg transition cursor-pointer"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Bundle Copied!' : 'Copy FHIR Bundle'}</span>
              </button>
            </div>

            <pre className="font-mono text-xs text-teal-200 whitespace-pre overflow-x-auto max-h-[450px] leading-relaxed p-2">
              {JSON.stringify(fhir.bundle || {}, null, 2)}
            </pre>
          </div>
        )}

      </div>

    </div>
  );
}
