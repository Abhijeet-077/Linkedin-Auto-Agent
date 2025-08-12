import { Seo } from "@/components/Seo";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Index = () => {
  return (
    <main className="container py-16 text-center">
      <Seo title="InfluenceOS – Emergent-style Content Builder" description="Create, visualize, and schedule AI-powered posts with a fluid, modern UI." canonicalPath="/" />
      <h1 className="mb-4 text-4xl font-bold">Welcome to InfluenceOS</h1>
      <p className="mx-auto mb-8 max-w-2xl text-muted-foreground">
        Start with the One-Click Content Pipeline to generate text, image, and hashtags in real-time.
      </p>
      <Link to="/pipeline" className="contents">
        <Button size="lg" className="hover-scale">Launch Pipeline</Button>
      </Link>
    </main>
  );
};

export default Index;
