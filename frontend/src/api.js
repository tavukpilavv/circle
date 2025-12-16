const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/+$/, "");

export function apiFetch(path, options = {}) {
  if (!path.startsWith("/")) path = "/" + path;

  const finalOptions = {
    credentials: "include",
    ...options,
  };

  // ✅ FIX: only set JSON header if body is NOT FormData
  if (finalOptions.body && !(finalOptions.body instanceof FormData)) {
    finalOptions.headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };
  } else {
    finalOptions.headers = {
      ...(options.headers || {}),
    };
  }

  return fetch(API_BASE_URL + path, finalOptions);
}
