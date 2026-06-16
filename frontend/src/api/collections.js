/**
 * Collections API
 * All collection-related API endpoints
 */

import { request } from "./client";

/**
 * Fetch all collections
 * @returns {Promise<Array>} List of collections
 */
export async function getCollections() {
  const response = await request("/collections");
  return response?.collections || [];
}

/**
 * Create a new collection
 * @param {Object} collection - Collection data (name, description)
 * @returns {Promise<Object>} The created collection
 */
export function createCollection(collection) {
  return request("/collections", {
    method: "POST",
    body: JSON.stringify(collection),
  });
}

/**
 * Delete a collection
 * @param {string|number} id - The collection ID
 * @returns {Promise<null>}
 */
export function deleteCollection(id) {
  return request(`/collections/${id}`, {
    method: "DELETE",
  });
}
