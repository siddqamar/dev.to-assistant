"use client"

import { TrendingUp, Users, Zap } from "lucide-react"

const features = [
  {
    icon: TrendingUp,
    title: "Track Tech Trends",
    description: "See which tools, languages, and frameworks are gaining traction right now.",
    accent: "#00F08B",
    shadow: "rgba(0,240,139,0.35)",
    bg: "linear-gradient(135deg, #00F08B 0%, #00C96E 100%)",
    highlight: "rgba(255,255,255,0.25)",
  },
  {
    icon: Users,
    title: "Engage with Community",
    description: "Discover trending discussions and conversations worth joining.",
    accent: "#00E5FF",
    shadow: "rgba(0,229,255,0.35)",
    bg: "linear-gradient(135deg, #00E5FF 0%, #00B8D9 100%)",
    highlight: "rgba(255,255,255,0.25)",
  },
  {
    icon: Zap,
    title: "Learn Tips & Tricks",
    description: "Extract actionable insights, hooks, and solutions from top posts.",
    accent: "#7C5CFC",
    shadow: "rgba(124,92,252,0.35)",
    bg: "linear-gradient(135deg, #35256A 0%, #7C5CFC 100%)",
    highlight: "rgba(255,255,255,0.15)",
  },
]

export function HeroSection() {
  return (
    <section className="w-full">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
        {features.map((f) => (
          <FeatureCard key={f.title} {...f} />
        ))}
      </div>

      {/* Stats bar */}
      <div className="mt-4 flex flex-wrap items-center justify-center gap-x-8 gap-y-2 py-3 px-4 rounded-xl border border-border bg-card text-xs text-muted-foreground">
        <StatChip value="100+" label="posts per scan" dot="#00F08B" />
        <div className="hidden sm:block w-px h-3 bg-border" />
        <StatChip value="Any tag" label="full coverage" dot="#00E5FF" />
        <div className="hidden sm:block w-px h-3 bg-border" />
        <StatChip value="~30s" label="analysis time" dot="#7C5CFC" />
        <div className="hidden sm:block w-px h-3 bg-border" />
        <span className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground/60">Powered by Gemma 4</span>
      </div>
    </section>
  )
}

function FeatureCard({
  icon: Icon,
  title,
  description,
  accent,
  shadow,
  bg,
  highlight,
}: {
  icon: React.ElementType
  title: string
  description: string
  accent: string
  shadow: string
  bg: string
  highlight: string
}) {
  return (
    <div
      className="group relative flex flex-col gap-4 p-5 sm:p-6 rounded-2xl bg-card border border-border overflow-hidden
        transition-all duration-300 ease-out cursor-default
        hover:-translate-y-1.5 hover:shadow-xl"
      style={{
        ["--card-shadow" as string]: shadow,
        boxShadow: "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
      }}
      onMouseEnter={(e) => {
        (e.currentTarget as HTMLDivElement).style.boxShadow = `0 20px 40px -8px ${shadow}, 0 8px 16px -4px ${shadow}`
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLDivElement).style.boxShadow =
          "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)"
      }}
    >
      {/* Subtle tinted hover bg */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
        style={{ background: `radial-gradient(ellipse at top left, ${accent}0D 0%, transparent 70%)` }}
      />

      {/* 3D Icon */}
      <div
        className="relative w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center flex-shrink-0
          transition-all duration-300 group-hover:scale-110 group-hover:rotate-[-4deg]"
        style={{
          background: bg,
          boxShadow: `0 8px 24px -4px ${shadow}, 0 2px 6px -1px ${shadow}, inset 0 1px 0 ${highlight}`,
        }}
      >
        {/* Top gloss for 3D look */}
        <div
          className="absolute top-0 left-0 right-0 h-1/2 rounded-t-2xl"
          style={{ background: `linear-gradient(180deg, ${highlight} 0%, transparent 100%)` }}
        />
        <Icon className="relative z-10 w-5 h-5 sm:w-6 sm:h-6 text-white drop-shadow" strokeWidth={2.5} />
      </div>

      {/* Text */}
      <div className="flex flex-col gap-1.5">
        <span
          className="font-bold text-sm sm:text-base text-foreground tracking-tight transition-colors duration-300 group-hover:text-[var(--ac)]"
          style={{ ["--ac" as string]: accent }}
        >
          {title}
        </span>
        <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">{description}</p>
      </div>

    </div>
  )
}

function StatChip({ value, label, dot }: { value: string; label: string; dot: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: dot }} />
      <span className="font-bold text-foreground">{value}</span>
      <span>{label}</span>
    </div>
  )
}
