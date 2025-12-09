const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/+$/, "");

export function apiFetch(path, options = {}) {
  if (!path.startsWith("/")) path = "/" + path;

  const finalOptions = {
    credentials: "include",
    ...options,
  };

  // Only add JSON header when body exists
  if (finalOptions.body) {
    finalOptions.headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };
  }

  return fetch(API_BASE_URL + path, finalOptions);
}
