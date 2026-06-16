/**
 * API Index
 * Central export point for all API functions
 */

export { getPrompts, getPrompt, createPrompt, updatePrompt, deletePrompt } from "./prompts";
export { getCollections, createCollection, deleteCollection } from "./collections";
export { request } from "./client";
