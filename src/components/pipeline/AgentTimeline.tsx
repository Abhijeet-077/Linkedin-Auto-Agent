import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";
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
      {steps.map((s, idx) => (
        <li key={s.key} className="mb-6">
          <div className="absolute -left-3 mt-1 rounded-full bg-background">
            {s.status === "running" && <Loader2 className="animate-spin" />}
            {s.status === "pending" && <Circle />}
            {s.status === "done" && <CheckCircle2 className="text-primary" />}
            {s.status === "error" && <XCircle className="text-destructive" />}
          </div>
          <div className={cn("text-sm", s.status === "running" && "font-medium")}>{s.label}</div>
          <div className="text-xs text-muted-foreground">
            {s.status === "pending" && "Waiting"}
            {s.status === "running" && "In progress"}
            {s.status === "done" && "Completed"}
            {s.status === "error" && "Error"}
          </div>
        </li>
      ))}
    </ol>
  );
};
