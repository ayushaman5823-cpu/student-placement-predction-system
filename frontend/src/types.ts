export interface StudentInput {
  Branch: string;
  College_Tier: string;
  '10th_Percentage': number;
  '12th_Percentage': number;
  Current_CGPA: number;
  Backlogs: number;
  Attendance_Percentage: number;
  Projects: number;
  Internships: number;
}

export interface PredictionResult {
  predicted_status: 'Placed' | 'Not Placed';
  probability_placed: number;
  probability_not_placed: number;
  confidence_score: number;
  model_version: string;
  history_id?: number;
  input_features?: StudentInput;
}

export interface HoldoutMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
  brier_score: number;
}

export interface ConfusionMatrix {
  true_negatives: number;
  false_positives: number;
  false_negatives: number;
  true_positives: number;
}

export interface FeatureImportance {
  feature: string;
  importance_pct: number;
}

export interface ModelInfo {
  architecture: string;
  model_artifact_sha256: string;
  metadata_schema_version: string;
  holdout_test_metrics: HoldoutMetrics;
  confusion_matrix: ConfusionMatrix;
  valid_branches: string[];
  valid_tiers: string[];
  required_features: string[];
  feature_importances: FeatureImportance[];
  probability_semantics: Record<string, string>;
}

export interface SampleProfile {
  id: string;
  name: string;
  description: string;
  data: StudentInput;
  expected_status: string;
  expected_prob_placed: number;
}

export interface HistoryRecord {
  id: number;
  created_at: string;
  branch: string;
  college_tier: string;
  tenth_percentage: number;
  twelfth_percentage: number;
  current_cgpa: number;
  backlogs: number;
  attendance_percentage: number;
  projects: number;
  internships: number;
  student_features: StudentInput | Record<string, any>;
  predicted_status: 'Placed' | 'Not Placed';
  probability_placed: number;
  probability_not_placed: number;
  confidence_score: number;
  model_version: string;
}

