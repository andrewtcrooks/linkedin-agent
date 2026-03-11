#!/usr/bin/env node
import { Memory } from "mem0ai/oss";
import * as path from "path";
import * as os from "os";

const MEM0_DIR = path.join(os.homedir(), ".mem0");
const HISTORY_DB = path.join(MEM0_DIR, "history.db");

const LLM_BASE_URL = process.env.MEM0_LLM_BASE_URL || "http://127.0.0.1:8011/v1";
const EMBED_BASE_URL = process.env.MEM0_EMBED_BASE_URL || "http://127.0.0.1:8012/v1";
const DUMMY_KEY = process.env.MEM0_API_KEY || "local";

export function getMem0Instance(options = {}) {
  const dims = Number(process.env.MEM0_EMBED_DIMS || 384);

  const config = {
    version: "v1.1",
    embedder: {
      provider: "openai",
      config: {
        apiKey: DUMMY_KEY,
        url: EMBED_BASE_URL,
        model: process.env.MEM0_EMBED_MODEL || "bge-small-en-v1.5",
        embeddingDims: dims,
      },
    },
    vectorStore: {
      provider: "memory",
      config: {
        collectionName: "clawdbot_memories",
        dimension: dims,
      },
    },
    llm: {
      provider: "openai",
      config: {
        apiKey: DUMMY_KEY,
        baseURL: LLM_BASE_URL,
        model: process.env.MEM0_LLM_MODEL || "qwen2.5-1.5b-instruct",
      },
    },
    historyDbPath: HISTORY_DB,
    ...options,
  };

  return new Memory(config);
}

export const USER_ID = "andrew";
