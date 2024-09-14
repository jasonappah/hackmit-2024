import { useMutation, useQuery } from 'react-query';
import { SUNO_MODEL } from './constants';


type SunoGenerateAudioPayload = {
  gpt_description_prompt?: string;
  tags?: string[];
  prompt: string;
  mv: typeof SUNO_MODEL;
}

type SunoGeneratedClip = {
    id: string;
    video_url: string;
    audio_url: string;
    is_video_pending: boolean;
    major_model_version: string;
    model_name: string;
    metadata: any; // dont care lol
    is_liked: boolean;
    user_id: string;
    display_name: string;
    handle: string;
    is_handle_updated: boolean;
    avatar_image_url: string;
    is_trashed: boolean;
    created_at: string;
    status: 'submitted' | 'queued' | 'streaming' | 'complete' | 'error';
    title: string;
    play_count: number;
    upvote_count: number;
    is_public: boolean;
}

type SunoGenerateAudioResponse = {
    id: string;
    clips: SunoGeneratedClip[];
    metadata: {
        prompt: string;
        gpt_description_prompt: string;
        type: string;
        stream: boolean;
    };
    major_model_version: string;
    status: string;
    created_at: string;
    batch_size: number;
}

export const useGenerateAudioByPrompt = () => {
  return useMutation<SunoGenerateAudioResponse, Error, SunoGenerateAudioPayload>(
    async (payload) => {
      const route = '/api/generate/v2/';
      const url = `/suno_proxy?endpoint=${encodeURIComponent(route)}`
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }
  );
};

export interface SunoFeedResponse {
    clips: SunoGeneratedClip[];
    num_total_results: number;
    current_page: number;
}


export const useGetFeed = (ids: string[]) => {
  return useQuery<SunoFeedResponse, Error>(
    ['feed', ids],
    async () => {
      const route = `/api/feed/v2/?ids=${(ids.join(','))}`;
      const url = `/suno_proxy?endpoint=${encodeURIComponent(route)}`
      const response = await fetch(url, {
        method: "GET",
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }, {
      refetchInterval: 1000 * 10, // 10 seconds
    }
  );
};

