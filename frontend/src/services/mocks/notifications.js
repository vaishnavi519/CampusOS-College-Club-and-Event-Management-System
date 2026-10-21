import api from "../api.js";
import { ApiError } from "../errors.js";

function handleError(error) {
  if (error instanceof ApiError) throw error;

  const status = error.response?.status || 500;
  const data = error.response?.data;

  throw new ApiError(
    data?.message ||
      data?.detail ||
      "Unable to load notifications. Please try again.",
    { status }
  );
}

async function request(callback) {
  try {
    const response = await callback();
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

export async function listNotifications() {
  return request(() => api.get("/notifications"));
}

export async function countUnread() {
  const data = await request(() =>
    api.get("/notifications/unread-count")
  );

  return data.count;
}

export async function markRead(id) {
  const data = await request(() =>
    api.patch(`/notifications/${id}/read`)
  );

  return data.notification;
}

export async function markAllRead() {
  return request(() =>
    api.patch("/notifications/read-all")
  );
}