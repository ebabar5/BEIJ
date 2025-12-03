"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

interface FilterSidebarProps {
  categories: string[];
  currentCategory?: string;
  currentMin?: number;
  currentMax?: number;
}

export default function FilterSidebar({
  categories,
  currentCategory,
  currentMin,
  currentMax,
}: FilterSidebarProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [selectedCategory, setSelectedCategory] = useState(currentCategory || "");
  const [minPrice, setMinPrice] = useState(currentMin?.toString() || "");
  const [maxPrice, setMaxPrice] = useState(currentMax?.toString() || "");
  const [isOpen, setIsOpen] = useState(false); // For mobile toggle

  // Update URL when filters change
  const applyFilters = () => {
    const params = new URLSearchParams();
    
    if (selectedCategory) {
      params.set("cat", selectedCategory);
    }
    if (minPrice) {
      params.set("min", minPrice);
    }
    if (maxPrice) {
      params.set("max", maxPrice);
    }

    router.push(`/listings?${params.toString()}`);
  };

  const clearFilters = () => {
    setSelectedCategory("");
    setMinPrice("");
    setMaxPrice("");
    router.push("/listings");
  };

  // Group categories for better display (take top 15)
  const displayCategories = categories.slice(0, 15);

  return (
    <>
      {/* Mobile Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed bottom-4 right-4 z-50 bg-emerald-600 text-white p-4 rounded-full shadow-lg hover:bg-emerald-500 transition-colors"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-9.75 0h9.75" />
        </svg>
      </button>

      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-72 bg-white dark:bg-slate-800 
          border-r border-slate-200 dark:border-slate-700
          transform transition-transform duration-300 ease-in-out
          lg:transform-none lg:transition-none
          ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
          overflow-y-auto
        `}
      >
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Filters</h2>
            <button
              onClick={clearFilters}
              className="text-sm text-emerald-600 hover:text-emerald-500 font-medium"
            >
              Clear all
            </button>
          </div>

          {/* Categories */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Categories</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto pr-2">
              <label className="flex items-center gap-2 cursor-pointer group">
                <input
                  type="radio"
                  name="category"
                  checked={selectedCategory === ""}
                  onChange={() => setSelectedCategory("")}
                  className="w-4 h-4 text-emerald-600 border-slate-300 focus:ring-emerald-500"
                />
                <span className="text-sm text-slate-600 dark:text-slate-400 group-hover:text-slate-900 dark:group-hover:text-white">
                  All Categories
                </span>
              </label>
              {displayCategories.map((cat) => (
                <label key={cat} className="flex items-center gap-2 cursor-pointer group">
                  <input
                    type="radio"
                    name="category"
                    checked={selectedCategory === cat}
                    onChange={() => setSelectedCategory(cat)}
                    className="w-4 h-4 text-emerald-600 border-slate-300 focus:ring-emerald-500"
                  />
                  <span className="text-sm text-slate-600 dark:text-slate-400 group-hover:text-slate-900 dark:group-hover:text-white truncate">
                    {cat.replace(/([A-Z])/g, ' $1').trim()}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Price Range */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Price Range</h3>
            <div className="flex items-center gap-2">
              <div className="relative flex-1">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">₹</span>
                <input
                  type="number"
                  placeholder="Min"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                  className="w-full pl-7 pr-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500"
                />
              </div>
              <span className="text-slate-400">–</span>
              <div className="relative flex-1">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">₹</span>
                <input
                  type="number"
                  placeholder="Max"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                  className="w-full pl-7 pr-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500"
                />
              </div>
            </div>
          </div>

          {/* Apply Button */}
          <button
            onClick={applyFilters}
            className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-lg transition-colors"
          >
            Apply Filters
          </button>

          {/* Close button for mobile */}
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden w-full mt-3 py-3 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 font-medium rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </aside>
    </>
  );
}

