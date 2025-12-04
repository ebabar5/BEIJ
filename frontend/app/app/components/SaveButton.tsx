"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../context/AuthContext";

interface SaveButtonProps {
  productId: string;
  className?: string;
  showText?: boolean;
}

export default function SaveButton({ productId, className = "", showText = true }: SaveButtonProps) {
  const router = useRouter();
  const { isAuthenticated, isItemSaved, toggleSaveItem } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isSaved = isItemSaved(productId);

  const handleClick = async () => {
    if (!isAuthenticated) {
      // Redirect to login
      router.push("/users/login");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await toggleSaveItem(productId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save item");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={isLoading}
      className={`flex items-center justify-center gap-2 transition-colors ${
        isSaved
          ? "bg-pink-600 hover:bg-pink-500 text-white"
          : "bg-emerald-600 hover:bg-emerald-500 text-white"
      } ${isLoading ? "opacity-50 cursor-not-allowed" : ""} ${className}`}
      title={isSaved ? "Remove from saved" : "Save item"}
    >
      {isLoading ? (
        <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      ) : (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill={isSaved ? "currentColor" : "none"}
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-5 h-5"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
          />
        </svg>
      )}
      {showText && (
        <span>{isSaved ? "Saved" : "Save Item"}</span>
      )}
    </button>
  );
}

