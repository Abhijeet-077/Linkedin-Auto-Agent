import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, Users, MessageSquare, Heart, RefreshCw } from "lucide-react";
import { motion } from "framer-motion";
import { Seo } from "@/components/Seo";
import { useEffect, useState } from "react";
import { getAnalytics, createNewPost } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";

interface AnalyticsData {
  metrics: Array<{
    label: string;
    value: string;
    change: string;
    icon: string;
  }>;
  recentPosts: Array<{
    id: number;
    title: string;
    reach: string;
    engagement: string;
    date: string;
  }>;
}

const iconMap = {
  TrendingUp,
  Users,
  MessageSquare,
  Heart,
};

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [creatingPost, setCreatingPost] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const response = await getAnalytics();

      // Transform backend data to frontend format
      const backendData = response.analytics || response;

      const transformedData = {
        metrics: [
          {
            label: "Total Posts",
            value: backendData.total_posts?.toString() || "0",
            change: "+12%",
            icon: "TrendingUp"
          },
          {
            label: "Engagement Rate",
            value: `${backendData.engagement_rate || 0}%`,
            change: "+8%",
            icon: "Heart"
          },
          {
            label: "Total Likes",
            value: backendData.total_likes?.toString() || "0",
            change: "+15%",
            icon: "Users"
          },
          {
            label: "Growth Rate",
            value: `${backendData.growth_rate || 0}%`,
            change: "+5%",
            icon: "MessageSquare"
          }
        ],
        recentPosts: [
          {
            id: "1",
            content: "Sample LinkedIn post about AI trends and business transformation. This post demonstrates the power of AI-driven content creation...",
            engagement: {
              likes: backendData.total_likes || 45,
              comments: backendData.total_comments || 8,
              shares: backendData.total_shares || 3
            },
            date: new Date().toISOString()
          },
          {
            id: "2",
            content: "Leadership insights for modern professionals. Building effective teams in the digital age requires...",
            engagement: {
              likes: 32,
              comments: 5,
              shares: 2
            },
            date: new Date(Date.now() - 86400000).toISOString()
          }
        ]
      };

      setAnalyticsData(transformedData);
    } catch (error) {
      console.error("Failed to load analytics:", error);
      toast({
        title: "Failed to load analytics",
        description: "Please check your connection and try again.",
        variant: "destructive",
      });

      // Fallback to empty state for production
      setAnalyticsData({
        metrics: [
          { label: "Total Reach", value: "0", change: "0%", icon: "TrendingUp" },
          { label: "Followers", value: "0", change: "0%", icon: "Users" },
          { label: "Engagement", value: "0", change: "0%", icon: "MessageSquare" },
          { label: "Likes", value: "0", change: "0%", icon: "Heart" },
        ],
        recentPosts: [],
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNewPost = async () => {
    try {
      setCreatingPost(true);
      const result = await createNewPost("Professional insights and industry trends");

      if (result.success) {
        toast({
          title: "Post created successfully!",
          description: "Your new post has been generated. Redirecting to pipeline...",
        });

        // Redirect to pipeline page
        navigate("/pipeline");
      } else {
        throw new Error(result.error || "Failed to create post");
      }
    } catch (error) {
      toast({
        title: "Failed to create post",
        description: error instanceof Error ? error.message : "Please try again.",
        variant: "destructive",
      });
    } finally {
      setCreatingPost(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (loading) {
    return (
      <motion.main
        className="container py-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-center min-h-[400px]">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          >
            <RefreshCw className="w-8 h-8 text-primary" />
          </motion.div>
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
      <Seo title="Analytics Dashboard | InfluenceOS" description="Track performance and insights for your content." canonicalPath="/analytics" />
      
      <motion.h1 
        className="mb-6 text-3xl font-bold tracking-tight"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        Analytics Dashboard
      </motion.h1>

      <div className="space-y-6">
        {/* Loading State */}
        {loading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-muted/30 rounded-lg animate-pulse" />
            ))}
          </div>
        ) : (
          <>
            {/* Metrics Grid */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {analyticsData?.metrics?.map((metric, idx) => {
            const IconComponent = iconMap[metric.icon as keyof typeof iconMap] || TrendingUp;
            return (
            <motion.div
              key={metric.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * idx }}
            >
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">{metric.label}</p>
                      <motion.p 
                        className="text-2xl font-bold"
                        initial={{ scale: 0.9 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.3 + idx * 0.05 }}
                      >
                        {metric.value}
                      </motion.p>
                      <Badge variant="secondary" className="mt-1">
                        {metric.change}
                      </Badge>
                    </div>
                    <IconComponent className="h-8 w-8 text-muted-foreground" />
                  </div>
                </CardContent>
              </Card>
            </motion.div>
            );
          })}
        </div>

        {/* Recent Posts */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Recent Posts Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analyticsData?.recentPosts.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <p>No recent posts available.</p>
                    <p className="text-sm mt-2">Start creating content to see analytics here.</p>
                  </div>
                ) : (
                  analyticsData?.recentPosts?.map((post, idx) => (
                  <motion.div
                    key={post.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + idx * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-lg border"
                  >
                    <div>
                      <h3 className="font-medium">{post.title}</h3>
                      <p className="text-sm text-muted-foreground">{post.date}</p>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span>{post.reach} reach</span>
                      <Badge variant="outline">{post.engagement} engagement</Badge>
                    </div>
                  </motion.div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
        </>
        )}

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="text-center"
        >
          <Card>
            <CardContent className="p-8">
              <h2 className="text-xl font-semibold mb-2">Ready to create more content?</h2>
              <p className="text-muted-foreground mb-4">Use the pipeline to generate your next viral post.</p>
              <Button
                variant="glow-accent"
                onClick={handleCreateNewPost}
                disabled={creatingPost}
              >
                {creatingPost ? "Creating..." : "Create New Post"}
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </motion.main>
  );
};

export default Analytics;