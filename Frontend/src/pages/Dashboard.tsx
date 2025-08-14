import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { getEngagementAnalytics, getContentCalendar, getOptimalPostingTimes, getDateRange, getNextWeekRange } from "../lib/api";
import { useToast } from "@/hooks/use-toast";
import { Seo } from "@/components/Seo";
import {
  BarChart3,
  TrendingUp,
  Users,
  Heart,
  MessageCircle,
  Share2,
  Eye,
  Calendar,
  Clock,
  Target,
  Zap,
  Star,
  Award,
  Activity,
  Sparkles,
  Brain,
  Rocket
} from "lucide-react";

interface AnalyticsData {
  total_metrics: {
    likes: number;
    comments: number;
    shares: number;
    views: number;
    reach: number;
  };
  average_metrics: {
    likes: number;
    comments: number;
    shares: number;
    views: number;
    reach: number;
  };
  engagement_rate: number;
  total_posts: number;
  growth_trends: {
    engagement_growth: number;
    follower_growth: number;
    reach_growth: number;
  };
  insights: string[];
}

const Dashboard = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [calendar, setCalendar] = useState<any>(null);
  const [optimalTimes, setOptimalTimes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [timePeriod, setTimePeriod] = useState('30d');
  const { toast } = useToast();

  useEffect(() => {
    loadDashboardData();
  }, [timePeriod]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load analytics data
      const analyticsResponse = await getEngagementAnalytics('default', timePeriod);
      if (analyticsResponse.success) {
        setAnalytics(analyticsResponse.analytics);
      }

      // Load calendar data for next week
      const { start, end } = getNextWeekRange();
      const calendarResponse = await getContentCalendar(start, end);
      if (calendarResponse.success) {
        setCalendar(calendarResponse.calendar);
      }

      // Load optimal posting times
      const timesResponse = await getOptimalPostingTimes();
      if (timesResponse.success) {
        setOptimalTimes(timesResponse.optimal_times);
      }

    } catch (error) {
      console.error('Dashboard data loading failed:', error);
      toast({
        title: "Loading Failed",
        description: "Failed to load dashboard data. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const getEngagementColor = (rate: number) => {
    if (rate >= 5) return "text-green-600 dark:text-green-400";
    if (rate >= 3) return "text-blue-600 dark:text-blue-400";
    if (rate >= 1) return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const getGrowthColor = (growth: number) => {
    if (growth > 0) return "text-green-600 dark:text-green-400";
    if (growth < 0) return "text-red-600 dark:text-red-400";
    return "text-gray-600 dark:text-gray-400";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center h-64">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            >
              <Brain className="h-8 w-8 text-blue-600" />
            </motion.div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <Seo 
        title="Dashboard - InfluenceOS" 
        description="Comprehensive analytics and insights for your LinkedIn content performance"
      />
      
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <div className="relative">
                    <BarChart3 className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                    <motion.div
                      className="absolute inset-0 bg-blue-400 rounded-full blur-lg opacity-30"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                  </div>
                  <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                    Dashboard
                  </h1>
                </div>
                <p className="text-lg text-muted-foreground">
                  Comprehensive analytics and insights for your LinkedIn content
                </p>
              </div>
              
              <div className="flex items-center gap-2">
                <Button
                  variant={timePeriod === '7d' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setTimePeriod('7d')}
                >
                  7 Days
                </Button>
                <Button
                  variant={timePeriod === '30d' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setTimePeriod('30d')}
                >
                  30 Days
                </Button>
                <Button
                  variant={timePeriod === '90d' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setTimePeriod('90d')}
                >
                  90 Days
                </Button>
              </div>
            </div>
          </motion.div>

          {/* Key Metrics Cards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          >
            {/* Engagement Rate */}
            <Card className="relative overflow-hidden border-2 border-blue-200 dark:border-blue-800">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/50 dark:to-indigo-950/50" />
              <CardHeader className="relative pb-2">
                <CardTitle className="flex items-center gap-2 text-sm font-medium">
                  <Heart className="h-4 w-4 text-red-500" />
                  Engagement Rate
                </CardTitle>
              </CardHeader>
              <CardContent className="relative">
                <div className={`text-3xl font-bold ${getEngagementColor(analytics?.engagement_rate || 0)}`}>
                  {analytics?.engagement_rate?.toFixed(1) || '0.0'}%
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  {analytics?.engagement_rate >= 3 ? 'Excellent performance!' : 'Room for improvement'}
                </p>
              </CardContent>
            </Card>

            {/* Total Posts */}
            <Card className="relative overflow-hidden">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-sm font-medium">
                  <Activity className="h-4 w-4 text-green-500" />
                  Total Posts
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                  {analytics?.total_posts || 0}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Last {timePeriod === '7d' ? '7 days' : timePeriod === '30d' ? '30 days' : '90 days'}
                </p>
              </CardContent>
            </Card>

            {/* Total Reach */}
            <Card className="relative overflow-hidden">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-sm font-medium">
                  <Eye className="h-4 w-4 text-purple-500" />
                  Total Reach
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                  {analytics?.total_metrics?.reach?.toLocaleString() || '0'}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  People reached
                </p>
              </CardContent>
            </Card>

            {/* Growth Trend */}
            <Card className="relative overflow-hidden">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-sm font-medium">
                  <TrendingUp className="h-4 w-4 text-orange-500" />
                  Growth Trend
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className={`text-3xl font-bold ${getGrowthColor(analytics?.growth_trends?.engagement_growth || 0)}`}>
                  {analytics?.growth_trends?.engagement_growth > 0 ? '+' : ''}
                  {analytics?.growth_trends?.engagement_growth?.toFixed(1) || '0.0'}%
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Engagement growth
                </p>
              </CardContent>
            </Card>
          </motion.div>

          {/* Main Content Tabs */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Tabs defaultValue="analytics" className="space-y-6">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="analytics" className="flex items-center gap-2">
                  <BarChart3 className="h-4 w-4" />
                  Analytics
                </TabsTrigger>
                <TabsTrigger value="calendar" className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Calendar
                </TabsTrigger>
                <TabsTrigger value="insights" className="flex items-center gap-2">
                  <Brain className="h-4 w-4" />
                  Insights
                </TabsTrigger>
                <TabsTrigger value="optimization" className="flex items-center gap-2">
                  <Rocket className="h-4 w-4" />
                  Optimization
                </TabsTrigger>
              </TabsList>

              {/* Analytics Tab */}
              <TabsContent value="analytics" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Engagement Breakdown */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Heart className="h-5 w-5 text-red-500" />
                        Engagement Breakdown
                      </CardTitle>
                      <CardDescription>
                        How your audience interacts with your content
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <Heart className="h-4 w-4 text-red-500" />
                            <span className="text-sm">Likes</span>
                          </div>
                          <span className="font-medium">{analytics?.total_metrics?.likes?.toLocaleString() || 0}</span>
                        </div>
                        <Progress value={analytics?.total_metrics?.likes ? (analytics.total_metrics.likes / (analytics.total_metrics.likes + analytics.total_metrics.comments + analytics.total_metrics.shares)) * 100 : 0} className="h-2" />
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <MessageCircle className="h-4 w-4 text-blue-500" />
                            <span className="text-sm">Comments</span>
                          </div>
                          <span className="font-medium">{analytics?.total_metrics?.comments?.toLocaleString() || 0}</span>
                        </div>
                        <Progress value={analytics?.total_metrics?.comments ? (analytics.total_metrics.comments / (analytics.total_metrics.likes + analytics.total_metrics.comments + analytics.total_metrics.shares)) * 100 : 0} className="h-2" />
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <Share2 className="h-4 w-4 text-green-500" />
                            <span className="text-sm">Shares</span>
                          </div>
                          <span className="font-medium">{analytics?.total_metrics?.shares?.toLocaleString() || 0}</span>
                        </div>
                        <Progress value={analytics?.total_metrics?.shares ? (analytics.total_metrics.shares / (analytics.total_metrics.likes + analytics.total_metrics.comments + analytics.total_metrics.shares)) * 100 : 0} className="h-2" />
                      </div>
                    </CardContent>
                  </Card>

                  {/* Performance Metrics */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Target className="h-5 w-5 text-blue-500" />
                        Performance Metrics
                      </CardTitle>
                      <CardDescription>
                        Average performance per post
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center p-4 bg-blue-50 dark:bg-blue-950/50 rounded-lg">
                          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                            {analytics?.average_metrics?.likes?.toFixed(1) || '0.0'}
                          </div>
                          <div className="text-sm text-muted-foreground">Avg Likes</div>
                        </div>
                        <div className="text-center p-4 bg-green-50 dark:bg-green-950/50 rounded-lg">
                          <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                            {analytics?.average_metrics?.comments?.toFixed(1) || '0.0'}
                          </div>
                          <div className="text-sm text-muted-foreground">Avg Comments</div>
                        </div>
                        <div className="text-center p-4 bg-purple-50 dark:bg-purple-950/50 rounded-lg">
                          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                            {analytics?.average_metrics?.views?.toFixed(0) || '0'}
                          </div>
                          <div className="text-sm text-muted-foreground">Avg Views</div>
                        </div>
                        <div className="text-center p-4 bg-orange-50 dark:bg-orange-950/50 rounded-lg">
                          <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                            {analytics?.average_metrics?.reach?.toFixed(0) || '0'}
                          </div>
                          <div className="text-sm text-muted-foreground">Avg Reach</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              {/* Calendar Tab */}
              <TabsContent value="calendar" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Calendar className="h-5 w-5 text-green-500" />
                      Content Calendar
                    </CardTitle>
                    <CardDescription>
                      Upcoming scheduled posts and optimal posting times
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Scheduled Posts */}
                      <div className="space-y-4">
                        <h3 className="font-semibold">Scheduled Posts</h3>
                        {calendar?.scheduled_posts?.length > 0 ? (
                          calendar.scheduled_posts.map((post: any, index: number) => (
                            <div key={index} className="p-4 border rounded-lg">
                              <div className="flex items-center justify-between mb-2">
                                <Badge variant="outline">{post.post_type}</Badge>
                                <span className="text-sm text-muted-foreground">
                                  {new Date(post.scheduled_time).toLocaleDateString()}
                                </span>
                              </div>
                              <p className="text-sm">{post.content?.text?.substring(0, 100)}...</p>
                            </div>
                          ))
                        ) : (
                          <p className="text-muted-foreground">No scheduled posts</p>
                        )}
                      </div>

                      {/* Optimal Times */}
                      <div className="space-y-4">
                        <h3 className="font-semibold">Optimal Posting Times</h3>
                        {optimalTimes.map((time, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-950/50 rounded-lg">
                            <div className="flex items-center gap-2">
                              <Clock className="h-4 w-4 text-blue-500" />
                              <span className="font-medium">{time.day}</span>
                            </div>
                            <div className="text-right">
                              <div className="font-medium">{time.time}</div>
                              <div className="text-sm text-muted-foreground">
                                {time.engagement_score}% engagement
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Insights Tab */}
              <TabsContent value="insights" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Brain className="h-5 w-5 text-purple-500" />
                      AI-Powered Insights
                    </CardTitle>
                    <CardDescription>
                      Actionable recommendations to improve your content performance
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {analytics?.insights?.map((insight, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="flex items-start gap-3 p-4 bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-950/50 dark:to-blue-950/50 rounded-lg"
                        >
                          <Sparkles className="h-5 w-5 text-purple-500 mt-0.5 flex-shrink-0" />
                          <p className="text-sm">{insight}</p>
                        </motion.div>
                      )) || (
                        <p className="text-muted-foreground">No insights available yet. Create more content to get personalized recommendations!</p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Optimization Tab */}
              <TabsContent value="optimization" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Rocket className="h-5 w-5 text-orange-500" />
                      Content Optimization
                    </CardTitle>
                    <CardDescription>
                      Tools and recommendations to boost your content performance
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-4">
                        <h3 className="font-semibold">Quick Actions</h3>
                        <div className="space-y-2">
                          <Button className="w-full justify-start" variant="outline">
                            <Zap className="h-4 w-4 mr-2" />
                            Generate Content Ideas
                          </Button>
                          <Button className="w-full justify-start" variant="outline">
                            <Target className="h-4 w-4 mr-2" />
                            Analyze Competitors
                          </Button>
                          <Button className="w-full justify-start" variant="outline">
                            <Star className="h-4 w-4 mr-2" />
                            A/B Test Content
                          </Button>
                        </div>
                      </div>
                      
                      <div className="space-y-4">
                        <h3 className="font-semibold">Performance Tips</h3>
                        <div className="space-y-3">
                          <div className="flex items-start gap-2">
                            <Award className="h-4 w-4 text-yellow-500 mt-0.5" />
                            <div className="text-sm">
                              <div className="font-medium">Post consistently</div>
                              <div className="text-muted-foreground">Aim for 3-5 posts per week</div>
                            </div>
                          </div>
                          <div className="flex items-start gap-2">
                            <Award className="h-4 w-4 text-yellow-500 mt-0.5" />
                            <div className="text-sm">
                              <div className="font-medium">Use visual content</div>
                              <div className="text-muted-foreground">Images and carousels get 40% more engagement</div>
                            </div>
                          </div>
                          <div className="flex items-start gap-2">
                            <Award className="h-4 w-4 text-yellow-500 mt-0.5" />
                            <div className="text-sm">
                              <div className="font-medium">Ask questions</div>
                              <div className="text-muted-foreground">Questions generate 3x more comments</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </motion.div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
