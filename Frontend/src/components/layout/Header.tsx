import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "@/components/ui/theme-toggle";

const nav = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/pipeline", label: "Pipeline" },
  { to: "/analytics", label: "Analytics" },
  { to: "/profile", label: "Profile" },
  { to: "/outreach", label: "Outreach" },
];

export const Header = () => {
  const { pathname } = useLocation();

  return (
    <motion.header 
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60"
    >
      <nav className="container flex h-14 items-center justify-between">
        <Link to="/" className="story-link text-sm font-semibold">
          <motion.span
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            InfluenceOS
          </motion.span>
        </Link>
        <div className="flex items-center gap-1">
          {nav.map((n, idx) => (
            <motion.div
              key={n.to}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <Link to={n.to} className="contents">
                <Button
                  variant={pathname === n.to ? "secondary" : "ghost"}
                  size="sm"
                  className={cn("hover-scale", pathname === n.to && "pointer-events-none")}
                  aria-current={pathname === n.to ? "page" : undefined}
                >
                  {n.label}
                </Button>
              </Link>
            </motion.div>
          ))}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: nav.length * 0.1 }}
            className="ml-2"
          >
            <ThemeToggle />
          </motion.div>
        </div>
      </nav>
    </motion.header>
  );
};
