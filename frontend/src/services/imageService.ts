import api from '@/lib/api'

export interface ProductInfo {
  name: string
  description: string
  category?: string
  target_audience?: string
  key_features?: string[]
  reference_image_url?: string
}

export interface GenerationRequest {
  product_info: ProductInfo
  mode?: 'text2img' | 'img2img' | 'mixed'
  num_images?: number
  quality_threshold?: number
  max_retries?: number
  negative_prompt?: string
  style_preference?: string
  custom_settings?: Record<string, unknown>
}

export interface GeneratedImage {
  url: string
  thumbnail_url?: string
  width: number
  height: number
  format: string
  size_bytes?: number
}

export interface QualityEvaluation {
  overall_score: number
  clarity: number
  color_accuracy: number
  composition: number
  commercial_value: number
  issues: string[]
  suggestions: string[]
}

export interface AnalysisResult {
  color_scheme: string[]
  composition_type: string
  lighting_style: string
  background_type: string
  viewing_angle: string
  style_tags: string[]
  marketing_points: string[]
}

export interface PromptResult {
  positive_prompt: string
  negative_prompt: string
  suggested_settings: {
    steps: number
    cfg_scale: number
  }
}

export interface GenerationResponse {
  success: boolean
  images: GeneratedImage[]
  selected_image?: GeneratedImage
  quality_scores: number[]
  iteration_count: number
  analysis_result?: AnalysisResult
  prompt_result?: PromptResult
  quality_evaluations?: QualityEvaluation[]
  error_message?: string | null
  metadata?: {
    generation_time: number
    model_version: string
  }
}

export type TaskStatus = 'pending' | 'processing' | 'completed' | 'failed'

export interface TaskInfo {
  task_id: string
  status: TaskStatus
  progress: number
  current_step: string
  result: GenerationResponse | null
  error_message: string | null
  created_at: string
  updated_at: string
}

// API 方法
export const generateImageSync = async (request: GenerationRequest): Promise<GenerationResponse> => {
  return api.post('/generate', request)
}

export const generateImageAsync = async (request: GenerationRequest): Promise<TaskInfo> => {
  return api.post('/generate/async', request)
}

export const getTaskStatus = async (taskId: string): Promise<TaskInfo> => {
  return api.get(`/task/${taskId}`)
}

export const checkHealth = async (): Promise<{ status: string; timestamp: string }> => {
  return api.get('/health')
}
