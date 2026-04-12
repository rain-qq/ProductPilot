import { useState, useEffect } from 'react'
import { AlertCircle, CheckCircle2 } from 'lucide-react'
import { Layout } from '@/components/Layout'
import { GenerationForm } from '@/components/GenerationForm'
import { ImageGallery } from '@/components/ImageGallery'
import { TaskProgress } from '@/components/TaskProgress'
import { generateImageAsync, getTaskStatus, type GenerationRequest, type GenerationResponse, type TaskInfo } from '@/services/imageService'

export function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [task, setTask] = useState<TaskInfo | null>(null)
  const [result, setResult] = useState<GenerationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  // 轮询任务状态
  useEffect(() => {
    if (!task || task.status === 'completed' || task.status === 'failed') return

    const interval = setInterval(async () => {
      try {
        const updatedTask = await getTaskStatus(task.task_id)
        setTask(updatedTask)

        if (updatedTask.status === 'completed') {
          setResult(updatedTask.result)
          setSuccess('图片生成成功!')
          setIsLoading(false)
        } else if (updatedTask.status === 'failed') {
          setError(updatedTask.error_message || '生成失败')
          setIsLoading(false)
        }
      } catch (err) {
        console.error('Failed to fetch task status:', err)
      }
    }, 3000) // 每3秒轮询一次

    return () => clearInterval(interval)
  }, [task])

  const handleSubmit = async (data: GenerationRequest) => {
    setIsLoading(true)
    setError(null)
    setSuccess(null)
    setResult(null)
    setTask(null)

    try {
      // 使用异步接口
      const newTask = await generateImageAsync(data)
      setTask(newTask)
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } }; message?: string }
      setError(error.response?.data?.detail || error.message || '提交任务失败')
      setIsLoading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* 页面标题 */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">AI 电商图片生成</h2>
          <p className="text-slate-400">基于 CrewAI + LangGraph 的智能图片生成系统</p>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm text-red-300">{error}</p>
            </div>
            <button onClick={() => setError(null)} className="text-red-400 hover:text-red-300">
              ×
            </button>
          </div>
        )}

        {/* 成功提示 */}
        {success && (
          <div className="mb-6 p-4 bg-green-500/10 border border-green-500/50 rounded-lg flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm text-green-300">{success}</p>
            </div>
            <button onClick={() => setSuccess(null)} className="text-green-400 hover:text-green-300">
              ×
            </button>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* 左侧:表单 */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 backdrop-blur-sm">
            <h3 className="text-lg font-semibold text-white mb-6">配置参数</h3>
            <GenerationForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>

          {/* 右侧:结果展示 */}
          <div className="space-y-6">
            {/* 任务进度 */}
            {task && (
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 backdrop-blur-sm">
                <TaskProgress
                  status={task.status}
                  progress={task.progress}
                  currentStep={task.current_step}
                />
              </div>
            )}

            {/* 生成结果 */}
            {result && result.success && result.images.length > 0 && (
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 backdrop-blur-sm">
                <ImageGallery
                  images={result.images}
                  qualityScores={result.quality_scores}
                  evaluations={result.quality_evaluations}
                />
                
                {/* 元信息 */}
                {result.metadata && result.metadata.generation_time != null && (
                  <div className="mt-6 pt-6 border-t border-slate-800">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-slate-400">生成耗时:</span>
                        <span className="ml-2 text-white font-medium">
                          {typeof result.metadata.generation_time === 'number' 
                            ? `${result.metadata.generation_time.toFixed(1)}s`
                            : 'N/A'}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-400">迭代次数:</span>
                        <span className="ml-2 text-white font-medium">{result.iteration_count}</span>
                      </div>
                      {result.metadata.model_version && (
                        <div>
                          <span className="text-slate-400">模型版本:</span>
                          <span className="ml-2 text-white font-medium">{result.metadata.model_version}</span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 空状态 */}
            {!task && !result && (
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-12 backdrop-blur-sm text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-800 flex items-center justify-center">
                  <svg
                    className="w-8 h-8 text-slate-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                </div>
                <p className="text-slate-400">填写左侧表单开始生成图片</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}
