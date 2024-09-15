import { SUNO_BASE_URL } from "../frontend/app/lib/constants";
import { action, mutation, query, internalMutation, internalQuery } from "./_generated/server";
import { SunoFeedResponse, sunoGenerateAudioPayload, SunoGenerateAudioResponse, sunoGeneratedClip } from "./schema";
import { v } from "convex/values";
import { api, internal } from "./_generated/api";
import { paginationOptsValidator } from "convex/server";

const headers = {
  "Content-Type": "application/json",
  Authorization: `Bearer ${process.env.SUNO_API_KEY}`,
};


export const generateSunoAudio = action({
  args: sunoGenerateAudioPayload,
  handler: async (ctx, args) => {
    const res = await fetch(SUNO_BASE_URL + "/api/generate/v2/", {
      headers,
      method: "POST",
      body: JSON.stringify(args),
    });
    const json = (await res.json()) as SunoGenerateAudioResponse;

    await ctx.runMutation(internal.functions.saveSunoClipsToDb, {
      args,
      promptId: json.id,
      clips: json.clips.map((clip) => clip.id),
    });
  },
});

export const saveSunoClipsToDb = internalMutation({
  args: {
    args: sunoGenerateAudioPayload,
    promptId: v.string(),
    clips: v.array(v.string()),
  },
  handler: async (ctx, { args, promptId, clips }) => {
    const promptDbId = await ctx.db.insert("suno_prompts", {
      suno_request_payload: args,
      suno_prompt_id: promptId,
    });
    for (const suno_clip_id of clips) {
      await ctx.db.insert("suno_clips", {
        suno_prompt: promptDbId,
        suno_clip_id,
        status: "submitted",
      });
    }
    await ctx.scheduler.runAfter(0, api.functions.schedulePollSunoClips, {});
  },
});

export const getSunoClipIdsToPoll = internalQuery({
  args: {},
  handler: async (ctx) => {
    const objs = await ctx.db
      .query("suno_clips")
      .filter((q) =>
        q.and(
          q.not(q.eq(q.field("status"), "complete")),
          q.not(q.eq(q.field("status"), "error")),
        ),
      )
      .take(10);

    return objs.map((obj) => obj.suno_clip_id);
  },
});

export const updateSunoClipStatus = internalMutation({
  args: {
    clipId: v.string(),
    body: sunoGeneratedClip,
  },
  handler: async (ctx, args) => {
    const clip = await ctx.db
      .query("suno_clips")
      .filter((q) => q.eq(q.field("suno_clip_id"), args.clipId))
      .first();
    if (!clip) {
      throw new Error("Clip not found");
    }
    const dbId = clip._id;
    await ctx.db.patch(dbId, {
      result: args.body,
      status: args.body.status,
    });
  },
});



export const getSunoClips = query({
  args: { paginationOpts: paginationOptsValidator },
  handler: async (ctx, args) => {
    // TODO: paginate maybe idk
    const objs = await ctx.db.query("suno_clips").order("desc").paginate(args.paginationOpts);
    return objs;
  },
});

export const schedulePollSunoClips = mutation({
  handler: async (ctx) => {
    const tasks = await ctx.db.system.query("_scheduled_functions").collect();
    const isPollScheduled = tasks.some(
      (task) =>
        task.name === "functions.js:pollSunoClips" && !task.completedTime,
    );

    console.log({ tasks, isPollScheduled });
    if (!isPollScheduled) {
      await ctx.scheduler.runAfter(0, api.functions.pollSunoClips, {});
    }
  },
});

export const pollSunoClips = action({
  handler: async (ctx) => {
    const clipsToUpdate = await ctx.runQuery(
      internal.functions.getSunoClipIdsToPoll,
      {},
    );

    if (clipsToUpdate.length === 0) {
      return;
    }

    const response = await fetch(
      SUNO_BASE_URL + `/api/feed/v2/?ids=${clipsToUpdate.join(",")}`,
      { headers },
    );
    const clipData = (await response.json()) as SunoFeedResponse;

    if (!clipData.clips) {
      console.log(clipData);
      throw new Error("Suno API error");
    }

    for (const clip of clipData.clips) {
      await ctx.runMutation(internal.functions.updateSunoClipStatus, {
        clipId: clip.id,
        body: clip,
      });
    }

    await ctx.scheduler.runAfter(10000, api.functions.pollSunoClips, {});
  },
});
