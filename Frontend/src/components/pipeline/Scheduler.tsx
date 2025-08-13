import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { Calendar, Clock } from "lucide-react";
import { motion } from "framer-motion";
import { schedulePost } from "@/lib/api";

interface SchedulerProps {
  text?: string;
  imageUrl?: string;
  hashtags?: string[];
  onSchedule?: (isoDate: string) => Promise<void> | void;
}

export const Scheduler = ({ text, imageUrl, hashtags, onSchedule }: SchedulerProps) => {
  const [dt, setDt] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handle = async () => {
    if (!dt) {
      toast({ title: "Select date & time", description: "Please choose when to publish." });
      return;
    }

    if (!text && !imageUrl) {
      toast({
        title: "No content to schedule",
        description: "Please generate content first before scheduling.",
        variant: "destructive"
      });
      return;
    }

    try {
      setLoading(true);

      if (onSchedule) {
        await onSchedule(dt);
      } else {
        // Use the API to schedule the post
        await schedulePost({
          text: text || "",
          imageUrl,
          hashtags: hashtags || [],
          scheduledTime: dt,
        });
      }

      toast({
        title: "Post scheduled successfully",
        description: `Your post will be published on ${new Date(dt).toLocaleString()}`
      });

      setDt(""); // Reset the form
    } catch (error) {
      console.error("Schedule error:", error);
      toast({
        title: "Failed to schedule post",
        description: "Please try again later.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
    >
      <Card className="card-glow">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="w-5 h-5" />
            Schedule
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-end gap-3">
          <label className="flex flex-col text-sm flex-1">
            <span className="mb-2 text-muted-foreground flex items-center gap-1">
              <Clock className="w-3 h-3" />
              Publish at
            </span>
            <motion.input
              type="datetime-local"
              value={dt}
              onChange={(e) => setDt(e.target.value)}
              className="h-10 rounded-md border border-input bg-background px-3 text-sm transition-all duration-300 focus:border-primary focus:ring-2 focus:ring-primary/20 hover:border-primary/50"
              whileFocus={{ scale: 1.02 }}
            />
          </label>
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button
              onClick={handle}
              variant="glow-accent"
              className="relative overflow-hidden"
              disabled={loading}
            >
              {loading ? "Scheduling..." : "Schedule"}
            </Button>
          </motion.div>
        </CardContent>
      </Card>
    </motion.div>
  );
};
