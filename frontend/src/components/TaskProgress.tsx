import { CheckCircle, Clock, Loader2, XCircle } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { TaskStatus } from '@/services/imageService'

interface TaskProgressProps {
  status: TaskStatus
  progress: number
  currentStep: string
  className?: string
}

const statusConfig = {
  pending: {
    icon: Clock,
    color: 'text-slate-400',
    bgColor: 'bg-slate-500/20',
    label: '等待处理',
  },
  processing: {
    icon: Loader2,
    color: 'text-blue-400',
    bgColor: 'bg-blue-500/20',
    label: '处理中',
  },
  completed: {
    icon: CheckCircle,
    color: 'text-green-400',
    bgColor: 'bg-green-500/20',
    label: '已完成',
  },
  failed: {
    icon: XCircle,
    color: 'text-red-400',
    bgColor: 'bg-red-500/20',
    label: '失败',
  },
}

export function TaskProgress({ status, progress, currentStep, className }: TaskProgressProps) {
  const config = statusConfig[status]
  const Icon = config.icon

  return (
    <div className={cn('space-y-4', className)}>
      {/* 状态头部 */}
      <div className="flex items-center gap-3">
        <div className={cn('p-2 rounded-lg', config.bgColor)}>
          <Icon className={cn('w-5 h-5', config.color, status === 'processing' && 'animate-spin')} />
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-medium text-white">{config.label}</h3>
          <p className="text-xs text-slate-400">{currentStep}</p>
        </div>
        <span className="text-sm font-semibold text-white">{progress.toFixed(0)}%</span>
      </div>

      {/* 进度条 */}
      <div className="relative h-2 bg-slate-800 rounded-full overflow-hidden">
        <div
          className={cn(
            'absolute left-0 top-0 h-full transition-all duration-500 rounded-full',
            status === 'failed'
              ? 'bg-gradient-to-r from-red-500 to-red-600'
              : status === 'completed'
              ? 'bg-gradient-to-r from-green-500 to-emerald-500'
              : 'bg-gradient-to-r from-violet-500 to-fuchsia-500'
          )}
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* 步骤指示器 */}
      <div className="grid grid-cols-6 gap-2">
        {[
          { label: '分析需求', threshold: 20 },
          { label: '优化提示词', threshold: 35 },
          { label: '生成图片', threshold: 60 },
          { label: '质量检查', threshold: 80 },
          { label: '后处理', threshold: 95 },
          { label: '完成', threshold: 100 },
        ].map((step, index) => {
          const isCompleted = progress >= step.threshold
          const isCurrent = progress < step.threshold && (index === 0 || progress >= [0, 20, 35, 60, 80, 95][index - 1])
          
          return (
            <div key={index} className="text-center">
              <div
                className={cn(
                  'w-2 h-2 mx-auto rounded-full mb-1 transition-all',
                  isCompleted ? 'bg-green-500' : isCurrent ? 'bg-violet-500 animate-pulse' : 'bg-slate-700'
                )}
              />
              <span className={cn('text-[10px]', isCompleted || isCurrent ? 'text-slate-300' : 'text-slate-600')}>
                {step.label}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
