"use client";

import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { Product, getRecommendations } from "../lib/api";
import ProductCard from "./ProductCard";

interface RecommendationsProps {
  currentProductId: string;
}

export default function Recommendations({ currentProductId }: RecommendationsProps) {
  const { user, isAuthenticated } = useAuth();
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchRecommendations() {
      if (!isAuthenticated || !user) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        // First, ensure the current product view is tracked
        // This ensures recommendations can use it in the analysis
        const { trackProductView } = await import("../lib/api");
        try {
          await trackProductView(user.user_id, currentProductId);
        } catch (trackErr) {
          // If tracking fails, still try to get recommendations
          console.warn("Failed to track product view, continuing with recommendations:", trackErr);
        }
        
        // Then fetch recommendations (which will now include the current product in history)
        const data = await getRecommendations(user.user_id, currentProductId, 8);
        setRecommendations(data);
      } catch (err) {
        // Silently fail - don't show error to user, just don't show recommendations
        console.error("Error fetching recommendations:", err);
        setRecommendations([]);
      } finally {
        setLoading(false);
      }
    }

    fetchRecommendations();
  }, [isAuthenticated, user, currentProductId]);

  // Don't render if user is not logged in
  if (!isAuthenticated || !user) {
    return null;
  }

  if (loading) {
    return (
      <div className="mt-12">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6">Recommended for You</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white dark:bg-slate-800 rounded-xl overflow-hidden shadow-sm border border-slate-200 dark:border-slate-700 animate-pulse">
              <div className="aspect-square bg-slate-200 dark:bg-slate-700" />
              <div className="p-4 space-y-2">
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4" />
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/2" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Don't show error to user - just hide recommendations if there's an error
  if (error) {
    return null;
  }

  if (recommendations.length === 0) {
    return null;
  }

  return (
    <div className="mt-12">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6">Recommended for You</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {recommendations.map((product) => (
          <ProductCard
            key={product.product_id}
            product_id={product.product_id}
            product_name={product.product_name}
            discounted_price={product.discounted_price}
            rating={product.rating}
            img_link={product.img_link}
            actual_price={product.actual_price}
          />
        ))}
      </div>
    </div>
  );
}

