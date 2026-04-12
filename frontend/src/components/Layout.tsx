import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface HeaderProps {
  className?: string
}

export function Header({ className }: HeaderProps) {
  return (
    <header className={cn('border-b border-slate-800 bg-slate-950/50 backdrop-blur-sm', className)}>
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center">
              <span className="text-white font-bold text-lg">P</span>
            </div>
            <div>
              <h1 className="text-xl font-semibold text-white">ProductPilot</h1>
              <p className="text-xs text-slate-400">AI 电商图片生成系统</p>
            </div>
          </div>
          <nav className="flex items-center gap-6">
            <a href="#" className="text-sm text-slate-300 hover:text-white transition-colors">
              文档
            </a>
            <a href="#" className="text-sm text-slate-300 hover:text-white transition-colors">
              GitHub
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}

interface FooterProps {
  className?: string
}

export function Footer({ className }: FooterProps) {
  return (
    <footer className={cn('border-t border-slate-800 bg-slate-950/50', className)}>
      <div className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between text-sm text-slate-400">
          <p>© 2026 ProductPilot. All rights reserved.</p>
          <p>Powered by CrewAI + LangGraph</p>
        </div>
      </div>
    </footer>
  )
}

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-6 py-8">{children}</main>
      <Footer />
    </div>
  )
}
