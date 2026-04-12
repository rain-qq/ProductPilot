import { Download, Eye, Star } from 'lucide-react'
import type { GeneratedImage, QualityEvaluation } from '@/services/imageService'

interface ImageGalleryProps {
  images: GeneratedImage[]
  qualityScores?: number[]
  evaluations?: QualityEvaluation[]
}

export function ImageGallery({ images, qualityScores = [], evaluations = [] }: ImageGalleryProps) {
  if (images.length === 0) return null

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-white">生成结果</h3>
      <div className="grid grid-cols-2 gap-4">
        {images.map((image, index) => (
          <div key={index} className="group relative bg-slate-800 rounded-lg overflow-hidden border border-slate-700 hover:border-violet-500 transition-all">
            {/* 图片 */}
            <div className="aspect-square relative overflow-hidden">
              <img
                src={image.url}
                alt={`Generated image ${index + 1}`}
                className="w-full h-full object-cover"
              />
              
              {/* 悬浮操作 */}
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3">
                <button
                  onClick={() => window.open(image.url, '_blank')}
                  className="p-2 bg-white/10 hover:bg-white/20 rounded-lg backdrop-blur-sm transition-colors"
                  title="查看大图"
                >
                  <Eye className="w-5 h-5 text-white" />
                </button>
                <a
                  href={image.url}
                  download
                  className="p-2 bg-white/10 hover:bg-white/20 rounded-lg backdrop-blur-sm transition-colors"
                  title="下载图片"
                >
                  <Download className="w-5 h-5 text-white" />
                </a>
              </div>
            </div>

            {/* 图片信息 */}
            <div className="p-3 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>{image.width} × {image.height}</span>
                <span className="uppercase">{image.format}</span>
              </div>
              
              {qualityScores[index] && (
                <div className="flex items-center gap-2">
                  <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                  <span className="text-sm font-medium text-white">
                    {(qualityScores[index] * 100).toFixed(0)}%
                  </span>
                  <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full transition-all"
                      style={{ width: `${qualityScores[index] * 100}%` }}
                    />
                  </div>
                </div>
              )}

              {evaluations[index] && (
                <div className="text-xs space-y-1">
                  <div className="flex justify-between text-slate-400">
                    <span>清晰度:</span>
                    <span className="text-slate-300">{(evaluations[index].clarity * 100).toFixed(0)}%</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>色彩:</span>
                    <span className="text-slate-300">{(evaluations[index].color_accuracy * 100).toFixed(0)}%</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>构图:</span>
                    <span className="text-slate-300">{(evaluations[index].composition * 100).toFixed(0)}%</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
