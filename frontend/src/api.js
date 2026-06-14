const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Request failed with status ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function getPrompts() {
  return request("/prompts");
}

export function createPrompt(prompt) {
  return request("/prompts", {
    method: "POST",
    body: JSON.stringify(prompt),
  });
}

export function updatePrompt(id, prompt) {
  return request(`/prompts/${id}`, {
    method: "PUT",
    body: JSON.stringify(prompt),
  });
}

export function deletePrompt(id) {
  return request(`/prompts/${id}`, {
    method: "DELETE",
  });
}

export function getCollections() {
  return request("/collections");
}

export function createCollection(collection) {
  return request("/collections", {
    method: "POST",
    body: JSON.stringify(collection),
  });
}