import { APP_NAME,SUNO_MODEL } from "~/lib/constants";

import { Button } from "~/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import { useGenerateAudioByPrompt, useGetFeed } from "~/lib/suno";
import { useState } from "react";

export default function Card2() {
  const feedQuery = useGetFeed(['e114e151-8243-4e16-b756-eb47874e85d1','33b00567-6772-43b2-b97c-4dc8b2f77dc6']);
  const generate = useGenerateAudioByPrompt();
  const [input, setInput] = useState<string>('')
  return (
      <div className="flex flex-col items-center justify-center w-full min-h-screen gap-4 py-12">
        <Card className="w-[350px]">
          <CardHeader>
            <CardTitle>{APP_NAME}</CardTitle>
            <CardDescription>Generate a song in one click.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="prompt">Prompt</Label>
                <Input id="prompt" placeholder="Name of your project" value={input} onChange={(e)=>setInput(e.target.value)} />
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button type="button" onClick={(e) => {
              e.preventDefault();
              generate.mutate({
                mv: SUNO_MODEL,
                prompt: input
              })
            }}>Generate</Button>
          </CardFooter>
        </Card>
          {feedQuery.isLoading && <p>Loading...</p>}
          {feedQuery.error && <p>Error: {feedQuery.error.message}</p>}
          {feedQuery.data && 
            feedQuery.data.clips.map((clip) => (
              <ClipCard key={clip.id} clip={clip} />
            ))
          }
      </div>
  );
}

interface ClipCardProps {
  clip: SunoFeedResponse['clips'][0];
}

import { SunoFeedResponse } from '~/lib/suno';
import { Play, Pause, ThumbsUp } from "lucide-react";
import { Badge } from "~/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "~/components/ui/avatar";

const ClipCard: React.FC<ClipCardProps> = ({ clip }) => {

  const renderStatus = () => {
    switch (clip.status) {
      case 'submitted':
      case 'queued':
        return <Badge variant="secondary">In Queue</Badge>;
      case 'streaming':
        return <Badge variant="secondary">Generating</Badge>;
      case 'complete':
        return <Badge variant="default">Ready</Badge>;
      case 'error':
        return <Badge variant="destructive">Error</Badge>;
      default:
        return null;
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="truncate">{clip.title}</span>
          {renderStatus()}
        </CardTitle>
        <div className="flex items-center space-x-2">
          <Avatar>
            <AvatarImage src={clip.avatar_image_url} />
            <AvatarFallback>{clip.display_name.charAt(0)}</AvatarFallback>
          </Avatar>
          <span className="text-sm text-muted-foreground">{clip.display_name}</span>
        </div>
      </CardHeader>
      <CardContent>
        {clip.status === 'complete' && (
          <div className="aspect-video bg-secondary flex items-center justify-center">
            {clip.video_url ? (
              <video controls width="100%" height="100%">
                <source src={clip.video_url} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            ) : clip.audio_url ? (
              <audio controls className="w-full">
                <source src={clip.audio_url} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
            ) : (
              <p>No media available</p>
            )}
          </div>
        )}
        <p className="mt-2 text-sm text-muted-foreground">Prompt: {clip.metadata.prompt}</p>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline" size="icon" disabled={clip.status !== 'complete'}>
          
          hi
        </Button>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm">
            <ThumbsUp className="h-4 w-4 mr-2" />
            {clip.upvote_count}
          </Button>
          <span className="text-sm text-muted-foreground">{clip.play_count} plays</span>
        </div>
      </CardFooter>
    </Card>
  );
};

// {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}