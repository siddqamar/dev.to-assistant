import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"

import { ResultsSection, type PostData } from "./results-section"


const data: PostData[] = [
  {
    id: 1,
    author: "Grace Hopper",
    avatar: "https://images.dev/grace.png",
    date: "2026-07-08",
    topic: "Ship Better Python APIs",
    tech_stack: "FastAPI, Python",
    problem: "Slow sync handlers.",
    solution: "Adopt async IO.",
    github_url: "https://github.com/acme/api",
    reacts: 14,
    comments: 2,
    url: "https://dev.to/example/post",
  },
]

describe("ResultsSection", () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it("copies a readable text summary to the clipboard", async () => {
    const user = userEvent.setup()
    const writeTextMock = vi.mocked(navigator.clipboard.writeText)

    render(<ResultsSection data={data} />)

    await user.click(screen.getByRole("button", { name: /copy data/i }))

    expect(writeTextMock).toHaveBeenCalledWith(
      expect.stringContaining("Grace Hopper - Ship Better Python APIs")
    )
    expect(writeTextMock).toHaveBeenCalledWith(
      expect.stringContaining("GitHub URL: https://github.com/acme/api")
    )
  })

  it("exports the current results as csv", async () => {
    const user = userEvent.setup()
    const createObjectURLMock = vi.mocked(URL.createObjectURL)
    const revokeObjectURLMock = vi.mocked(URL.revokeObjectURL)
    const clickSpy = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => {})

    render(<ResultsSection data={data} />)

    await user.click(screen.getByRole("button", { name: /export csv/i }))

    expect(createObjectURLMock).toHaveBeenCalledTimes(1)
    const blob = createObjectURLMock.mock.calls[0][0] as Blob
    await expect(blob.text()).resolves.toContain('"Grace Hopper"')
    expect(clickSpy).toHaveBeenCalledTimes(1)
    expect(revokeObjectURLMock).toHaveBeenCalledWith("blob:mock-url")
  })
})
