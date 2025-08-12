import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

interface SchedulerProps {
  onSchedule?: (isoDate: string) => Promise<void> | void;
}

export const Scheduler = ({ onSchedule }: SchedulerProps) => {
  const [dt, setDt] = useState("");
  const { toast } = useToast();

  const handle = async () => {
    if (!dt) {
      toast({ title: "Select date & time", description: "Please choose when to publish." });
      return;
    }
    await onSchedule?.(dt);
    toast({ title: "Post scheduled", description: new Date(dt).toLocaleString() });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Schedule</CardTitle>
      </CardHeader>
      <CardContent className="flex items-end gap-3">
        <label className="flex flex-col text-sm">
          <span className="mb-1 text-muted-foreground">Publish at</span>
          <input
            type="datetime-local"
            value={dt}
            onChange={(e) => setDt(e.target.value)}
            className="h-10 rounded-md border bg-background px-3 text-sm"
          />
        </label>
        <Button onClick={handle}>Schedule</Button>
      </CardContent>
    </Card>
  );
};
