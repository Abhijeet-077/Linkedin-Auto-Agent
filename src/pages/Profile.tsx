import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { User, Camera, FileText, Target, Zap } from "lucide-react";
import { motion } from "framer-motion";
import { Seo } from "@/components/Seo";

// Mock profile analysis data
const profileScore = 72;
const recommendations = [
  { icon: Camera, title: "Update profile photo", description: "Use a high-quality headshot", priority: "high" },
  { icon: FileText, title: "Enhance bio", description: "Add more keywords and call-to-action", priority: "medium" },
  { icon: Target, title: "Define target audience", description: "Specify your ideal follower", priority: "high" },
  { icon: Zap, title: "Post consistently", description: "Maintain regular posting schedule", priority: "low" },
];

const profileStats = [
  { label: "Bio Optimization", score: 85, color: "bg-green-500" },
  { label: "Content Quality", score: 78, color: "bg-blue-500" },
  { label: "Posting Frequency", score: 65, color: "bg-yellow-500" },
  { label: "Engagement Rate", score: 82, color: "bg-purple-500" },
];

const Profile = () => {
  return (
    <motion.main 
      className="container py-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Seo title="Profile Optimization | InfluenceOS" description="Optimize your profile for reach and conversion." canonicalPath="/profile" />
      
      <motion.h1 
        className="mb-6 text-3xl font-bold tracking-tight"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        Profile Optimization
      </motion.h1>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Profile Score */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Profile Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.5, type: "spring" }}
                  className="text-4xl font-bold text-primary mb-2"
                >
                  {profileScore}/100
                </motion.div>
                <Progress value={profileScore} className="w-full mb-4" />
                <p className="text-sm text-muted-foreground">
                  Your profile is performing well but has room for improvement
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Profile Stats */}
          <Card className="mt-4">
            <CardHeader>
              <CardTitle>Detailed Analysis</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {profileStats.map((stat, idx) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 + idx * 0.1 }}
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium">{stat.label}</span>
                    <span className="text-sm text-muted-foreground">{stat.score}%</span>
                  </div>
                  <Progress value={stat.score} className="h-2" />
                </motion.div>
              ))}
            </CardContent>
          </Card>
        </motion.div>

        {/* Recommendations */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Recommendations</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {recommendations.map((rec, idx) => (
                <motion.div
                  key={rec.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 + idx * 0.1 }}
                  className="flex items-start gap-3 p-4 rounded-lg border"
                >
                  <rec.icon className="h-5 w-5 mt-0.5 text-primary" />
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h3 className="font-medium">{rec.title}</h3>
                      <Badge 
                        variant={rec.priority === "high" ? "destructive" : 
                               rec.priority === "medium" ? "default" : "secondary"}
                      >
                        {rec.priority}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">{rec.description}</p>
                  </div>
                </motion.div>
              ))}
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="mt-4 space-y-2"
          >
            <Button className="w-full">Run Full Analysis</Button>
            <Button variant="outline" className="w-full">Export Report</Button>
          </motion.div>
        </motion.div>
      </div>
    </motion.main>
  );
};

export default Profile;