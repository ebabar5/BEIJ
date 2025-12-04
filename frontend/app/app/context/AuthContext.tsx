"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { getSavedItems, saveItem, unsaveItem } from "../lib/api";
import { API_BASE } from "./APIAddress";

// Types for our auth system
export interface User {
  user_id: string;
  username: string;
  email: string;
  is_admin: boolean;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  savedItems: string[];
}

export interface AuthContextType extends AuthState {
  login: (user: User, token: string, rememberMe: boolean) => void;
  logout: () => Promise<void>;
  updateUser: (user: User) => void;
  toggleSaveItem: (productId: string) => Promise<void>;
  isItemSaved: (productId: string) => boolean;
}

// Create the context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Storage keys
const TOKEN_KEY = "beij_auth_token";
const USER_KEY = "beij_auth_user";


// Provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [savedItems, setSavedItems] = useState<string[]>([]);

  // On mount, check for existing auth in localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);

    if (storedToken && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setToken(storedToken);
        setUser(parsedUser);
      } catch (e) {
        // Invalid stored data, clear it
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      }
    }
    setIsLoading(false);
  }, []);

  // Fetch saved items when user logs in
  useEffect(() => {
    if (user) {
      getSavedItems(user.user_id)
        .then(items => setSavedItems(items))
        .catch(err => console.error("Failed to fetch saved items:", err));
    } else {
      setSavedItems([]);
    }
  }, [user]);

  // Login function - stores auth data
  const login = (userData: User, authToken: string, rememberMe: boolean) => {
    setUser(userData);
    setToken(authToken);

    // Always store in localStorage for persistence
    // (In production, you might use httpOnly cookies for tokens)
    if (rememberMe) {
      localStorage.setItem(TOKEN_KEY, authToken);
      localStorage.setItem(USER_KEY, JSON.stringify(userData));
    } else {
      // For session-only, we still use localStorage but could use sessionStorage
      sessionStorage.setItem(TOKEN_KEY, authToken);
      sessionStorage.setItem(USER_KEY, JSON.stringify(userData));
    }
  };

  // Logout function - clears auth data and calls API
  const logout = async () => {
    const currentToken = token || localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY);
    
    // Call logout API to invalidate token on server
    if (currentToken) {
      try {
        await fetch(`${API_BASE}/users/logout`, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${currentToken}`,
          },
        });
      } catch (e) {
        // Even if API call fails, we still clear local state
        console.error("Logout API call failed:", e);
      }
    }

    // Clear state
    setUser(null);
    setToken(null);

    // Clear storage
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
  };

  // Update user data (e.g., after profile edit)
  const updateUser = (userData: User) => {
    setUser(userData);
    
    // Update in storage too
    if (localStorage.getItem(USER_KEY)) {
      localStorage.setItem(USER_KEY, JSON.stringify(userData));
    }
    if (sessionStorage.getItem(USER_KEY)) {
      sessionStorage.setItem(USER_KEY, JSON.stringify(userData));
    }
  };

  // Toggle save/unsave item
  const toggleSaveItem = async (productId: string) => {
    if (!user) {
      throw new Error("Must be logged in to save items");
    }

    try {
      if (savedItems.includes(productId)) {
        // Unsave
        const updatedItems = await unsaveItem(user.user_id, productId);
        setSavedItems(updatedItems);
      } else {
        // Save
        const updatedItems = await saveItem(user.user_id, productId);
        setSavedItems(updatedItems);
      }
    } catch (err) {
      console.error("Failed to toggle save item:", err);
      throw err;
    }
  };

  // Check if item is saved
  const isItemSaved = (productId: string): boolean => {
    return savedItems.includes(productId);
  };

  const value: AuthContextType = {
    user,
    token,
    isLoading,
    isAuthenticated: !!user && !!token,
    savedItems,
    login,
    logout,
    updateUser,
    toggleSaveItem,
    isItemSaved,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

