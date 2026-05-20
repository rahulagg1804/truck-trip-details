export function getApiErrorMessage(err, fallback = "Something went wrong.") {
  if (err?.response?.data?.error) {
    return err.response.data.error;
  }
  if (err?.message) {
    return err.message;
  }
  return fallback;
}
