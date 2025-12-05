// API utility functions for BEIJ frontend
// This file contains all the functions to communicate with the backend

// Central API base URL for all API calls.

const isServer = typeof window === "undefined";

export const API_BASE = isServer
  // inside the Next.js container → talk to Docker service "backend"
  ? process.env.INTERNAL_API_URL ?? "http://backend:8000/api/v1"
  // in the browser → talk to localhost
  : process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";


// ============================================
// Types
// ============================================

export interface User {
  user_id: string;
  username: string;
  email: string;
  is_admin: boolean;
}

export interface LoginResponse {
  user: User;
  token: string;
  expires_in: number;
}

export interface ApiError {
  message: string;
  code: string;
}

// ============================================
// Auth API Functions
// ============================================

/**
 * Register a new user
 * POST /api/v1/users/register
 */
export async function registerUser(
  username: string,
  email: string,
  password: string
): Promise<User> {
  const response = await fetch(`${API_BASE}/users/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Registration failed");
  }

  return response.json();
}

/**
 * Login a user
 * POST /api/v1/users/login
 */
export async function loginUser(
  usernameOrEmail: string,
  password: string,
  rememberMe: boolean = false
): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username_or_email: usernameOrEmail,
      password: password,
      remember_me: rememberMe,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Login failed");
  }

  return response.json();
}

/**
 * Register a new admin user
 * POST /api/v1/users/admin/register?admin_secret=XXX
 */
export async function registerAdmin(
  username: string,
  email: string,
  password: string,
  adminSecret: string
): Promise<User> {
  const response = await fetch(`${API_BASE}/users/admin/register?admin_secret=${encodeURIComponent(adminSecret)}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Admin registration failed");
  }

  return response.json();
}

/**
 * Login as admin
 * POST /api/v1/users/admin/login
 */
export async function loginAdmin(
  usernameOrEmail: string,
  password: string,
  rememberMe: boolean = false
): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE}/users/admin/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username_or_email: usernameOrEmail,
      password: password,
      remember_me: rememberMe,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Admin login failed");
  }

  return response.json();
}

/**
 * Logout user
 * POST /api/v1/users/logout
 */
export async function logoutUser(token: string): Promise<void> {
  const response = await fetch(`${API_BASE}/users/logout`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Logout failed");
  }
}

/**
 * Get user profile
 * GET /api/v1/users/{user_id}
 */
export async function getUserProfile(userId: string): Promise<User> {
  const response = await fetch(`${API_BASE}/users/${userId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to get profile");
  }

  return response.json();
}

/**
 * Update user profile
 * PUT /api/v1/users/{user_id}
 */
export async function updateUserProfile(
  userId: string,
  updates: {
    username?: string;
    email?: string;
    password?: string;
  }
): Promise<User> {
  const response = await fetch(`${API_BASE}/users/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to update profile");
  }

  return response.json();
}

// ============================================
// Products API Functions
// ============================================

export interface Product {
  product_id: string;
  product_name: string;
  category: string[];
  discounted_price: number;
  actual_price: number;
  discount_percentage: string;
  rating: number;
  rating_count: number;
  about_product: string;
  img_link: string;
  product_link: string;
}

export interface ProductPreview {
  product_id: string;
  product_name: string;
  discounted_price: number;
  rating: number;
}

/**
 * Get all product previews
 * GET /api/v1/previews/
 */
export async function getProductPreviews(): Promise<ProductPreview[]> {
  const response = await fetch(`${API_BASE}/previews/`);

  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json();
}

/**
 * Get filtered product previews
 * GET /api/v1/previews/{filter}
 */
export async function getFilteredPreviews(filter: string): Promise<ProductPreview[]> {
  const response = await fetch(`${API_BASE}/previews/${filter}`);

  if (!response.ok) {
    throw new Error("Failed to fetch filtered products");
  }

  return response.json();
}

/**
 * Get a single product by ID
 * GET /api/v1/products/{product_id}
 */
export async function getProduct(productId: string): Promise<Product> {
  const response = await fetch(`${API_BASE}/products/${productId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Product not found");
  }

  return response.json();
}

/**
 * Search products by keyword
 * GET /api/v1/previews/search/{search_string}
 */
export async function searchProducts(
  keywords: string,
  filter?: string
): Promise<ProductPreview[]> {
  const searchPath = filter 
    ? `${keywords}&${filter}` 
    : keywords;
  
  const response = await fetch(`${API_BASE}/previews/search/${searchPath}`);

  if (!response.ok) {
    throw new Error("Search failed");
  }

  return response.json();
}

// ============================================
// Saved Items API Functions
// ============================================

/**
 * Save an item to user's list
 * POST /api/v1/users/{user_id}/saved-items/{product_id}
 */
export async function saveItem(userId: string, productId: string): Promise<string[]> {
  const response = await fetch(`${API_BASE}/users/${userId}/saved-items/${productId}`, {
    method: "POST",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to save item");
  }

  const data = await response.json();
  return data.saved_item_ids;
}

/**
 * Remove an item from user's saved list
 * DELETE /api/v1/users/{user_id}/saved-items/{product_id}
 */
export async function unsaveItem(userId: string, productId: string): Promise<string[]> {
  const response = await fetch(`${API_BASE}/users/${userId}/saved-items/${productId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to remove item");
  }

  const data = await response.json();
  return data.saved_item_ids;
}

/**
 * Get user's saved items
 * GET /api/v1/users/{user_id}/saved-items
 */
export async function getSavedItems(userId: string): Promise<string[]> {
  const response = await fetch(`${API_BASE}/users/${userId}/saved-items`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to get saved items");
  }

  const data = await response.json();
  return data.saved_item_ids;
}

// ============================================
// View History & Recommendations API Functions
// ============================================

/**
 * Track a product view
 * POST /api/v1/users/{user_id}/recently-viewed/{product_id}
 */
export async function trackProductView(userId: string, productId: string): Promise<void> {
  try {
    const response = await fetch(`${API_BASE}/users/${userId}/view-history/${productId}`, {
      method: "POST",
    });

    if (!response.ok) {
      if (process.env.NODE_ENV === "development") {
        let body: unknown;
        try {
          body = await response.json();
        } catch {
          body = await response.text().catch(() => null);
        }
        console.warn("[trackProductView] non-OK:", response.status, body);
      } else {
        // Silently fail - this is a non-critical feature
        console.warn(`Failed to track product view: ${response.status}`);
      }
      return;
    }
  } catch (err) {
    if (process.env.NODE_ENV === "development") {
      console.warn("[trackProductView] error:", err);
    } else if (err instanceof TypeError && err.message === "Failed to fetch") {
      // Silently handle network errors - this is a non-critical feature
      console.warn("Network error tracking product view - backend may be unreachable");
    }
    // Don't throw – tracking is best-effort
    return;
  }
}


/**
 * Get user's viewing history
 * GET /api/v1/users/{user_id}/view-history
 */
export async function getViewHistory(
  userId: string,
): Promise<Array<{ product_id: string; viewed_at: string }>> {
  try {
    const response = await fetch(`${API_BASE}/users/${userId}/view-history`);

    if (!response.ok) {
      if (process.env.NODE_ENV === "development") {
        let body: unknown;
        try {
          body = await response.json();
        } catch {
          body = await response.text().catch(() => null);
        }
        console.warn(
          "[getViewHistory] non-OK:",
          response.status,
          body,
        );
      }
      return [];
    }

    const data = await response.json();
    return data.recently_viewed || [];
  } catch (err) {
    if (process.env.NODE_ENV === "development") {
      console.warn("[getViewHistory] error:", err);
    }
    return [];
  }
}

/**
 * Get product recommendations for a user
 * GET /api/v1/users/{user_id}/recommendations?exclude_product_id=XXX&limit=8
 */
export async function getRecommendations(
  userId: string,
  excludeProductId?: string,
  limit: number = 8
): Promise<Product[]> {
  const params = new URLSearchParams();
  if (excludeProductId) {
    params.set("exclude_product_id", excludeProductId);
  }
  params.set("limit", limit.toString());

  try {
    const response = await fetch(
      `${API_BASE}/users/${userId}/recommendations?${params.toString()}`
    );

    if (!response.ok) {
      if (process.env.NODE_ENV === "development") {
        let body: unknown;
        try {
          body = await response.json();
        } catch {
          body = await response.text().catch(() => null);
        }
        console.warn("[getRecommendations] non-OK:", response.status, body);
      } else {
        // Silently fail - return empty array for non-critical feature
        console.warn(`Failed to get recommendations: ${response.status}`);
      }
      return [];
    }

    return response.json();
  } catch (err) {
    if (process.env.NODE_ENV === "development") {
      console.warn("[getRecommendations] error:", err);
    } else if (err instanceof TypeError && err.message === "Failed to fetch") {
      // Handle all errors gracefully - return empty array for non-critical feature
      console.warn("Network error getting recommendations - backend may be unreachable");
    }
    // Return empty array instead of throwing
    return [];
  }
}



// ============================================
// Admin API Functions
// ============================================

/**
 * Get all users (admin only)
 * GET /api/v1/users/
 */
export async function getAllUsers(token: string): Promise<User[]> {
  const response = await fetch(`${API_BASE}/users/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Failed to get users" }));
    throw new Error(error.message || "Failed to get users");
  }

  return response.json();
}

/**
 * Create a new product (admin only)
 * POST /api/v1/products/
 */
export async function createProductAdmin(
  product: Partial<Product>,
  token: string
): Promise<Product> {
  const response = await fetch(`${API_BASE}/products/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(product),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Failed to create product" }));
    throw new Error(error.message || "Failed to create product");
  }

  return response.json();
}

/**
 * Update a product (admin only)
 * PUT /api/v1/products/{product_id}
 */
export async function updateProductAdmin(
  productId: string,
  product: Partial<Product>,
  token: string
): Promise<Product> {
  const response = await fetch(`${API_BASE}/products/${productId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(product),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Failed to update product" }));
    throw new Error(error.message || "Failed to update product");
  }

  return response.json();
}

/**
 * Delete a product (admin only)
 * DELETE /api/v1/products/{product_id}
 */
export async function deleteProductAdmin(
  productId: string,
  token: string
): Promise<void> {
  const response = await fetch(`${API_BASE}/products/${productId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Failed to delete product" }));
    throw new Error(error.message || "Failed to delete product");
  }
}

/**
 * Get all products (admin only)
 * GET /api/v1/products/
 */
export async function getAllProductsAdmin(token: string): Promise<Product[]> {
  const response = await fetch(`${API_BASE}/products/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Failed to get products" }));
    throw new Error(error.message || "Failed to get products");
  }

  return response.json();
}


