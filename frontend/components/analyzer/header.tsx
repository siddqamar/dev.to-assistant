export function AnalyzerHeader() {
  return (
    <header className="relative flex flex-col items-center justify-center pt-10 pb-8 sm:pt-14 sm:pb-10 text-center">
      {/* Beta badge — pinned top right */}
      <div className="absolute top-0 right-0">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#35256A] text-white text-[10px] font-bold uppercase tracking-widest shadow-md">
          <span className="w-1.5 h-1.5 rounded-full bg-[#00F08B] animate-pulse" />
          Beta
        </span>
      </div>

      {/* Eyebrow label */}
      <div className="mb-4 inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#35256A]/20 bg-[#35256A]/5 text-[#35256A] text-xs font-semibold tracking-wider uppercase">
        <span className="w-1.5 h-1.5 rounded-full bg-[#00F08B]" />
        AI-Powered Dev.to Scanner
      </div>

      {/* Main headline */}
      <h1
        className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold leading-[1.05] tracking-tight text-balance text-foreground"
        style={{ fontFamily: "var(--font-display, 'Syne', sans-serif)" }}
      >
        Let{" "}
        <span
          className="relative inline-block"
          style={{
            WebkitTextStroke: "2px #35256A",
            color: "transparent",
          }}
        >
          AI
        </span>{" "}
        scan{" "}
        <span
          className="relative inline-block px-2"
          style={{
            background: "linear-gradient(135deg, #35256A 0%, #5B3FA8 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
          }}
        >
          Dev.to
        </span>
        <br className="hidden sm:block" />
        <span> feeds</span>{" "}
        <span className="relative">
          for you
          {/* Underline accent */}
          <svg
            className="absolute -bottom-2 left-0 w-full"
            viewBox="0 0 200 8"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            preserveAspectRatio="none"
          >
            <path
              d="M2 5.5C40 2 100 1 198 5.5"
              stroke="#00F08B"
              strokeWidth="3"
              strokeLinecap="round"
            />
          </svg>
        </span>
      </h1>

      {/* Subheading */}
      <p className="mt-6 max-w-xl text-sm sm:text-base text-muted-foreground leading-relaxed text-balance">
        Track trends, surface insights, and stay ahead of the dev community — without scrolling for hours.
      </p>
    </header>
  )
}
