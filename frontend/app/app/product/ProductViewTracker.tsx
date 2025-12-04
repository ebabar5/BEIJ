"use client";

import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { trackProductView } from "../lib/api";

interface ProductViewTrackerProps {
  productId: string;
}

export default function ProductViewTracker({ productId }: ProductViewTrackerProps) {
  const { user, isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated && user && productId) {
      // Track the view asynchronously (don't block page load)
      trackProductView(user.user_id, productId).catch((err) => {
        // Silently fail - don't disrupt user experience
        console.error("Failed to track product view:", err);
      });
    }
  }, [isAuthenticated, user, productId]);

  return null; // This component doesn't render anything
}

