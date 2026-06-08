import type { Metadata } from 'next'
import { Geist, Geist_Mono, Syne } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

const _geist = Geist({ subsets: ["latin"] });
const _geistMono = Geist_Mono({ subsets: ["latin"] });
const _syne = Syne({ subsets: ["latin"], variable: "--font-display", weight: ["700", "800"] });

export const metadata: Metadata = {
  title: 'Dev.to Analyzer',
  description: 'Analyze Dev.to posts with AI-powered insights',
  generator: 'v0.app',
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans antialiased ${_syne.variable}`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
