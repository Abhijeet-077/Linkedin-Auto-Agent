import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

export type Step = {
  key: string;
  label: string;
  status: "pending" | "running" | "done" | "error";
};

interface AgentTimelineProps {
  steps: Step[];
}

export const AgentTimeline = ({ steps }: AgentTimelineProps) => {
  return (
    <ol className="relative ml-2 border-l pl-6">
      <AnimatePresence>
        {steps.map((s, idx) => (
          <motion.li 
            key={s.key} 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="mb-6"
          >
            <motion.div 
              className="absolute -left-3 mt-1 rounded-full bg-background"
              whileHover={{ scale: 1.1 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <AnimatePresence mode="wait">
                {s.status === "running" && (
                  <motion.div
                    key="running"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1, rotate: 360 }}
                    exit={{ scale: 0 }}
                    transition={{ repeat: Infinity, duration: 1 }}
                  >
                    <Loader2 className="animate-spin" />
                  </motion.div>
                )}
                {s.status === "pending" && (
                  <motion.div
                    key="pending"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                  >
                    <Circle />
                  </motion.div>
                )}
                {s.status === "done" && (
                  <motion.div
                    key="done"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <CheckCircle2 className="text-primary" />
                  </motion.div>
                )}
                {s.status === "error" && (
                  <motion.div
                    key="error"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                  >
                    <XCircle className="text-destructive" />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
            <motion.div 
              className={cn("text-sm", s.status === "running" && "font-medium")}
              animate={{ 
                opacity: s.status === "running" ? [1, 0.7, 1] : 1 
              }}
              transition={{ 
                repeat: s.status === "running" ? Infinity : 0, 
                duration: 1.5 
              }}
            >
              {s.label}
            </motion.div>
            <div className="text-xs text-muted-foreground">
              {s.status === "pending" && "Waiting"}
              {s.status === "running" && "In progress"}
              {s.status === "done" && "Completed"}
              {s.status === "error" && "Error"}
            </div>
          </motion.li>
        ))}
      </AnimatePresence>
    </ol>
  );
};
