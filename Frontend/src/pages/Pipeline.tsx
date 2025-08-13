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
import { motion } from "framer-motion";

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
  const [isGenerating, setIsGenerating] = useState(false);
  const { toast } = useToast();

  // Check if any step is currently running
  const hasRunningStep = steps.some(step => step.status === "running");

  useEffect(() => {
    // reset preview when topic changes
    setSteps(initialSteps);
    setText(undefined);
    setImageUrl(undefined);
    setHashtags(undefined);
    setJobId(null);
    setIsGenerating(false);
  }, [topic]);

  // Update generating state based on steps
  useEffect(() => {
    const hasRunning = steps.some(step => step.status === "running");
    setIsGenerating(hasRunning);
  }, [steps]);

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
    <motion.main
      className={`container py-8 relative ${isGenerating ? 'ai-processing-bg' : ''}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Dynamic background particles during generation */}
      {isGenerating && (
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
          {Array.from({ length: 20 }).map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 bg-primary/10 rounded-full"
              initial={{
                opacity: 0,
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight
              }}
              animate={{
                opacity: [0, 0.6, 0],
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                scale: [0, 1, 0]
              }}
              transition={{
                duration: 4,
                delay: i * 0.2,
                repeat: Infinity,
                repeatDelay: Math.random() * 3
              }}
            />
          ))}
        </div>
      )}
      <Seo
        title="One-Click Content Pipeline | InfluenceOS"
        description="Generate social posts with AI text, image, and hashtags—Emergent-style UI with real-time progress."
        canonicalPath="/pipeline"
      />
      <motion.h1
        className={`mb-6 text-3xl font-bold tracking-tight relative z-10 ${isGenerating ? 'gradient-text' : ''}`}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        One-Click Content Pipeline
        {isGenerating && (
          <motion.span
            className="ml-3 inline-block"
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            ✨
          </motion.span>
        )}
      </motion.h1>

      <div className="grid gap-6 lg:grid-cols-2 xl:gap-8">
        <motion.section
          className="space-y-4 relative z-10 w-full"
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card className={`card-glow ${isGenerating ? 'ai-processing' : ''}`}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                Topic
                {isGenerating && (
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 1, repeat: Infinity }}
                    className="w-2 h-2 bg-primary rounded-full"
                  />
                )}
              </CardTitle>
            </CardHeader>
            <CardContent className="flex items-center gap-3">
              <Input
                placeholder="e.g., How AI boosts creator productivity"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
                className={`transition-all duration-300 ${isGenerating ? 'glow-primary' : ''}`}
                disabled={isGenerating}
              />
              <motion.div
                whileHover={{ scale: isGenerating ? 1 : 1.05 }}
                whileTap={{ scale: isGenerating ? 1 : 0.95 }}
              >
                <Button
                  onClick={handleGenerate}
                  variant={isGenerating ? "shimmer" : "glow"}
                  disabled={isGenerating}
                  className="relative overflow-hidden"
                >
                  {isGenerating ? (
                    <>
                      <motion.span
                        animate={{ opacity: [1, 0.5, 1] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                      >
                        Generating...
                      </motion.span>
                    </>
                  ) : (
                    "Generate"
                  )}
                </Button>
              </motion.div>
            </CardContent>
          </Card>

          <Card className={`card-glow ${hasRunningStep ? 'gradient-border' : ''}`}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                Agent Timeline
                {hasRunningStep && (
                  <motion.div
                    animate={{
                      scale: [1, 1.3, 1],
                      opacity: [0.5, 1, 0.5]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="w-2 h-2 bg-primary rounded-full"
                  />
                )}
              </CardTitle>
            </CardHeader>
            <CardContent className="relative">
              <AgentTimeline steps={steps} />
            </CardContent>
          </Card>
        </motion.section>

        <motion.section
          className="space-y-4 relative z-10 w-full"
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <ContentPreview text={text} imageUrl={imageUrl} hashtags={hashtags} isGenerating={isGenerating} />
          <Scheduler text={text} imageUrl={imageUrl} hashtags={hashtags} />
        </motion.section>
      </div>
    </motion.main>
  );
};

export default Pipeline;
