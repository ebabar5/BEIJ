"use client";

import { useCompare } from "../context/CompareContext";

interface CompareButtonProps {
  productId: string;
  variant?: "icon" | "full";
  className?: string;
}

export default function CompareButton({ 
  productId, 
  variant = "full",
  className = "" 
}: CompareButtonProps) {
  const { isInCompare, addToCompare, removeFromCompare, isFull } = useCompare();
  
  const isSelected = isInCompare(productId);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (isSelected) {
      removeFromCompare(productId);
    } else {
      addToCompare(productId);
    }
  };

  // Icon-only variant (for ProductCard)
  if (variant === "icon") {
    return (
      <button
        onClick={handleClick}
        disabled={!isSelected && isFull}
        className={`p-2 rounded-lg transition-all ${
          isSelected
            ? "bg-indigo-600 text-white"
            : isFull
            ? "bg-slate-200 dark:bg-slate-700 text-slate-400 cursor-not-allowed"
            : "bg-white/90 dark:bg-slate-800/90 text-slate-600 dark:text-slate-300 hover:bg-indigo-100 dark:hover:bg-indigo-900/30 hover:text-indigo-600 dark:hover:text-indigo-400"
        } ${className}`}
        title={isSelected ? "Remove from compare" : isFull ? "Compare full (2 max)" : "Add to compare"}
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
        </svg>
      </button>
    );
  }

  // Full button variant (for Product detail page)
  return (
    <button
      onClick={handleClick}
      disabled={!isSelected && isFull}
      className={`flex items-center justify-center gap-2 px-6 py-3 font-medium rounded-lg transition-colors ${
        isSelected
          ? "bg-indigo-600 hover:bg-indigo-500 text-white"
          : isFull
          ? "bg-slate-300 dark:bg-slate-700 text-slate-500 cursor-not-allowed"
          : "bg-slate-200 dark:bg-slate-700 hover:bg-indigo-100 dark:hover:bg-indigo-900/30 text-slate-700 dark:text-slate-300 hover:text-indigo-600 dark:hover:text-indigo-400"
      } ${className}`}
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
        <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
      </svg>
      {isSelected ? "Added" : isFull ? "Compare Full" : "Compare"}
    </button>
  );
}

