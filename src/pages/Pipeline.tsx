import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AgentTimeline, type Step } from "@/components/pipeline/AgentTimeline";
import { ContentPreview } from "@/components/pipeline/ContentPreview";
import { Scheduler } from "@/components/pipeline/Scheduler";
import { startPipeline, type PipelineEvent } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { Seo } from "@/components/Seo";

const initialSteps: Step[] = [
  { key: "draft", label: "Drafting post text", status: "pending" },
  { key: "image", label: "Generating image", status: "pending" },
  { key: "hashtags", label: "Optimizing hashtags", status: "pending" },
];

const Pipeline = () => {
  const [topic, setTopic] = useState("");
  const [steps, setSteps] = useState<Step[]>(initialSteps);
  const [text, setText] = useState<string | undefined>(undefined);
  const [imageUrl, setImageUrl] = useState<string | undefined>(undefined);
  const [hashtags, setHashtags] = useState<string[] | undefined>(undefined);
  const [jobId, setJobId] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    // reset preview when topic changes
    setSteps(initialSteps);
    setText(undefined);
    setImageUrl(undefined);
    setHashtags(undefined);
    setJobId(null);
  }, [topic]);

  const onEvent = (e: PipelineEvent) => {
    if (e.type === "status") {
      setSteps((prev) => prev.map((s) => (s.key === e.payload.step ? { ...s, status: e.payload.status } : s)));
    }
    if (e.type === "text") setText(e.payload.text);
    if (e.type === "image") setImageUrl(e.payload.url);
    if (e.type === "hashtags") setHashtags(e.payload.tags);
    if (e.type === "complete") {
      toast({ title: "Generation complete", description: "Your post is ready to schedule." });
    }
    if (e.type === "error") {
      toast({ title: "Pipeline error", description: e.payload.message });
    }
  };

  const handleGenerate = () => {
    if (!topic.trim()) {
      toast({ title: "Enter a topic", description: "Please provide a topic to generate content." });
      return;
    }
    setSteps((prev) => prev.map((s, i) => (i === 0 ? { ...s, status: "running" } : s)));
    const { jobId } = startPipeline(topic.trim(), onEvent);
    setJobId(jobId);
  };

  return (
    <main className="container py-8">
      <Seo
        title="One-Click Content Pipeline | InfluenceOS"
        description="Generate social posts with AI text, image, and hashtags—Emergent-style UI with real-time progress."
        canonicalPath="/pipeline"
      />
      <h1 className="mb-6 text-3xl font-bold tracking-tight">One-Click Content Pipeline</h1>

      <div className="grid gap-6 md:grid-cols-2">
        <section className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Topic</CardTitle>
            </CardHeader>
            <CardContent className="flex items-center gap-3">
              <Input
                placeholder="e.g., How AI boosts creator productivity"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
              <Button onClick={handleGenerate} className="hover-scale">Generate</Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Agent Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <AgentTimeline steps={steps} />
            </CardContent>
          </Card>
        </section>

        <section className="space-y-4">
          <ContentPreview text={text} imageUrl={imageUrl} hashtags={hashtags} />
          <Scheduler onSchedule={async () => { /* integrate with backend later */ }} />
        </section>
      </div>
    </main>
  );
};

export default Pipeline;
