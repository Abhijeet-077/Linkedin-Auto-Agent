import { Seo } from "@/components/Seo";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

const Index = () => {
  return (
    <motion.main 
      className="container py-16 text-center"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Seo title="InfluenceOS – Emergent-style Content Builder" description="Create, visualize, and schedule AI-powered posts with a fluid, modern UI." canonicalPath="/" />
      <motion.h1 
        className="mb-4 text-4xl font-bold"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        Welcome to InfluenceOS
      </motion.h1>
      <motion.p 
        className="mx-auto mb-8 max-w-2xl text-muted-foreground"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        Start with the One-Click Content Pipeline to generate text, image, and hashtags in real-time.
      </motion.p>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Link to="/pipeline" className="contents">
          <Button size="lg" variant="glow" className="relative overflow-hidden">
            Launch Pipeline
          </Button>
        </Link>
      </motion.div>
    </motion.main>
  );
};

export default Index;
