const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export async function uploadMedicalDocument(file, onProgress) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${BASE_URL}/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to upload and process document');
  }

  return await response.json();
}

export async function fetchDocuments() {
  const res = await fetch(`${BASE_URL}/documents`);
  if (!res.ok) throw new Error('Failed to fetch documents');
  return await res.json();
}

export async function fetchDocumentById(id) {
  const res = await fetch(`${BASE_URL}/documents/${id}`);
  if (!res.ok) throw new Error('Failed to fetch document details');
  return await res.json();
}

export async function fetchHealthProfile() {
  const res = await fetch(`${BASE_URL}/health-profile`);
  if (!res.ok) throw new Error('Failed to fetch health profile');
  return await res.json();
}

export async function fetchHealthTimeline() {
  const res = await fetch(`${BASE_URL}/timeline`);
  if (!res.ok) throw new Error('Failed to fetch health timeline');
  return await res.json();
}

export async function sendChatMessage(message, language = 'English') {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, language, session_id: 'default' }),
  });
  if (!res.ok) throw new Error('Failed to get chat response');
  return await res.json();
}

export async function translateText(text, target_language) {
  const res = await fetch(`${BASE_URL}/translate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, target_language, context_type: 'summary' }),
  });
  if (!res.ok) throw new Error('Translation failed');
  return await res.json();
}

export async function fetchAbhaProfile() {
  const res = await fetch(`${BASE_URL}/abha-profile`);
  if (!res.ok) throw new Error('Failed to fetch ABHA profile');
  return await res.json();
}

export async function loadDemoSamples() {
  const res = await fetch(`${BASE_URL}/demo/load-samples`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to load demo samples');
  return await res.json();
}

export async function resetAllData() {
  const res = await fetch(`${BASE_URL}/documents/reset`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to reset records');
  return await res.json();
}
