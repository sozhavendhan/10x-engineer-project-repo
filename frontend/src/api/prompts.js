/**
 * Prompts API
 * All prompt-related API endpoints
 */

import { request } from "./client";

/**
 * Fetch all prompts
 * @returns {Promise<Array>} List of prompts
 */
export function getPrompts() {
  return request("/prompts");
}

/**
 * Fetch a single prompt by ID
 * @param {string|number} id - The prompt ID
 * @returns {Promise<Object>} The prompt object
 */
export function getPrompt(id) {
  return request(`/prompts/${id}`);
}

/**
 * Create a new prompt
 * @param {Object} prompt - Prompt data (title, content, description, tags, collection_id)
 * @returns {Promise<Object>} The created prompt
 */
export function createPrompt(prompt) {
  return request("/prompts", {
    method: "POST",
    body: JSON.stringify(prompt),
  });
}

/**
 * Update an existing prompt
 * @param {string|number} id - The prompt ID
 * @param {Object} prompt - Updated prompt data
 * @returns {Promise<Object>} The updated prompt
 */
export function updatePrompt(id, prompt) {
  return request(`/prompts/${id}`, {
    method: "PUT",
    body: JSON.stringify(prompt),
  });
}

/**
 * Delete a prompt
 * @param {string|number} id - The prompt ID
 * @returns {Promise<null>}
 */
export function deletePrompt(id) {
  return request(`/prompts/${id}`, {
    method: "DELETE",
  });
}
