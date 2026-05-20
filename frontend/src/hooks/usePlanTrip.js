import { useState, useCallback } from "react";
import { planTrip } from "../api";
import { getApiErrorMessage } from "../utils/errors";

const API_UNAVAILABLE =
  "Could not reach the API. Start the Django server on port 8000.";

export function usePlanTrip() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const submit = useCallback(async (form) => {
    setLoading(true);
    setError(null);
    try {
      const data = await planTrip(form);
      setResult(data);
    } catch (err) {
      setError(getApiErrorMessage(err, API_UNAVAILABLE));
      setResult(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setError(null);
    setResult(null);
  }, []);

  return { loading, error, result, submit, reset };
}
