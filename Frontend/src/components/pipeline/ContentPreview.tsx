import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Image, Hash } from "lucide-react";

interface ContentPreviewProps {
  text?: string;
  imageUrl?: string;
  hashtags?: string[];
  isGenerating?: boolean;
}

export const ContentPreview = ({ text, imageUrl, hashtags, isGenerating }: ContentPreviewProps) => {
  const hasContent = text || imageUrl || (hashtags && hashtags.length > 0);
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card className={`overflow-hidden transition-all duration-500 ${hasContent ? 'card-glow glow-accent' : ''} ${isGenerating ? 'ai-processing' : ''}`}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            Generated Post Preview
            {isGenerating && (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full"
              />
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 relative">
          {/* Shimmer effect when generating */}
          {isGenerating && !hasContent && (
            <div className="space-y-4">
              <div className="shimmer h-20 bg-muted/30 rounded-md" />
              <div className="shimmer h-32 bg-muted/30 rounded-md" />
              <div className="flex gap-2">
                <div className="shimmer h-6 w-16 bg-muted/30 rounded-full" />
                <div className="shimmer h-6 w-20 bg-muted/30 rounded-full" />
                <div className="shimmer h-6 w-14 bg-muted/30 rounded-full" />
              </div>
            </div>
          )}

          <AnimatePresence>
            {text && (
              <motion.div
                key="text"
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{
                  opacity: 1,
                  y: 0,
                  scale: 1,
                }}
                exit={{ opacity: 0, y: -10 }}
                transition={{
                  duration: 0.6,
                  type: "spring",
                  stiffness: 100
                }}
                className="relative"
              >
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="absolute -inset-2 bg-gradient-to-r from-primary/10 to-transparent rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
                />
                <div className="flex items-start gap-2 mb-2">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.3, type: "spring" }}
                  >
                    <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center">
                      <span className="text-xs">📝</span>
                    </div>
                  </motion.div>
                  <span className="text-xs text-muted-foreground font-medium">Generated Text</span>
                </div>
                <motion.p
                  className="text-sm leading-6 text-foreground/90 whitespace-pre-wrap relative z-10 p-3 rounded-lg bg-background/50 border border-primary/20"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  {text}
                </motion.p>
                <motion.div
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: [0, 1.2, 1], opacity: [0, 0.8, 0] }}
                  transition={{ duration: 1, delay: 0.1 }}
                  className="absolute -inset-1 bg-primary/20 rounded-lg"
                />
              </motion.div>
            )}
            {imageUrl && (
              <motion.div
                key="image"
                initial={{ opacity: 0, scale: 0.8, rotateY: 90 }}
                animate={{
                  opacity: 1,
                  scale: 1,
                  rotateY: 0,
                }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{
                  duration: 0.8,
                  type: "spring",
                  stiffness: 100
                }}
                className="relative group"
              >
                <div className="flex items-start gap-2 mb-2">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.3, type: "spring" }}
                  >
                    <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center">
                      <Image className="w-3 h-3" />
                    </div>
                  </motion.div>
                  <span className="text-xs text-muted-foreground font-medium">Generated Image</span>
                </div>
                <motion.div
                  className="relative overflow-hidden rounded-lg"
                  whileHover={{ scale: 1.02 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <img
                    src={imageUrl}
                    alt="AI generated social post visual"
                    loading="lazy"
                    className="h-56 w-full rounded-lg object-cover border border-primary/20"
                    onError={(e) => {
                      console.warn('Image failed to load:', imageUrl);
                      // Fallback to a professional placeholder
                      (e.target as HTMLImageElement).src = "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop";
                    }}
                    onLoad={() => {
                      console.log('Image loaded successfully:', imageUrl);
                    }}
                  />
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="absolute inset-0 bg-gradient-to-t from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                  />
                </motion.div>
                <motion.div
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: [0, 1.1, 1], opacity: [0, 0.6, 0] }}
                  transition={{ duration: 1.2, delay: 0.2 }}
                  className="absolute -inset-2 bg-primary/15 rounded-lg"
                />
              </motion.div>
            )}
            {hashtags && hashtags.length > 0 && (
              <motion.div
                key="hashtags"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="relative"
              >
                <div className="flex items-start gap-2 mb-3">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.4, type: "spring" }}
                  >
                    <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center">
                      <Hash className="w-3 h-3" />
                    </div>
                  </motion.div>
                  <span className="text-xs text-muted-foreground font-medium">Optimized Hashtags</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {hashtags.map((t, idx) => (
                    <motion.span
                      key={t}
                      initial={{ opacity: 0, scale: 0.5, y: 20 }}
                      animate={{
                        opacity: 1,
                        scale: 1,
                        y: 0,
                      }}
                      transition={{
                        delay: 0.5 + idx * 0.1,
                        type: "spring",
                        stiffness: 200
                      }}
                      whileHover={{
                        scale: 1.1,
                        backgroundColor: "hsla(var(--primary), 0.2)"
                      }}
                      className="text-xs text-primary bg-primary/10 border border-primary/20 px-3 py-1.5 rounded-full cursor-pointer transition-all duration-200 hover:shadow-md hover:shadow-primary/20"
                    >
                      {t}
                    </motion.span>
                  ))}
                </div>
                <motion.div
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: [0, 1.3, 1], opacity: [0, 0.4, 0] }}
                  transition={{ duration: 1.5, delay: 0.3 }}
                  className="absolute -inset-2 bg-primary/10 rounded-lg"
                />
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>
    </motion.div>
  );
};
