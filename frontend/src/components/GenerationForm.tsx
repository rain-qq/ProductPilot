import { useState } from 'react'
import { Sparkles, Upload, Image as ImageIcon, Settings } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { ProductInfo, GenerationRequest } from '@/services/imageService'

interface GenerationFormProps {
  onSubmit: (data: GenerationRequest) => void
  isLoading: boolean
}

export function GenerationForm({ onSubmit, isLoading }: GenerationFormProps) {
  const [mode, setMode] = useState<'text2img' | 'img2img' | 'mixed'>('mixed')
  const [formData, setFormData] = useState<ProductInfo>({
    name: '',
    description: '',
    category: '',
    target_audience: '',
    key_features: [],
    reference_image_url: '',
  })
  const [settings, setSettings] = useState({
    num_images: 4,
    quality_threshold: 0.8,
    max_retries: 3,
    negative_prompt: 'blurry, low quality, distorted, watermark',
    style_preference: '',
  })
  const [featureInput, setFeatureInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      product_info: formData,
      mode,
      ...settings,
    })
  }

  const addFeature = () => {
    if (featureInput.trim() && !formData.key_features?.includes(featureInput.trim())) {
      setFormData({
        ...formData,
        key_features: [...(formData.key_features || []), featureInput.trim()],
      })
      setFeatureInput('')
    }
  }

  const removeFeature = (index: number) => {
    setFormData({
      ...formData,
      key_features: formData.key_features?.filter((_, i) => i !== index),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* 生成模式选择 */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { value: 'text2img', label: '文生图', icon: Sparkles },
          { value: 'img2img', label: '图生图', icon: ImageIcon },
          { value: 'mixed', label: '混合模式', icon: Settings },
        ].map((item) => (
          <button
            key={item.value}
            type="button"
            onClick={() => setMode(item.value as 'text2img' | 'img2img' | 'mixed')}
            className={cn(
              'flex items-center justify-center gap-2 px-4 py-3 rounded-lg border transition-all',
              mode === item.value
                ? 'border-violet-500 bg-violet-500/10 text-violet-400'
                : 'border-slate-700 bg-slate-800/50 text-slate-400 hover:border-slate-600'
            )}
          >
            <item.icon className="w-4 h-4" />
            <span className="text-sm font-medium">{item.label}</span>
          </button>
        ))}
      </div>

      {/* 产品信息 */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">商品名称 *</label>
          <input
            type="text"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
            placeholder="例如:无线蓝牙耳机"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">商品描述 *</label>
          <textarea
            required
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={3}
            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all resize-none"
            placeholder="详细描述商品特点、材质、功能等"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">商品类别</label>
            <input
              type="text"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
              placeholder="例如:数码配件"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">目标人群</label>
            <input
              type="text"
              value={formData.target_audience}
              onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
              className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
              placeholder="例如:年轻白领"
            />
          </div>
        </div>

        {/* 核心卖点 */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">核心卖点</label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              value={featureInput}
              onChange={(e) => setFeatureInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addFeature())}
              className="flex-1 px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
              placeholder="输入卖点后按回车添加"
            />
            <button
              type="button"
              onClick={addFeature}
              className="px-4 py-2.5 bg-violet-600 hover:bg-violet-700 text-white rounded-lg transition-colors font-medium"
            >
              添加
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {formData.key_features?.map((feature, index) => (
              <span
                key={index}
                className="inline-flex items-center gap-1 px-3 py-1 bg-violet-500/20 text-violet-300 rounded-full text-sm"
              >
                {feature}
                <button
                  type="button"
                  onClick={() => removeFeature(index)}
                  className="hover:text-violet-100 transition-colors"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* 参考图片 */}
        {mode !== 'text2img' && (
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">参考图片 URL</label>
            <div className="flex gap-2">
              <input
                type="url"
                value={formData.reference_image_url}
                onChange={(e) => setFormData({ ...formData, reference_image_url: e.target.value })}
                className="flex-1 px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
                placeholder="https://example.com/image.jpg"
              />
              <button
                type="button"
                className="px-4 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors flex items-center gap-2"
              >
                <Upload className="w-4 h-4" />
                上传
              </button>
            </div>
          </div>
        )}
      </div>

      {/* 高级设置 */}
      <div className="border-t border-slate-800 pt-6 space-y-4">
        <h3 className="text-sm font-semibold text-slate-300">高级设置</h3>
        
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm text-slate-400 mb-2">生成数量</label>
            <input
              type="number"
              min={1}
              max={10}
              value={settings.num_images}
              onChange={(e) => setSettings({ ...settings, num_images: parseInt(e.target.value) })}
              className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-2">质量阈值 (0-1)</label>
            <input
              type="number"
              min={0}
              max={1}
              step={0.05}
              value={settings.quality_threshold}
              onChange={(e) => setSettings({ ...settings, quality_threshold: parseFloat(e.target.value) })}
              className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-2">最大重试次数</label>
            <input
              type="number"
              min={1}
              max={5}
              value={settings.max_retries}
              onChange={(e) => setSettings({ ...settings, max_retries: parseInt(e.target.value) })}
              className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-2">负向提示词</label>
          <input
            type="text"
            value={settings.negative_prompt}
            onChange={(e) => setSettings({ ...settings, negative_prompt: e.target.value })}
            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-2">风格偏好</label>
          <input
            type="text"
            value={settings.style_preference}
            onChange={(e) => setSettings({ ...settings, style_preference: e.target.value })}
            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all"
            placeholder="例如:现代简约风格、科技感、温馨居家..."
          />
        </div>
      </div>

      {/* 提交按钮 */}
      <button
        type="submit"
        disabled={isLoading}
        className={cn(
          'w-full py-3 px-6 rounded-lg font-semibold text-white transition-all',
          isLoading
            ? 'bg-slate-700 cursor-not-allowed'
            : 'bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 shadow-lg shadow-violet-500/25'
        )}
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            生成中...
          </span>
        ) : (
          '开始生成'
        )}
      </button>
    </form>
  )
}
