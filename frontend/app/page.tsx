"use client"

import { useState } from "react"
import { AnalyzerHeader } from "@/components/analyzer/header"
import { HeroSection } from "@/components/analyzer/hero-section"
import { ControlsCard } from "@/components/analyzer/controls-card"
import { ResultsSection } from "@/components/analyzer/results-section"

const sampleData = [
  {
    id: 1,
    author: "Sarah Drasner",
    avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
    date: "Oct 24",
    topic: "FastAPI Architecture",
    hook: "\"Stop building monoliths in Python. Here is why your next API should be asynchronous from day one.\"",
    problem: "Sync blocking I/O creates bottlenecks when scaling machine learning endpoints.",
    solution: "Implementing FastAPI with Uvicorn and Asyncpg for non-blocking database queries.",
    reacts: 420,
    comments: 85,
    url: "#"
  },
  {
    id: 2,
    author: "Alex Developer",
    avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
    date: "Oct 22",
    topic: "Python Tips",
    hook: "\"You are probably using Python decorators wrong. Let's fix that in 3 minutes.\"",
    problem: "Losing metadata and debugging context when wrapping functions with standard closures.",
    solution: "Using the built-in functools.wraps to preserve function signatures.",
    reacts: 156,
    comments: 22,
    url: "#"
  },
  {
    id: 3,
    author: "Maria Tech",
    avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Maria",
    date: "Oct 21",
    topic: "Gemma 4 API",
    hook: "\"Integrating Gemma 4 into legacy codebases doesn't have to be a nightmare.\"",
    problem: "Handling rate limits and parsing unstructured JSON responses from LLM endpoints.",
    solution: "Building a resilient adapter pattern with exponential backoff and Pydantic validation.",
    reacts: 890,
    comments: 143,
    url: "#"
  },
  {
    id: 4,
    author: "Jason Cooper",
    avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Jason",
    date: "Oct 20",
    topic: "Data Science",
    hook: "\"Pandas is great, but Polars might be the future of data manipulation in Python.\"",
    problem: "Memory constraints and slow processing when working with datasets over 10GB.",
    solution: "Migrating critical data pipelines to Polars for lazy evaluation and multi-threading.",
    reacts: 312,
    comments: 67,
    url: "#"
  }
]

export default function DevToAnalyzer() {
  const [tag, setTag] = useState("python")
  const [pages, setPages] = useState(3)
  const [data, setData] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/analyze?tag=${tag}&pages=${pages}`)
      if (!response.ok) {
        throw new Error("Failed to fetch data from API")
      }
      const result = await response.json()
      setData(result)
    } catch (err: any) {
      setError(err.message || "An error occurred")
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background p-4 sm:p-6 lg:p-8">
      <div className="mx-auto max-w-[1400px] flex flex-col gap-4 sm:gap-6">
        <AnalyzerHeader />
        <HeroSection />
        <ControlsCard 
          tag={tag}
          setTag={setTag}
          pages={pages}
          setPages={setPages}
          onAnalyze={handleAnalyze}
        />
        {error && (
          <div className="p-4 bg-destructive/10 border border-destructive text-destructive rounded-lg">
            {error}
          </div>
        )}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <div className="w-12 h-12 border-4 border-[var(--accent-green)] border-t-transparent rounded-full animate-spin"></div>
            <p className="text-muted-foreground animate-pulse text-lg font-medium">
              Gemma 4 is analyzing posts for #{tag}...
            </p>
          </div>
        ) : (
          <ResultsSection data={data.length > 0 ? data : []} />
        )}
      </div>
    </div>
  )
}
