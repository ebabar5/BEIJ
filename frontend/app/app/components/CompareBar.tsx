"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useCompare } from "../context/CompareContext";

interface ProductPreview {
  product_id: string;
  product_name: string;
  img_link?: string;
  discounted_price: number;
}

const API_BASE = "http://localhost:8000/api/v1";

export default function CompareBar() {
  const { compareIds, removeFromCompare, clearCompare } = useCompare();
  const [products, setProducts] = useState<ProductPreview[]>([]);
  const [isMinimized, setIsMinimized] = useState(false);

  // Fetch product details when compareIds changes
  useEffect(() => {
    if (compareIds.length === 0) {
      setProducts([]);
      return;
    }

    const fetchProducts = async () => {
      try {
        const results = await Promise.all(
          compareIds.map(async (id) => {
            const res = await fetch(`${API_BASE}/products/${id}`);
            if (!res.ok) return null;
            return res.json();
          })
        );
        setProducts(results.filter((p): p is ProductPreview => p !== null));
      } catch (err) {
        console.error("Failed to fetch compare products:", err);
      }
    };

    fetchProducts();
  }, [compareIds]);

  // Don't render if no items
  if (compareIds.length === 0) {
    return null;
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50">
      {/* Minimized bar */}
      {isMinimized ? (
        <div className="bg-indigo-600 text-white px-4 py-2 flex items-center justify-between">
          <button
            onClick={() => setIsMinimized(false)}
            className="flex items-center gap-2 hover:bg-indigo-500 px-3 py-1 rounded transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
            </svg>
            <span className="font-medium">Compare ({compareIds.length}/2)</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
            </svg>
          </button>
        </div>
      ) : (
        /* Expanded bar */
        <div className="bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 shadow-lg">
          <div className="max-w-4xl mx-auto px-4 py-4">
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-indigo-600 dark:text-indigo-400">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                </svg>
                <span className="font-medium text-slate-900 dark:text-white">
                  Compare ({compareIds.length}/2)
                </span>
              </div>
              <button
                onClick={() => setIsMinimized(true)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                </svg>
              </button>
            </div>

            {/* Products */}
            <div className="flex items-center gap-4">
              {/* Product slots */}
              <div className="flex-1 flex gap-3">
                {[0, 1].map((index) => {
                  const product = products[index];
                  const productId = compareIds[index];

                  if (!productId) {
                    // Empty slot
                    return (
                      <div
                        key={index}
                        className="flex-1 h-20 border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-lg flex items-center justify-center text-slate-400 dark:text-slate-500 text-sm"
                      >
                        Select a product
                      </div>
                    );
                  }

                  return (
                    <div
                      key={productId}
                      className="flex-1 bg-slate-50 dark:bg-slate-900 rounded-lg p-2 flex items-center gap-3 relative group"
                    >
                      {/* Remove button */}
                      <button
                        onClick={() => removeFromCompare(productId)}
                        className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>

                      {/* Image */}
                      <div className="w-16 h-16 bg-white dark:bg-slate-800 rounded flex-shrink-0 flex items-center justify-center">
                        {product?.img_link ? (
                          <img
                            src={product.img_link}
                            alt={product.product_name}
                            className="w-full h-full object-contain p-1"
                          />
                        ) : (
                          <div className="w-8 h-8 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
                        )}
                      </div>

                      {/* Info */}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-900 dark:text-white truncate">
                          {product?.product_name || "Loading..."}
                        </p>
                        <p className="text-sm text-indigo-600 dark:text-indigo-400 font-semibold">
                          {product?.discounted_price
                            ? `₹${product.discounted_price.toLocaleString()}`
                            : "..."}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Actions */}
              <div className="flex items-center gap-2">
                <Link
                  href="/compare"
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    compareIds.length === 2
                      ? "bg-indigo-600 hover:bg-indigo-500 text-white"
                      : "bg-slate-200 dark:bg-slate-700 text-slate-400 cursor-not-allowed pointer-events-none"
                  }`}
                >
                  Compare
                </Link>
                <button
                  onClick={clearCompare}
                  className="px-3 py-2 text-slate-500 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                >
                  Clear
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

