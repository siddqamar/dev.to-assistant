"use client"

import { Copy, Download } from "lucide-react"
import { ResultsTable } from "./results-table"

export interface PostData {
  id: number
  author: string
  avatar: string
  date: string
  topic: string
  hook: string
  problem: string
  solution: string
  reacts: number
  comments: number
  url: string
}

interface ResultsSectionProps {
  data: PostData[]
}

export function ResultsSection({ data }: ResultsSectionProps) {
  const handleCopyData = () => {
    const text = data.map(d => 
      `${d.author} - ${d.topic}\nHook: ${d.hook}\nProblem: ${d.problem}\nSolution: ${d.solution}\n`
    ).join('\n---\n')
    navigator.clipboard.writeText(text)
  }

  const handleExportCSV = () => {
    const headers = ['Author', 'Date', 'Topic', 'Hook', 'Problem', 'Solution', 'Reacts', 'Comments']
    const rows = data.map(d => [
      d.author, d.date, d.topic, d.hook, d.problem, d.solution, d.reacts.toString(), d.comments.toString()
    ])
    const csv = [headers.join(','), ...rows.map(r => r.map(c => `"${c}"`).join(','))].join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'analysis-results.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <section>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-3">
        <h2 className="text-base sm:text-lg font-semibold tracking-[-0.02em]">Analysis Results</h2>
        <div className="flex flex-wrap gap-2 sm:gap-3 w-full sm:w-auto">
          <button
            onClick={handleCopyData}
            className="flex-1 sm:flex-none h-9 sm:h-11 px-4 sm:px-8 font-semibold text-xs sm:text-sm rounded-full bg-transparent text-foreground border border-[var(--accent-cyan)] cursor-pointer inline-flex items-center justify-center gap-1.5 sm:gap-2 transition-colors hover:bg-[rgba(0,229,255,0.05)]"
          >
            <Copy className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
            Copy Data
          </button>
          <button
            onClick={handleExportCSV}
            className="flex-1 sm:flex-none h-9 sm:h-11 px-4 sm:px-8 font-semibold text-xs sm:text-sm rounded-full bg-transparent text-foreground border border-[var(--accent-cyan)] cursor-pointer inline-flex items-center justify-center gap-1.5 sm:gap-2 transition-colors hover:bg-[rgba(0,229,255,0.05)]"
          >
            <Download className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
            Export CSV
          </button>
        </div>
      </div>
      <ResultsTable data={data} />
    </section>
  )
}
