import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { LoadingScreen } from "@/components/ui/loading";
import { User, Camera, FileText, Target, Zap } from "lucide-react";
import { motion } from "framer-motion";
import { Seo } from "@/components/Seo";
import { useEffect, useState, useCallback } from "react";
import { getProfileAnalysis, connectLinkedIn, createProfile } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

interface ProfileData {
  score: number;
  recommendations: Array<{
    icon: string;
    title: string;
    description: string;
    priority: "high" | "medium" | "low";
  }>;
  stats: Array<{
    label: string;
    score: number;
    color: string;
  }>;
}

const iconMap = {
  Camera,
  FileText,
  Target,
  Zap,
};

const Profile = () => {
  const [profileData, setProfileData] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const { toast } = useToast();

  const loadProfileAnalysis = useCallback(async () => {
    try {
      setLoading(true);
      const response = await getProfileAnalysis();

      // Transform backend data to frontend format
      const backendData = response.analysis || response;

      const transformedData = {
        score: backendData.profile_score || 0,
        recommendations: (backendData.recommendations || []).map((rec: string, idx: number) => ({
          icon: ["Camera", "FileText", "Target", "Zap"][idx % 4],
          title: `Recommendation ${idx + 1}`,
          description: rec,
          priority: idx < 2 ? "high" : "medium" as "high" | "medium" | "low"
        })),
        stats: [
          { label: "Profile Completeness", score: backendData.completeness || 0, color: "bg-blue-500" },
          { label: "Content Quality", score: backendData.profile_score || 0, color: "bg-green-500" },
          { label: "Posting Frequency", score: 75, color: "bg-yellow-500" },
          { label: "Engagement Rate", score: backendData.engagement_potential || 0, color: "bg-purple-500" },
        ]
      };

      setProfileData(transformedData);
    } catch (error) {
      // Remove console.error for production
      toast({
        title: "Failed to load profile analysis",
        description: "Please check your connection and try again.",
        variant: "destructive",
      });

      // Fallback to empty state for production
      setProfileData({
        score: 0,
        recommendations: [
          { icon: "Camera", title: "Connect your LinkedIn profile", description: "Link your account to get personalized recommendations", priority: "high" },
          { icon: "Target", title: "Complete profile setup", description: "Add your professional information", priority: "high" },
        ],
        stats: [
          { label: "Profile Completeness", score: 0, color: "bg-gray-500" },
          { label: "Content Quality", score: 0, color: "bg-gray-500" },
          { label: "Posting Frequency", score: 0, color: "bg-gray-500" },
          { label: "Engagement Rate", score: 0, color: "bg-gray-500" },
        ],
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const handleConnectLinkedIn = async () => {
    try {
      setConnecting(true);
      const result = await connectLinkedIn();

      if (result.success) {
        toast({
          title: "LinkedIn connection initiated",
          description: "Please complete the authorization process.",
        });

        // In a real app, you would redirect to the auth URL
        if (result.auth_url) {
          window.open(result.auth_url, '_blank');
        }
      } else {
        throw new Error("Failed to initiate LinkedIn connection");
      }
    } catch (error) {
      toast({
        title: "Connection failed",
        description: error instanceof Error ? error.message : "Please try again.",
        variant: "destructive",
      });
    } finally {
      setConnecting(false);
    }
  };

  const handleRunAnalysis = async () => {
    try {
      setAnalyzing(true);
      await loadProfileAnalysis();
      toast({
        title: "Analysis completed",
        description: "Your profile analysis has been updated.",
      });
    } catch (error) {
      toast({
        title: "Analysis failed",
        description: "Please try again.",
        variant: "destructive",
      });
    } finally {
      setAnalyzing(false);
    }
  };

  useEffect(() => {
    loadProfileAnalysis();
  }, [loadProfileAnalysis]);

  if (loading) {
    return (
      <motion.main
        className="container py-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <LoadingScreen text="Analyzing your profile..." />
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
                  {profileData?.score || 0}/100
                </motion.div>
                <Progress value={profileData?.score || 0} className="w-full mb-4" />
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
              {profileData?.stats.map((stat, idx) => (
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
              {profileData?.recommendations.map((rec, idx) => {
                const IconComponent = iconMap[rec.icon as keyof typeof iconMap] || Target;
                return (
                <motion.div
                  key={rec.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 + idx * 0.1 }}
                  className="flex items-start gap-3 p-4 rounded-lg border"
                >
                  <IconComponent className="h-5 w-5 mt-0.5 text-primary" />
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
                );
              })}
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="mt-4 space-y-2"
          >
            <Button
              variant="glow"
              className="w-full"
              onClick={handleRunAnalysis}
              disabled={analyzing}
            >
              {analyzing ? "Analyzing..." : "Run Full Analysis"}
            </Button>
            <Button
              variant="outline"
              className="w-full hover:glow-primary"
              onClick={handleConnectLinkedIn}
              disabled={connecting}
            >
              {connecting ? "Connecting..." : "Connect LinkedIn"}
            </Button>
          </motion.div>
        </motion.div>
      </div>
    </motion.main>
  );
};

export default Profile;