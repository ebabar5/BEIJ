"use client";

import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { trackProductView } from "../lib/api";

interface ProductViewTrackerProps {
  productId: string;
}

export default function ProductViewTracker({
  productId,
}: ProductViewTrackerProps) {
  const { user, isAuthenticated } = useAuth();
  const userId = user?.user_id;

  useEffect(() => {
    if (!isAuthenticated || !userId || !productId) return;

    // Fire-and-forget; trackProductView already swallows errors
    void trackProductView(userId, productId);
  }, [isAuthenticated, userId, productId]);

  return null;
}
