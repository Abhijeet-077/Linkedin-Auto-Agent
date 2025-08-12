import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface ContentPreviewProps {
  text?: string;
  imageUrl?: string;
  hashtags?: string[];
}

export const ContentPreview = ({ text, imageUrl, hashtags }: ContentPreviewProps) => {
  return (
    <Card className="animate-[fade-in_0.3s_ease-out]">
      <CardHeader>
        <CardTitle>Generated Post Preview</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {text && (
          <p className="text-sm leading-6 text-foreground/90 whitespace-pre-wrap">
            {text}
          </p>
        )}
        {imageUrl && (
          <img
            src={imageUrl}
            alt="AI generated social post visual"
            loading="lazy"
            className="h-56 w-full rounded-md object-cover"
          />
        )}
        {hashtags && hashtags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {hashtags.map((t) => (
              <span key={t} className="text-xs text-muted-foreground">{t}</span>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
