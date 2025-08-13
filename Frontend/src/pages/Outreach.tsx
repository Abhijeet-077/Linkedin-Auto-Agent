import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Users, MessageSquare, Send, Calendar, Search } from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { Seo } from "@/components/Seo";
import { getOutreachCampaigns, createOutreachCampaign, getOutreachTemplates } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

// Mock outreach data
const campaigns = [
  { id: 1, name: "Tech Influencer Outreach", status: "active", sent: 45, responses: 12, scheduled: "2024-01-15" },
  { id: 2, name: "Content Creator Collab", status: "draft", sent: 0, responses: 0, scheduled: "2024-01-20" },
  { id: 3, name: "Industry Expert Network", status: "completed", sent: 32, responses: 8, scheduled: "2024-01-10" },
];

const templates = [
  { id: 1, name: "Collaboration Proposal", category: "Partnership" },
  { id: 2, name: "Guest Post Invitation", category: "Content" },
  { id: 3, name: "Podcast Interview", category: "Media" },
];

const Outreach = () => {
  const [newCampaign, setNewCampaign] = useState("");
  const [message, setMessage] = useState("");
  const [campaigns, setCampaigns] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const { toast } = useToast();

  const loadData = async () => {
    try {
      setLoading(true);
      const [campaignsData, templatesData] = await Promise.all([
        getOutreachCampaigns(),
        getOutreachTemplates()
      ]);

      setCampaigns(campaignsData.campaigns || []);
      setTemplates(templatesData.templates || []);
    } catch (error) {
      toast({
        title: "Failed to load data",
        description: "Using fallback data. Please check your connection.",
        variant: "destructive",
      });

      // Fallback to mock data
      setCampaigns([
        { id: 1, name: "Tech Influencer Outreach", status: "active", sent: 45, responses: 12, scheduled: "2024-01-15" },
        { id: 2, name: "Content Creator Collab", status: "draft", sent: 0, responses: 0, scheduled: "2024-01-20" },
        { id: 3, name: "Industry Expert Network", status: "completed", sent: 32, responses: 8, scheduled: "2024-01-10" },
      ]);
      setTemplates([
        { id: 1, name: "Collaboration Proposal", category: "Partnership" },
        { id: 2, name: "Guest Post Invitation", category: "Content" },
        { id: 3, name: "Podcast Interview", category: "Media" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCampaign = async () => {
    if (!newCampaign.trim() || !message.trim()) {
      toast({
        title: "Missing information",
        description: "Please fill in both campaign name and message.",
        variant: "destructive",
      });
      return;
    }

    try {
      setCreating(true);
      const result = await createOutreachCampaign({
        name: newCampaign,
        message: message,
        targets: [] // In a real app, this would come from a target selection UI
      });

      if (result.success) {
        toast({
          title: "Campaign created successfully!",
          description: `Campaign "${newCampaign}" has been created.`,
        });

        // Reset form
        setNewCampaign("");
        setMessage("");

        // Reload campaigns
        await loadData();
      } else {
        throw new Error(result.error || "Failed to create campaign");
      }
    } catch (error) {
      toast({
        title: "Failed to create campaign",
        description: error instanceof Error ? error.message : "Please try again.",
        variant: "destructive",
      });
    } finally {
      setCreating(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <motion.main
        className="flex-1 p-6 space-y-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Loading outreach data...</p>
          </div>
        </div>
      </motion.main>
    );
  }

  return (
    <motion.main 
      className="container py-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Seo title="Outreach Automation (Mock) | InfluenceOS" description="Plan outreach and lead generation with a mock flow." canonicalPath="/outreach" />
      
      <motion.h1 
        className="mb-6 text-3xl font-bold tracking-tight"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        Outreach Automation
      </motion.h1>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Campaign Creation */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Send className="h-5 w-5" />
                Create New Campaign
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Campaign Name</label>
                <Input
                  placeholder="e.g., Q1 Influencer Partnerships"
                  value={newCampaign}
                  onChange={(e) => setNewCampaign(e.target.value)}
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Message Template</label>
                <Textarea
                  placeholder="Hi [NAME], I came across your content on [PLATFORM] and would love to collaborate..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={4}
                />
              </div>
              <div className="flex items-center gap-2">
                <Button
                  onClick={handleCreateCampaign}
                  disabled={creating || !newCampaign.trim() || !message.trim()}
                >
                  <Send className="h-4 w-4 mr-2" />
                  {creating ? "Creating..." : "Create Campaign"}
                </Button>
                <Button variant="outline">Save Template</Button>
              </div>
            </CardContent>
          </Card>

          {/* Active Campaigns */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Campaign Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {campaigns.map((campaign, idx) => (
                  <motion.div
                    key={campaign.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 + idx * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-lg border"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium">{campaign.name}</h3>
                        <Badge 
                          variant={campaign.status === "active" ? "default" : 
                                 campaign.status === "completed" ? "secondary" : "outline"}
                        >
                          {campaign.status}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Send className="h-3 w-3" />
                          {campaign.sent} sent
                        </span>
                        <span className="flex items-center gap-1">
                          <MessageSquare className="h-3 w-3" />
                          {campaign.responses} responses
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {campaign.scheduled}
                        </span>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm">View</Button>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="space-y-6"
        >
          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Quick Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Total Sent</span>
                <span className="font-medium">77</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Response Rate</span>
                <span className="font-medium">26%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Active Campaigns</span>
                <span className="font-medium">1</span>
              </div>
            </CardContent>
          </Card>

          {/* Message Templates */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Message Templates</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {templates.map((template, idx) => (
                  <motion.div
                    key={template.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 + idx * 0.1 }}
                    className="flex items-center justify-between p-3 rounded-lg border hover:bg-accent cursor-pointer"
                  >
                    <div>
                      <p className="font-medium text-sm">{template.name}</p>
                      <p className="text-xs text-muted-foreground">{template.category}</p>
                    </div>
                    <Button variant="ghost" size="sm">Use</Button>
                  </motion.div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4">
                Create Template
              </Button>
            </CardContent>
          </Card>

          {/* Mock Notice */}
          <Card className="border-dashed border-2">
            <CardContent className="p-4 text-center">
              <p className="text-sm text-muted-foreground">
                🚧 This is a mock interface. Real LinkedIn integration coming soon.
              </p>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </motion.main>
  );
};

export default Outreach;