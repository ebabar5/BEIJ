"use client";

import { useState } from "react";

interface LivePriceButtonProps {
  amazonURL: string;
}

// Get the live price from Amazon using the product link
// Note: This may be unreliable due to Amazon's bot detection
async function getLivePrice(amazonURL: string): Promise<string | null> {
  // check URL exists
  if (!amazonURL) {
    return null;
  }

  try {
    // Use Next.js API route to proxy the request and avoid CORS issues
    const apiUrl = `/api/live-price?url=${encodeURIComponent(amazonURL)}`;
    const res = await fetch(apiUrl);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      console.log("Live price fetch failed:", errorData.message || res.status);
      return null;
    }

    const data = await res.json();

    if (data.success && data.price) {
      return data.price;
    }

    console.log("Could not fetch live price:", data.message || "Unknown error");
    return null;

  } catch (error) {
    // handle network errors
    console.error("Error fetching live price:", error);
    return null;
  }
}

export default function LivePriceButton({ amazonURL }: LivePriceButtonProps) {
  const [price, setPrice] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetchPrice = async () => {
    setLoading(true);
    setError(null);
    setPrice(null);

    try {
      const fetchedPrice = await getLivePrice(amazonURL);
      if (fetchedPrice) {
        setPrice(fetchedPrice);
      } else {
        setError("Could not fetch live price. Please try again.");
      }
    } catch (err) {
      setError("Failed to fetch live price. Please try again.");
      console.error("Error fetching live price:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-3">
      <button
        onClick={handleFetchPrice}
        disabled={loading}
        className={`
          inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all
          ${loading
            ? "bg-slate-300 dark:bg-slate-600 text-slate-500 dark:text-slate-400 cursor-not-allowed"
            : "bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm hover:shadow-md"
          }
        `}
      >
        {loading ? (
          <>
            <svg
              className="animate-spin h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>Fetching...</span>
          </>
        ) : (
          <>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-4 h-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"
              />
            </svg>
            <span>Get Live Price</span>
          </>
        )}
      </button>

      {price && (
        <div className="mt-3 flex items-center gap-2">
          <span className="text-lg font-semibold text-emerald-600 dark:text-emerald-400">
            Amazon Live Price: ₹{price}
          </span>
          <span className="text-xs text-slate-500 dark:text-slate-400">
            (fetched from Amazon)
          </span>
        </div>
      )}

      {error && (
        <div className="mt-3 flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="w-4 h-4"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
            />
          </svg>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
