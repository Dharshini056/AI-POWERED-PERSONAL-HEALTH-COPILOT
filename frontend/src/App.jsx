import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardView from './components/DashboardView';
import DocumentUpload from './components/DocumentUpload';
import DocumentsListView from './components/DocumentsListView';
import HealthTimeline from './components/HealthTimeline';
import MedicationCards from './components/MedicationCards';
import LabOverview from './components/LabOverview';
import HealthCopilotChat from './components/HealthCopilotChat';
import AbhaFhirView from './components/AbhaFhirView';
import ArchitectureView from './components/ArchitectureView';
import OCRComparisonModal from './components/OCRComparisonModal';

import { 
  fetchHealthProfile, 
  fetchHealthTimeline, 
  fetchDocuments, 
  loadDemoSamples, 
  resetAllData 
} from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [profile, setProfile] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [selectedDocForOCR, setSelectedDocForOCR] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isDemoLoading, setIsDemoLoading] = useState(false);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [profData, timeData, docsData] = await Promise.all([
        fetchHealthProfile().catch(() => null),
        fetchHealthTimeline().catch(() => ({ timeline: [] })),
        fetchDocuments().catch(() => ({ documents: [] }))
      ]);

      if (profData) setProfile(profData);
      if (timeData) setTimeline(timeData.timeline || []);
      if (docsData) setDocuments(docsData.documents || []);
    } catch (err) {
      console.error('Data loading error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleLoadDemo = async () => {
    setIsDemoLoading(true);
    try {
      await loadDemoSamples();
      await loadData();
    } catch (err) {
      alert('Error loading demo samples: ' + err.message);
    } finally {
      setIsDemoLoading(false);
    }
  };

  const handleResetData = async () => {
    if (window.confirm('Reset all records to a clean slate?')) {
      try {
        await resetAllData();
        await loadData();
      } catch (err) {
        alert('Reset error: ' + err.message);
      }
    }
  };

  const handleUploadSuccess = (newDoc) => {
    loadData();
    setSelectedDocForOCR(newDoc);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-900">
      
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedLanguage={selectedLanguage}
        setSelectedLanguage={setSelectedLanguage}
        onLoadDemo={handleLoadDemo}
        onResetData={handleResetData}
        isDemoLoading={isDemoLoading}
      />

      {/* Main Page Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        
        {/* Tab 1: Dashboard */}
        {activeTab === 'dashboard' && (
          <DashboardView
            profile={profile}
            timeline={timeline}
            selectedLanguage={selectedLanguage}
            setSelectedLanguage={setSelectedLanguage}
            onNavigate={(tab) => setActiveTab(tab)}
            onViewOCR={(doc) => setSelectedDocForOCR(doc)}
          />
        )}

        {/* Tab 2: Upload & OCR */}
        {activeTab === 'upload' && (
          <div className="space-y-6">
            <DocumentUpload
              onUploadSuccess={handleUploadSuccess}
              onViewOCR={(doc) => setSelectedDocForOCR(doc)}
            />
            <DocumentsListView
              documents={documents}
              onViewOCR={(doc) => setSelectedDocForOCR(doc)}
              onUploadNew={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            />
          </div>
        )}

        {/* Tab 3: Health Timeline */}
        {activeTab === 'timeline' && (
          <HealthTimeline
            timelineEvents={timeline}
            onSelectDocument={(docId) => {
              const d = documents.find((doc) => doc.id === docId);
              if (d) setSelectedDocForOCR(d);
            }}
          />
        )}

        {/* Tab 4: Medications */}
        {activeTab === 'medications' && (
          <MedicationCards
            medications={profile?.medications || []}
            selectedLanguage={selectedLanguage}
          />
        )}

        {/* Tab 5: Lab Reports */}
        {activeTab === 'labs' && (
          <LabOverview
            labResults={profile?.lab_results || []}
            selectedLanguage={selectedLanguage}
          />
        )}

        {/* Tab 6: AI Copilot Chat */}
        {activeTab === 'chat' && (
          <HealthCopilotChat
            selectedLanguage={selectedLanguage}
          />
        )}

        {/* Tab 7: ABHA & FHIR */}
        {activeTab === 'abha' && (
          <AbhaFhirView />
        )}

        {/* Tab 8: Architecture */}
        {activeTab === 'architecture' && (
          <ArchitectureView />
        )}

      </main>

      {/* OCR Comparison Modal */}
      {selectedDocForOCR && (
        <OCRComparisonModal
          documentData={selectedDocForOCR}
          onClose={() => setSelectedDocForOCR(null)}
        />
      )}

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-12 py-6 text-xs text-slate-500 text-center">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>
            <strong>AI Personal Health Copilot</strong> — Built for Healthcare Hackathon 2026. Powered by RapidOCR (PaddleONNX), PyMuPDF, FastAPI, and HL7 FHIR R4 standard.
          </p>
          <p className="text-slate-400">
            Compliant with non-diagnostic clinical communication safety guardrails.
          </p>
        </div>
      </footer>

    </div>
  );
}
