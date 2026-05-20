import axios from "axios";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "",
  timeout: 120000,
  headers: { "Content-Type": "application/json" },
});

export async function planTrip(payload) {
  const { data } = await client.post("/api/plan-trip/", payload);
  return data;
}
