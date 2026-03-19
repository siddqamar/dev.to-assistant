"use client"

import { Minus, Plus } from "lucide-react"

interface ControlsCardProps {
  tag: string
  setTag: (tag: string) => void
  pages: number
  setPages: (pages: number) => void
  onAnalyze: () => void
}

export function ControlsCard({ tag, setTag, pages, setPages, onAnalyze }: ControlsCardProps) {
  const decreasePages = () => {
    if (pages > 1) setPages(pages - 1)
  }

  const increasePages = () => {
    if (pages < 50) setPages(pages + 1)
  }

  return (
    <section className="bg-card p-4 sm:p-6 flex flex-col sm:flex-row sm:items-end gap-4 sm:gap-6 border border-border rounded-lg">
      {/* Tag Input */}
      <div className="flex flex-col flex-grow sm:max-w-[400px]">
        <span className="text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground mb-1.5">
          Target Tag
        </span>
        <div className="relative flex items-center">
          <span className="absolute left-4 text-muted-foreground font-medium">#</span>
          <input
            type="text"
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="e.g. webdev, python, react"
            className="h-11 w-full pl-8 pr-4 text-sm font-sans border border-border rounded-md bg-background text-foreground outline-none transition-colors focus:border-[var(--accent-purple)] focus:bg-card"
          />
        </div>
      </div>

      {/* Pages Control */}
      <div className="flex flex-col">
        <span className="text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground mb-1.5">
          Pages to Scan
        </span>
        <div className="flex items-center bg-background border border-border rounded-md h-11 overflow-hidden">
          <button
            onClick={decreasePages}
            aria-label="Decrease"
            className="w-10 h-full flex items-center justify-center text-muted-foreground text-lg hover:bg-border hover:text-foreground transition-colors"
          >
            <Minus className="w-4 h-4" />
          </button>
          <input
            type="number"
            value={pages}
            onChange={(e) => setPages(Math.max(1, Math.min(50, parseInt(e.target.value) || 1)))}
            min="1"
            max="50"
            className="w-[60px] h-full border-none bg-transparent text-center text-sm font-sans text-foreground outline-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          />
          <button
            onClick={increasePages}
            aria-label="Increase"
            className="w-10 h-full flex items-center justify-center text-muted-foreground text-lg hover:bg-border hover:text-foreground transition-colors"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Analyze Button */}
      <button
        onClick={onAnalyze}
        className="h-11 w-full sm:w-auto px-8 font-semibold text-sm rounded-full bg-[var(--accent-green)] text-black border-none cursor-pointer inline-flex items-center justify-center gap-2 transition-all hover:-translate-y-0.5 hover:shadow-[0_4px_12px_rgba(0,240,139,0.3)]"
      >
        Analyze Posts
      </button>
    </section>
  )
}
