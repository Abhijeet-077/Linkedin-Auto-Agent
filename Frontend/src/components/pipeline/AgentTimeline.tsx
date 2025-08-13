import { CheckCircle2, Circle, Loader2, XCircle, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";

export type Step = {
  key: string;
  label: string;
  status: "pending" | "running" | "done" | "error";
};

interface AgentTimelineProps {
  steps: Step[];
}

// Particle component for visual effects
const Particle = ({ delay = 0 }: { delay?: number }) => {
  return (
    <motion.div
      className="absolute w-1 h-1 bg-primary/60 rounded-full"
      initial={{
        opacity: 0,
        scale: 0,
        x: Math.random() * 40 - 20,
        y: Math.random() * 40 - 20
      }}
      animate={{
        opacity: [0, 1, 0],
        scale: [0, 1, 0],
        x: Math.random() * 80 - 40,
        y: Math.random() * 80 - 40
      }}
      transition={{
        duration: 2,
        delay,
        repeat: Infinity,
        repeatDelay: Math.random() * 2
      }}
    />
  );
};

export const AgentTimeline = ({ steps }: AgentTimelineProps) => {
  const [particles, setParticles] = useState<number[]>([]);

  // Generate particles for running steps
  useEffect(() => {
    const runningSteps = steps.filter(s => s.status === "running");
    if (runningSteps.length > 0) {
      setParticles(Array.from({ length: 8 }, (_, i) => i));
    } else {
      setParticles([]);
    }
  }, [steps]);

  return (
    <div className="relative overflow-hidden">
      <ol className="relative ml-2 border-l border-border/50 pl-6 z-10">
        <AnimatePresence>
          {steps.map((s, idx) => (
            <motion.li
              key={s.key}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="mb-8 relative z-20 min-h-[60px]"
            >
            <motion.div
              className={cn(
                "absolute -left-3 mt-1 rounded-full bg-background p-1 border-2 transition-all duration-300 z-30",
                "w-6 h-6 flex items-center justify-center",
                s.status === "running" && "ai-processing glow-primary pulse-dot",
                s.status === "done" && "glow-accent border-primary/30",
                s.status === "pending" && "border-muted-foreground/30",
                s.status === "error" && "border-destructive/50"
              )}
              whileHover={{ scale: 1.1 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              {/* Particle effects for running state */}
              {s.status === "running" && (
                <div className="absolute inset-0 particle-container overflow-hidden rounded-full z-10">
                  {particles.map((_, i) => (
                    <Particle key={i} delay={i * 0.2} />
                  ))}
                </div>
              )}

              <AnimatePresence mode="wait">
                {s.status === "running" && (
                  <motion.div
                    key="running"
                    initial={{ scale: 0 }}
                    animate={{
                      scale: 1,
                      rotate: 360,
                    }}
                    exit={{ scale: 0 }}
                    transition={{
                      rotate: { repeat: Infinity, duration: 1, ease: "linear" },
                      scale: { type: "spring", stiffness: 300 }
                    }}
                    className="relative z-40"
                  >
                    <Loader2 className="w-4 h-4 text-primary" />
                  </motion.div>
                )}
                {s.status === "pending" && (
                  <motion.div
                    key="pending"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                    className="relative z-40"
                  >
                    <Circle className="w-4 h-4 text-muted-foreground" />
                  </motion.div>
                )}
                {s.status === "done" && (
                  <motion.div
                    key="done"
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{
                      scale: 1,
                      rotate: 0,
                    }}
                    exit={{ scale: 0 }}
                    transition={{
                      type: "spring",
                      stiffness: 300,
                      damping: 20
                    }}
                    className="relative z-40"
                  >
                    <CheckCircle2 className="w-4 h-4 text-primary" />
                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: [0, 1.5, 0], opacity: [0, 1, 0] }}
                      transition={{ duration: 0.6, delay: 0.2 }}
                      className="absolute inset-0 rounded-full bg-primary/20"
                    />
                  </motion.div>
                )}
                {s.status === "error" && (
                  <motion.div
                    key="error"
                    initial={{ scale: 0 }}
                    animate={{
                      scale: 1,
                      x: [0, -2, 2, -2, 2, 0]
                    }}
                    exit={{ scale: 0 }}
                    transition={{
                      scale: { type: "spring", stiffness: 300 },
                      x: { duration: 0.5, delay: 0.2 }
                    }}
                    className="relative z-40"
                  >
                    <XCircle className="w-4 h-4 text-destructive" />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
            <motion.div
              className={cn(
                "text-sm transition-all duration-300",
                s.status === "running" && "font-medium text-primary",
                s.status === "done" && "text-primary/80",
                s.status === "error" && "text-destructive"
              )}
              animate={{
                opacity: s.status === "running" ? [1, 0.7, 1] : 1,
                x: s.status === "running" ? [0, 2, 0] : 0
              }}
              transition={{
                repeat: s.status === "running" ? Infinity : 0,
                duration: 1.5
              }}
            >
              {s.label}
              {s.status === "running" && (
                <motion.span
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="ml-2 inline-block"
                >
                  <Sparkles className="w-3 h-3 text-primary animate-pulse" />
                </motion.span>
              )}
            </motion.div>
            <motion.div
              className={cn(
                "text-xs transition-colors duration-300",
                s.status === "running" && "text-primary/70",
                s.status === "done" && "text-primary/60",
                s.status === "error" && "text-destructive/70",
                s.status === "pending" && "text-muted-foreground"
              )}
              animate={{
                opacity: s.status === "running" ? [0.7, 1, 0.7] : 1
              }}
              transition={{
                repeat: s.status === "running" ? Infinity : 0,
                duration: 2
              }}
            >
              {s.status === "pending" && "Waiting"}
              {s.status === "running" && (
                <span className="flex items-center gap-1">
                  Processing
                  <motion.span
                    animate={{ opacity: [0, 1, 0] }}
                    transition={{ repeat: Infinity, duration: 1.5 }}
                  >
                    ...
                  </motion.span>
                </span>
              )}
              {s.status === "done" && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  ✨ Completed
                </motion.span>
              )}
              {s.status === "error" && "❌ Error occurred"}
            </motion.div>
          </motion.li>
        ))}
      </AnimatePresence>
    </ol>

    {/* Background particle effects for active processing */}
    {particles.length > 0 && (
      <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
        {Array.from({ length: 8 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-primary/15 rounded-full"
            initial={{
              opacity: 0,
              x: Math.random() * 200,
              y: Math.random() * 150
            }}
            animate={{
              opacity: [0, 0.4, 0],
              x: Math.random() * 200,
              y: Math.random() * 150,
              scale: [0, 1, 0]
            }}
            transition={{
              duration: 4,
              delay: i * 0.4,
              repeat: Infinity,
              repeatDelay: Math.random() * 3
            }}
          />
        ))}
      </div>
    )}
  </div>
  );
};
