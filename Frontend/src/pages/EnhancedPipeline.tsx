import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { startPipeline, generateIntelligentContent, type PipelineEvent, type UserProfile, type ContentGenerationRequest } from "../lib/api";
import { AgentTimeline, type Step } from "@/components/pipeline/AgentTimeline";
import { ContentPreview } from "@/components/pipeline/ContentPreview";
import { Scheduler } from "@/components/pipeline/Scheduler";
import { useToast } from "@/hooks/use-toast";
import { Seo } from "@/components/Seo";
import { 
  Sparkles, 
  Wand2, 
  Calendar, 
  Share2, 
  TrendingUp, 
  Brain, 
  Target, 
  Zap, 
  Settings,
  User,
  Briefcase,
  Star,
  Clock,
  BarChart3
} from "lucide-react";

const initialSteps: Step[] = [
  { key: "analysis", label: "Analyzing industry trends", status: "pending" },
  { key: "draft", label: "Crafting intelligent content", status: "pending" },
  { key: "image", label: "Generating professional image", status: "pending" },
  { key: "hashtags", label: "Optimizing hashtags", status: "pending" },
  { key: "optimization", label: "Final optimization", status: "pending" },
];

const EnhancedPipeline = () => {
  const [topic, setTopic] = useState("");
  const [steps, setSteps] = useState<Step[]>(initialSteps);
  const [text, setText] = useState<string | undefined>(undefined);
  const [imageUrl, setImageUrl] = useState<string | undefined>(undefined);
  const [hashtags, setHashtags] = useState<string[] | undefined>(undefined);
  const [jobId, setJobId] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [useIntelligentMode, setUseIntelligentMode] = useState(true);
  const [showAdvancedSettings, setShowAdvancedSettings] = useState(false);
  
  // User profile state
  const [userProfile, setUserProfile] = useState<UserProfile>({
    industry: "Technology",
    role: "Professional",
    experience_level: "Mid-level",
    interests: ["Innovation", "Leadership", "Growth"],
    brand_voice: "professional",
    timezone: "UTC"
  });
  
  const [contentType, setContentType] = useState<'text' | 'carousel' | 'poll' | 'article'>('text');
  const [targetAudience, setTargetAudience] = useState('professional');
  
  const { toast } = useToast();

  // Check if any step is currently running
  const hasRunningStep = steps.some(step => step.status === "running");

  useEffect(() => {
    // Reset preview when topic changes
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
    } else if (e.type === "text") {
      setText(e.payload.text);
    } else if (e.type === "image") {
      setImageUrl(e.payload.url);
    } else if (e.type === "hashtags") {
      setHashtags(e.payload.tags);
    } else if (e.type === "complete") {
      toast({
        title: "Content Generated Successfully! 🎉",
        description: "Your AI-powered content is ready to share.",
      });
    } else if (e.type === "error") {
      toast({
        title: "Generation Failed",
        description: e.payload.message,
        variant: "destructive",
      });
    }
  };

  const handleGenerate = async () => {
    if (!topic.trim()) {
      toast({
        title: "Topic Required",
        description: "Please enter a topic to generate content.",
        variant: "destructive",
      });
      return;
    }

    try {
      // Reset steps to initial state
      setSteps(initialSteps);
      setText(undefined);
      setImageUrl(undefined);
      setHashtags(undefined);
      setIsGenerating(true);

      // Start the pipeline - this will handle all the steps automatically
      const { jobId: newJobId, cancel } = startPipeline(topic.trim(), onEvent);
      setJobId(newJobId);

    } catch (error) {
      console.error('Content generation failed:', error);
      setIsGenerating(false);
      toast({
        title: "Generation Failed",
        description: "Failed to start content generation. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleCancel = () => {
    // Implementation for canceling generation
    setIsGenerating(false);
    setSteps(initialSteps);
    setJobId(null);
    toast({
      title: "Generation Cancelled",
      description: "Content generation has been stopped.",
    });
  };

  return (
    <>
      <Seo 
        title="AI Content Pipeline - InfluenceOS" 
        description="Generate intelligent LinkedIn content with AI-powered analysis and optimization"
      />
      
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
        <div className="container mx-auto px-4 py-8">
          {/* Header Section */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-8"
          >
            <div className="inline-flex items-center gap-2 mb-4">
              <div className="relative">
                <Brain className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                <motion.div
                  className="absolute inset-0 bg-blue-400 rounded-full blur-lg opacity-30"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
              </div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                AI Content Pipeline
              </h1>
            </div>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Generate intelligent, industry-specific LinkedIn content with advanced AI analysis and optimization
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Input & Settings */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="lg:col-span-1 space-y-6"
            >
              {/* Topic Input Card */}
              <Card className="relative overflow-hidden border-2 border-blue-200 dark:border-blue-800">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/50 dark:to-indigo-950/50" />
                <CardHeader className="relative">
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5 text-blue-600" />
                    Content Topic
                  </CardTitle>
                  <CardDescription>
                    What would you like to create content about?
                  </CardDescription>
                </CardHeader>
                <CardContent className="relative space-y-4">
                  <div className="space-y-2">
                    <Input
                      placeholder="e.g., AI in business transformation, Leadership lessons, Industry trends..."
                      value={topic}
                      onChange={(e) => setTopic(e.target.value)}
                      className="text-lg h-12"
                      disabled={isGenerating}
                    />
                  </div>
                  
                  {/* Intelligent Mode Toggle */}
                  <div className="flex items-center justify-between p-4 bg-white/50 dark:bg-slate-800/50 rounded-lg border">
                    <div className="flex items-center gap-2">
                      <Sparkles className="h-4 w-4 text-yellow-500" />
                      <Label htmlFor="intelligent-mode" className="font-medium">
                        Intelligent Mode
                      </Label>
                    </div>
                    <Switch
                      id="intelligent-mode"
                      checked={useIntelligentMode}
                      onCheckedChange={setUseIntelligentMode}
                      disabled={isGenerating}
                    />
                  </div>

                  {/* Advanced Settings Toggle */}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowAdvancedSettings(!showAdvancedSettings)}
                    className="w-full"
                    disabled={isGenerating}
                  >
                    <Settings className="h-4 w-4 mr-2" />
                    {showAdvancedSettings ? 'Hide' : 'Show'} Advanced Settings
                  </Button>
                </CardContent>
              </Card>

              {/* Advanced Settings */}
              <AnimatePresence>
                {showAdvancedSettings && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                  >
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <User className="h-5 w-5" />
                          Profile Settings
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <Label>Industry</Label>
                            <Select
                              value={userProfile.industry}
                              onValueChange={(value) => setUserProfile(prev => ({ ...prev, industry: value }))}
                              disabled={isGenerating}
                            >
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="Technology">Technology</SelectItem>
                                <SelectItem value="Marketing">Marketing</SelectItem>
                                <SelectItem value="Finance">Finance</SelectItem>
                                <SelectItem value="Healthcare">Healthcare</SelectItem>
                                <SelectItem value="Education">Education</SelectItem>
                                <SelectItem value="Consulting">Consulting</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                          
                          <div className="space-y-2">
                            <Label>Role</Label>
                            <Select
                              value={userProfile.role}
                              onValueChange={(value) => setUserProfile(prev => ({ ...prev, role: value }))}
                              disabled={isGenerating}
                            >
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="CEO">CEO</SelectItem>
                                <SelectItem value="Manager">Manager</SelectItem>
                                <SelectItem value="Professional">Professional</SelectItem>
                                <SelectItem value="Consultant">Consultant</SelectItem>
                                <SelectItem value="Entrepreneur">Entrepreneur</SelectItem>
                                <SelectItem value="Specialist">Specialist</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <Label>Content Type</Label>
                          <Select
                            value={contentType}
                            onValueChange={(value: any) => setContentType(value)}
                            disabled={isGenerating}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="text">Text Post</SelectItem>
                              <SelectItem value="carousel">Carousel</SelectItem>
                              <SelectItem value="poll">Poll</SelectItem>
                              <SelectItem value="article">Article</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>

                        <div className="space-y-2">
                          <Label>Brand Voice</Label>
                          <Select
                            value={userProfile.brand_voice}
                            onValueChange={(value) => setUserProfile(prev => ({ ...prev, brand_voice: value }))}
                            disabled={isGenerating}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="professional">Professional</SelectItem>
                              <SelectItem value="friendly">Friendly</SelectItem>
                              <SelectItem value="innovative">Innovative</SelectItem>
                              <SelectItem value="educational">Educational</SelectItem>
                              <SelectItem value="inspirational">Inspirational</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Generate Button */}
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button
                  onClick={handleGenerate}
                  disabled={isGenerating || !topic.trim()}
                  className="w-full h-14 text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  {isGenerating ? (
                    <>
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="mr-2"
                      >
                        <Zap className="h-5 w-5" />
                      </motion.div>
                      Generating...
                    </>
                  ) : (
                    <>
                      <Wand2 className="h-5 w-5 mr-2" />
                      {useIntelligentMode ? 'Generate Intelligent Content' : 'Generate Content'}
                    </>
                  )}
                </Button>
              </motion.div>

              {isGenerating && (
                <Button
                  onClick={handleCancel}
                  variant="outline"
                  className="w-full"
                >
                  Cancel Generation
                </Button>
              )}
            </motion.div>

            {/* Middle Column - Agent Timeline */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="lg:col-span-1"
            >
              <Card className="h-fit">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5 text-green-600" />
                    AI Agent Timeline
                  </CardTitle>
                  <CardDescription>
                    Watch the AI analyze and create your content
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <AgentTimeline steps={steps} />
                </CardContent>
              </Card>
            </motion.div>

            {/* Right Column - Content Preview & Scheduler */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-1 space-y-6"
            >
              <ContentPreview
                text={text}
                imageUrl={imageUrl}
                hashtags={hashtags}
                isGenerating={hasRunningStep}
              />
              
              <Scheduler
                content={{ text, imageUrl, hashtags }}
                disabled={!text || hasRunningStep}
              />
            </motion.div>
          </div>
        </div>
      </div>
    </>
  );
};

export default EnhancedPipeline;
