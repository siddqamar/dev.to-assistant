import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"

import DevToAnalyzer from "./page"


const apiResult = [
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

describe("DevToAnalyzer page", () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it("fetches analysis results with the selected filters", async () => {
    const user = userEvent.setup()
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => apiResult,
    })
    vi.stubGlobal("fetch", fetchMock)

    render(<DevToAnalyzer />)

    await user.clear(screen.getByPlaceholderText("e.g. webdev, python, react"))
    await user.type(screen.getByPlaceholderText("e.g. webdev, python, react"), "fastapi")
    await user.clear(screen.getByRole("spinbutton"))
    await user.type(screen.getByRole("spinbutton"), "4")
    await user.click(screen.getByRole("button", { name: "Analyze Posts" }))

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "http://127.0.0.1:8000/api/analyze?tag=fastapi&pages=4"
      )
    )
    expect((await screen.findAllByText("Grace Hopper")).length).toBeGreaterThan(0)
    expect(screen.getByRole("link", { name: "Repo" })).toHaveAttribute(
      "href",
      "https://github.com/acme/api"
    )
  })

  it("shows an error message when the API request fails", async () => {
    const user = userEvent.setup()
    const consoleErrorSpy = vi.spyOn(console, "error").mockImplementation(() => {})
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }))

    render(<DevToAnalyzer />)

    await user.click(screen.getByRole("button", { name: "Analyze Posts" }))

    expect(await screen.findByText("Failed to fetch data from API")).toBeInTheDocument()
    expect(consoleErrorSpy).toHaveBeenCalled()
  })
})
