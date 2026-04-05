import type { PostData } from "./results-section"

interface ResultsTableProps {
  data: PostData[]
}

export function ResultsTable({ data }: ResultsTableProps) {
  return (
    <>
      {/* Desktop Table View */}
      <div className="hidden md:block bg-card border border-border overflow-x-auto rounded-lg">
        <table className="w-full border-collapse text-left text-[13px]">
          <thead>
            <tr>
              <th className="p-4 border-b border-[var(--table-border)] text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground bg-card sticky top-0 z-10">
                Author &amp; Post
              </th>
              <th className="p-4 border-b border-[var(--table-border)] text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground bg-card sticky top-0 z-10">
                Extracted Hook
              </th>
              <th className="p-4 border-b border-[var(--table-border)] text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground bg-card sticky top-0 z-10">
                Problem Statement
              </th>
              <th className="p-4 border-b border-[var(--table-border)] text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground bg-card sticky top-0 z-10">
                Proposed Solution
              </th>
              <th className="p-4 border-b border-[var(--table-border)] text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground bg-card sticky top-0 z-10">
                Engagement
              </th>
              <th className="p-4 border-b border-[var(--table-border)] text-[11px] font-semibold uppercase tracking-[0.05em] text-muted-foreground bg-card sticky top-0 z-10">
                URL
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((post) => (
              <tr 
                key={post.id} 
                className="hover:bg-[#FAFAFA] [&:last-child_td]:border-b-0"
              >
                <td className="p-4 border-b border-[var(--table-border)] align-top">
                  <AuthorCell author={post.author} avatar={post.avatar} date={post.date} topic={post.topic} />
                </td>
                <td className="p-4 border-b border-[var(--table-border)] align-top min-w-[200px] max-w-[300px] text-foreground leading-[1.4]">
                  {post.hook}
                </td>
                <td className="p-4 border-b border-[var(--table-border)] align-top min-w-[200px] max-w-[300px] text-foreground leading-[1.4]">
                  {post.problem}
                </td>
                <td className="p-4 border-b border-[var(--table-border)] align-top min-w-[200px] max-w-[300px] text-foreground leading-[1.4]">
                  {post.solution}
                </td>
                <td className="p-4 border-b border-[var(--table-border)] align-top">
                  <EngagementCell reacts={post.reacts} comments={post.comments} />
                </td>
                <td className="p-4 border-b border-[var(--table-border)] align-top w-[60px] text-right">
                  <a 
                    href={post.url} 
                    className="text-[var(--accent-purple)] no-underline font-semibold text-[13px] hover:underline"
                  >
                    View
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Card View */}
      <div className="md:hidden flex flex-col gap-3">
        {data.map((post) => (
          <div key={post.id} className="bg-card border border-border rounded-lg p-4">
            {/* Header */}
            <div className="flex items-center justify-between gap-3 mb-3 pb-3 border-b border-border">
              <div className="flex items-center gap-3">
                <img 
                  src={post.avatar} 
                  alt={`${post.author}'s avatar`} 
                  className="w-10 h-10 rounded-full bg-border object-cover"
                />
                <div className="flex flex-col">
                  <span className="font-semibold text-foreground text-sm">{post.author}</span>
                  <span className="text-[11px] text-muted-foreground">{post.date} • {post.topic}</span>
                </div>
              </div>
              <a 
                href={post.url} 
                className="text-[var(--accent-purple)] no-underline font-semibold text-sm hover:underline"
              >
                View
              </a>
            </div>

            {/* Content */}
            <div className="flex flex-col gap-3 text-sm">
              <div>
                <span className="text-[10px] font-semibold uppercase tracking-[0.05em] text-muted-foreground block mb-1">
                  Hook
                </span>
                <p className="text-foreground leading-relaxed">{post.hook}</p>
              </div>
              <div>
                <span className="text-[10px] font-semibold uppercase tracking-[0.05em] text-muted-foreground block mb-1">
                  Problem
                </span>
                <p className="text-foreground leading-relaxed">{post.problem}</p>
              </div>
              <div>
                <span className="text-[10px] font-semibold uppercase tracking-[0.05em] text-muted-foreground block mb-1">
                  Solution
                </span>
                <p className="text-foreground leading-relaxed">{post.solution}</p>
              </div>
            </div>

            {/* Engagement Footer */}
            <div className="flex items-center gap-4 mt-3 pt-3 border-t border-border">
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <span className="inline-flex items-center px-1.5 py-0.5 bg-[var(--accent-purple)] text-white text-[11px] font-semibold rounded">
                  +{post.reacts}
                </span>
                Reacts
              </div>
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <span className="inline-flex items-center px-1.5 py-0.5 bg-muted-foreground text-white text-[11px] font-semibold rounded">
                  +{post.comments}
                </span>
                Comments
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  )
}

function AuthorCell({ author, avatar, date, topic }: { author: string; avatar: string; date: string; topic: string }) {
  return (
    <div className="flex items-center gap-3 min-w-[180px]">
      <img 
        src={avatar} 
        alt={`${author}'s avatar`} 
        className="w-8 h-8 rounded-full bg-border object-cover"
      />
      <div className="flex flex-col gap-0.5">
        <span className="font-semibold text-foreground">{author}</span>
        <span className="text-[11px] text-muted-foreground">{date} • {topic}</span>
      </div>
    </div>
  )
}

function EngagementCell({ reacts, comments }: { reacts: number; comments: number }) {
  return (
    <div className="min-w-[100px] flex flex-col gap-1.5">
      <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
        <span className="inline-flex items-center px-1.5 py-0.5 bg-[var(--accent-purple)] text-white text-[11px] font-semibold rounded tracking-[0.02em]">
          +{reacts}
        </span>
        Reacts
      </div>
      <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
        <span className="inline-flex items-center px-1.5 py-0.5 bg-muted-foreground text-white text-[11px] font-semibold rounded tracking-[0.02em]">
          +{comments}
        </span>
        Comments
      </div>
    </div>
  )
}
