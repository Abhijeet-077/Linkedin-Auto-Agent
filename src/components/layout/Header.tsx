import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const nav = [
  { to: "/pipeline", label: "Pipeline" },
  { to: "/analytics", label: "Analytics" },
  { to: "/profile", label: "Profile" },
  { to: "/outreach", label: "Outreach" },
];

export const Header = () => {
  const { pathname } = useLocation();

  return (
    <header className="border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <nav className="container flex h-14 items-center justify-between">
        <Link to="/" className="story-link text-sm font-semibold">
          InfluenceOS
        </Link>
        <div className="flex items-center gap-1">
          {nav.map((n) => (
            <Link key={n.to} to={n.to} className="contents">
              <Button
                variant={pathname === n.to ? "secondary" : "ghost"}
                size="sm"
                className={cn("hover-scale", pathname === n.to && "pointer-events-none")}
                aria-current={pathname === n.to ? "page" : undefined}
              >
                {n.label}
              </Button>
            </Link>
          ))}
        </div>
      </nav>
    </header>
  );
};
