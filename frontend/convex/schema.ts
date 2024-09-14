import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  prompts: defineTable({
    suno_prompt_id: v.string(),
    suno_request_payload: v.any() // Same as SunoGenerateAudioPayload in suno.ts
  }),
  suno_clips: defineTable({
    suno_prompt: v.id("prompts"),
    suno_clip_id: v.string(),
    status: v.string(), // TODO: enum, see frontend/app/lib/suno.ts for reference
    result: v.any()
  })
});