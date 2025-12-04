"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

// Storage key
const COMPARE_KEY = "beij_compare_items";
const MAX_COMPARE_ITEMS = 2;

export interface CompareContextType {
  compareIds: string[];
  addToCompare: (productId: string) => boolean;
  removeFromCompare: (productId: string) => void;
  clearCompare: () => void;
  isInCompare: (productId: string) => boolean;
  isFull: boolean;
}

const CompareContext = createContext<CompareContextType | undefined>(undefined);

export function CompareProvider({ children }: { children: ReactNode }) {
  const [compareIds, setCompareIds] = useState<string[]>([]);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(COMPARE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed)) {
          setCompareIds(parsed.slice(0, MAX_COMPARE_ITEMS));
        }
      } catch (e) {
        localStorage.removeItem(COMPARE_KEY);
      }
    }
    setIsInitialized(true);
  }, []);

  // Save to localStorage when compareIds changes
  useEffect(() => {
    if (isInitialized) {
      localStorage.setItem(COMPARE_KEY, JSON.stringify(compareIds));
    }
  }, [compareIds, isInitialized]);

  // Add product to compare (returns false if full or already added)
  const addToCompare = (productId: string): boolean => {
    if (compareIds.length >= MAX_COMPARE_ITEMS) {
      return false;
    }
    if (compareIds.includes(productId)) {
      return false;
    }
    setCompareIds(prev => [...prev, productId]);
    return true;
  };

  // Remove product from compare
  const removeFromCompare = (productId: string) => {
    setCompareIds(prev => prev.filter(id => id !== productId));
  };

  // Clear all
  const clearCompare = () => {
    setCompareIds([]);
  };

  // Check if product is in compare
  const isInCompare = (productId: string): boolean => {
    return compareIds.includes(productId);
  };

  const value: CompareContextType = {
    compareIds,
    addToCompare,
    removeFromCompare,
    clearCompare,
    isInCompare,
    isFull: compareIds.length >= MAX_COMPARE_ITEMS,
  };

  return (
    <CompareContext.Provider value={value}>
      {children}
    </CompareContext.Provider>
  );
}

export function useCompare() {
  const context = useContext(CompareContext);
  if (context === undefined) {
    throw new Error("useCompare must be used within a CompareProvider");
  }
  return context;
}

