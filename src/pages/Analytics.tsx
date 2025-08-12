import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, Users, MessageSquare, Heart } from "lucide-react";
import { motion } from "framer-motion";
import { Seo } from "@/components/Seo";

// Mock data for analytics
const metrics = [
  { label: "Total Reach", value: "12.4K", change: "+8.2%", icon: TrendingUp },
  { label: "Followers", value: "3.2K", change: "+12.5%", icon: Users },
  { label: "Engagement", value: "892", change: "+15.3%", icon: MessageSquare },
  { label: "Likes", value: "2.1K", change: "+6.7%", icon: Heart },
];

const recentPosts = [
  { id: 1, title: "AI in Content Creation", reach: "1.2K", engagement: "8.5%", date: "2 days ago" },
  { id: 2, title: "Productivity Tips", reach: "2.1K", engagement: "12.3%", date: "5 days ago" },
  { id: 3, title: "Future of Work", reach: "956", engagement: "6.8%", date: "1 week ago" },
];

const Analytics = () => {
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
        {/* Metrics Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {metrics.map((metric, idx) => (
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
                    <metric.icon className="h-8 w-8 text-muted-foreground" />
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
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
                {recentPosts.map((post, idx) => (
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
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

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
              <Button>Create New Post</Button>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </motion.main>
  );
};

export default Analytics;