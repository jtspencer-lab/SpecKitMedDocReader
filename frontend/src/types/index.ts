"""
TypeScript interfaces and types for API responses.
"""

export interface Document {
  id: string;
  filename: string;
  file_size: number;
  document_type: string;
  status: string;
  mime_type: string;
  confidence_score?: number;
  extraction_attempts: number;
  patient_id?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  file_size: number;
  status: string;
  created_at: string;
}

export interface ExtractionField {
  field_name: string;
  field_value: string;
  confidence: number;
  confidence_source: string;
}

export interface ExtractionResult {
  id: string;
  document_id: string;
  status: string;
  overall_confidence: number;
  is_flagged: boolean;
  flag_reason?: string;
  fields: ExtractionField[];
  created_at: string;
  updated_at: string;
}

export interface ReviewRecord {
  review_id: string;
  extraction_result_id: string;
  document_id: string;
  status: string;
  reviewer_id?: string;
  feedback?: string;
  is_approved: boolean;
  rejection_reason?: string;
  priority: number;
  created_at: string;
  updated_at: string;
}

export interface ApiError {
  error_code: string;
  message: string;
  details?: Record<string, unknown>;
}
