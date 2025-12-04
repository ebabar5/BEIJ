"use client";

import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";
const API_BASE = "http://localhost:8000/api/v1";

interface Props {
  productId: string;
}

export default function RecordProductView({ productId }: Props) {
  const { user } = useAuth();

  useEffect(() => {
    console.log("[RecordProductView] user:", user, "productId:", productId);

    if (!user || !productId) return;

    fetch(`${API_BASE}/users/${user.user_id}/recently-viewed/${productId}`, {
      method: "POST",
    })
      .then((res) => {
        console.log(
          "[RecordProductView] POST recently-viewed status:",
          res.status
        );
      })
      .catch((err) => {
        console.error("[RecordProductView] POST error:", err);
      });
  }, [user, productId]);

  return null;
}
