import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { motion, AnimatePresence } from "framer-motion";

interface ContentPreviewProps {
  text?: string;
  imageUrl?: string;
  hashtags?: string[];
}

export const ContentPreview = ({ text, imageUrl, hashtags }: ContentPreviewProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card className="overflow-hidden">
        <CardHeader>
          <CardTitle>Generated Post Preview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <AnimatePresence>
            {text && (
              <motion.div
                key="text"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                <p className="text-sm leading-6 text-foreground/90 whitespace-pre-wrap">
                  {text}
                </p>
              </motion.div>
            )}
            {imageUrl && (
              <motion.div
                key="image"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
              >
                <img
                  src={imageUrl}
                  alt="AI generated social post visual"
                  loading="lazy"
                  className="h-56 w-full rounded-md object-cover"
                />
              </motion.div>
            )}
            {hashtags && hashtags.length > 0 && (
              <motion.div
                key="hashtags"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3, delay: 0.1 }}
                className="flex flex-wrap gap-2"
              >
                {hashtags.map((t, idx) => (
                  <motion.span 
                    key={t} 
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: idx * 0.05 }}
                    className="text-xs text-muted-foreground bg-muted/50 px-2 py-1 rounded-full"
                  >
                    {t}
                  </motion.span>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>
    </motion.div>
  );
};
