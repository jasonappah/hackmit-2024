import { defineSchema, defineTable } from "convex/server";
import { Infer, v } from "convex/values";
import { SUNO_MODEL } from "../frontend/app/lib/constants";

export const sunoGenerateAudioPayload = v.object({
  gpt_description_prompt: v.optional(v.string()),
  tags: v.optional(v.array(v.string())),
  prompt: v.string(),
  mv: v.literal(SUNO_MODEL)
})

export type SunoGenerateAudioPayload = Infer<typeof sunoGenerateAudioPayload>

export const sunoStatus = v.union(
  v.literal("submitted"),
  v.literal("queued"),
  v.literal("streaming"),
  v.literal("complete"),
  v.literal("error")
)

export const sunoGeneratedClip = v.object({
  id: v.string(),
  video_url: v.optional(v.string()),
  audio_url: v.optional(v.string()),
  image_large_url: v.optional(v.string()),
  image_url: v.optional(v.string()),
  is_video_pending: v.boolean(),
  major_model_version: v.string(),
  model_name: v.string(),
  metadata: v.any(), // TODO
  status: sunoStatus,
  title: v.string(),
  play_count: v.number(),
  upvote_count: v.number(),
  is_public: v.boolean(),
  is_liked: v.boolean(),
  is_trashed: v.boolean(),
  created_at: v.string(),
  user_id: v.string(),
  display_name: v.string(),
  handle: v.string(),
  is_handle_updated: v.boolean(),
  avatar_image_url: v.string()
})




export type SunoGeneratedClip = Infer<typeof sunoGeneratedClip>

export default defineSchema({
  suno_prompts: defineTable({
    suno_prompt_id: v.string(),
    suno_request_payload: sunoGenerateAudioPayload
  }),
  suno_clips: defineTable({
    suno_prompt: v.id("suno_prompts"),
    suno_clip_id: v.string(),
    status: sunoStatus,
    result: v.optional(sunoGeneratedClip)
  })
});