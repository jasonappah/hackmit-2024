import { useMutation, useQuery } from 'react-query';
const SUNO_MODEL = "chirp-v3-5" as const;

type SunoGenerateAudioPayload = {
  gpt_description_prompt?: string;
  tags?: string[];
  prompt: string;
  mv: typeof SUNO_MODEL;
}

type SunoGenerateAudioResponse = {
    id: string;
    clips: {
        id: string;
        video_url: string;
        audio_url: string;
        is_video_pending: boolean;
        major_model_version: string;
        model_name: string;
        metadata: Metadata;
        is_liked: boolean;
        user_id: string;
        display_name: string;
        handle: string;
        is_handle_updated: boolean;
        avatar_image_url: string;
        is_trashed: boolean;
        created_at: string;
        status: string;
        title: string;
        play_count: number;
        upvote_count: number;
        is_public: boolean;
    }[];
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

const BASE_URL = "https://studio-api.suno.ai" as const;

export const useGenerateAudioByPrompt = () => {
  return useMutation<SunoGenerateAudioResponse, Error, SunoGenerateAudioPayload>(
    async (payload) => {
      const url = BASE_URL + '/api/generate/v2/';
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${process.env.SUNO_API_KEY}`,
        },
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
    clips: {
        id: string;
        video_url: string;
        audio_url: string;
        image_url: string;
        image_large_url: string;
        is_video_pending: boolean;
        major_model_version: string;
        model_name: string;
        metadata: {
            tags: string;
            prompt: string;
            gpt_description_prompt: string;
            type: string;
            duration?: number;
            refund_credits?: boolean;
            stream: boolean;
        };
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
    }[];
    num_total_results: number;
    current_page: number;
}


export const useGetFeed = (ids: string[]) => {
  return useQuery<SunoFeedResponse, Error>(
    ['feed', ids],
    async () => {
      const url = `${BASE_URL}/api/feed/v2/?ids=${ids.join(',')}`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${process.env.SUNO_API_KEY}`,
        },
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    }
  );
};

