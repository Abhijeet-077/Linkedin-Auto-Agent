import { useEffect } from "react";
import { useLocation } from "react-router-dom";

interface SeoProps {
  title: string;
  description?: string;
  canonicalPath?: string;
}

// Lightweight SEO helper without external deps
export const Seo = ({ title, description, canonicalPath }: SeoProps) => {
  const location = useLocation();

  useEffect(() => {
    // Title tag
    document.title = title;

    // Meta description
    let desc = document.querySelector('meta[name="description"]');
    if (!desc) {
      desc = document.createElement('meta');
      desc.setAttribute('name', 'description');
      document.head.appendChild(desc);
    }
    if (description) desc.setAttribute('content', description);

    // Canonical tag
    const href = `${window.location.origin}${canonicalPath ?? location.pathname}`;
    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      document.head.appendChild(canonical);
    }
    canonical.setAttribute('href', href);
  }, [title, description, canonicalPath, location.pathname]);

  return null;
};
