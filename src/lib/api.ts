export type PipelineEvent =
  | { type: "status"; payload: { step: string; status: "pending" | "running" | "done" | "error" } }
  | { type: "text"; payload: { text: string } }
  | { type: "image"; payload: { url: string } }
  | { type: "hashtags"; payload: { tags: string[] } }
  | { type: "complete" }
  | { type: "error"; payload: { message: string } };

export const USE_MOCK_API = true; // Toggle to false when backend is ready

export function startPipeline(
  topic: string,
  onEvent: (e: PipelineEvent) => void
): { jobId: string; cancel: () => void } {
  if (USE_MOCK_API) {
    const timeouts: number[] = [];
    const schedule = (ms: number, cb: () => void) => {
      const id = window.setTimeout(cb, ms);
      timeouts.push(id);
    };

    // Simulated event flow
    schedule(300, () => onEvent({ type: "status", payload: { step: "draft", status: "running" } }));
    schedule(1400, () => onEvent({ type: "text", payload: { text: `Here are insights about ${topic} — a concise, compelling post crafted for engagement.` } }));
    schedule(1500, () => onEvent({ type: "status", payload: { step: "draft", status: "done" } }));

    schedule(1600, () => onEvent({ type: "status", payload: { step: "image", status: "running" } }));
    schedule(2800, () => onEvent({ type: "image", payload: { url: "/placeholder.svg" } }));
    schedule(2900, () => onEvent({ type: "status", payload: { step: "image", status: "done" } }));

    schedule(3000, () => onEvent({ type: "status", payload: { step: "hashtags", status: "running" } }));
    schedule(3600, () => onEvent({ type: "hashtags", payload: { tags: ["#influenceOS", "#growth", "#automation", "#AI", "#productivity"] } }));
    schedule(3800, () => onEvent({ type: "status", payload: { step: "hashtags", status: "done" } }));

    schedule(4000, () => onEvent({ type: "complete" }));

    return {
      jobId: `mock-${Date.now()}`,
      cancel: () => timeouts.forEach(clearTimeout),
    };
  }

  // Real backend (same-origin FastAPI)
  const controller = new AbortController();
  const jobId = `job-${Date.now()}`;

  // Example SSE endpoint; adjust to your backend when ready.
  const es = new EventSource(`/api/v1/pipeline/stream?topic=${encodeURIComponent(topic)}`);
  es.onmessage = (ev) => {
    try {
      const e: PipelineEvent = JSON.parse(ev.data);
      onEvent(e);
    } catch (err) {
      console.error("Malformed event:", err);
    }
  };
  es.onerror = () => {
    onEvent({ type: "error", payload: { message: "Connection error" } });
    es.close();
  };

  return {
    jobId,
    cancel: () => {
      controller.abort();
      es.close();
    },
  };
}
