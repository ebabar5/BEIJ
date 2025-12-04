"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
// adjust this import to match your auth context file name/path
import { useAuth } from "../context/AuthContext";

const API_BASE = "http://localhost:8000/api/v1";

type Product = {
  product_id: string;
  product_name: string;
  discounted_price: number;
  rating: number;
  img_link?: string | null;
};

export default function RecentlyViewedSection() {
  const { user } = useAuth(); // assumes user.user_id exists when logged in
  const [items, setItems] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) {
      setItems([]);
      return;
    }

    setLoading(true);
    fetch(`${API_BASE}/users/${user.user_id}/recently-viewed?limit=4`)
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => setItems(Array.isArray(data) ? data : []))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [user]);

  // if no user or nothing viewed yet -> hide section
  if (!user || items.length === 0) return null;

  return (
    <section className="py-16 lg:py-24 bg-slate-50 dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white">
              Recently Viewed
            </h2>
            <p className="text-slate-500 dark:text-slate-400 mt-2">
              The last products you looked at.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {items.map((product) => (
            <Link
              key={product.product_id}
              href={`/product?id=${product.product_id}`}
              className="group bg-white dark:bg-slate-800 rounded-xl overflow-hidden border border-slate-200 dark:border-slate-700 hover:border-emerald-500/50 hover:shadow-lg transition-all"
            >
              <div className="aspect-square bg-slate-50 dark:bg-slate-900 p-4">
                {product.img_link ? (
                  <img
                    src={product.img_link}
                    alt={product.product_name}
                    className="w-full h-full object-contain group-hover:scale-105 transition-transform"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1}
                      stroke="currentColor"
                      className="w-12 h-12 text-slate-300"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5 
                           1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 
                           3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75
                           A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 
                           0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
                      />
                    </svg>
                  </div>
                )}
              </div>
              <div className="p-4">
                <h3 className="text-sm font-medium text-slate-900 dark:text-white line-clamp-2 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                  {product.product_name}
                </h3>
                <div className="flex items-center gap-1 mt-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    className="w-4 h-4 text-amber-400"
                  >
                    <path d="M11.48 3.499a.562.562 0 011.04 0l2.125 
                      5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 
                      3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 
                      01-.84.61l-4.725-2.885a.563.563 0 00-.586 
                      0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 
                      0 00-.182-.557l-4.204-3.602a.563.563 0 
                      01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                  </svg>
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    {product.rating}
                  </span>
                </div>
                <p className="text-lg font-bold text-slate-900 dark:text-white mt-2">
                  ₹{product.discounted_price?.toLocaleString()}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
