import { SunoGeneratedClip } from "../../../convex/schema";

export type SunoGenerateAudioResponse = {
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
};

export interface SunoFeedResponse {
  clips: SunoGeneratedClip[];
  num_total_results: number;
  current_page: number;
}

