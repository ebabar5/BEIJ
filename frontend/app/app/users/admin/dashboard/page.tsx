"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../../context/AuthContext";
import {
  getAllUsers,
  getAllProductsAdmin,
  createProductAdmin,
  updateProductAdmin,
  deleteProductAdmin,
  updateUserProfile,
  Product,
  User,
} from "../../../lib/api";

type Tab = "overview" | "products" | "users";

export default function AdminDashboardPage() {
  const router = useRouter();
  const { user, token, logout } = useAuth();
  const [activeTab, setActiveTab] = useState<Tab>("overview");
  const [users, setUsers] = useState<User[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Product form state
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [productForm, setProductForm] = useState({
    product_name: "",
    category: "",
    discounted_price: "",
    actual_price: "",
    discount_percentage: "",
    rating: "",
    rating_count: "",
    about_product: "",
    img_link: "",
    product_link: "",
  });

  // Check if user is admin
  useEffect(() => {
    if (!user || !user.is_admin) {
      router.push("/users/admin");
      return;
    }
    if (!token) {
      router.push("/users/admin");
      return;
    }
    loadData();
  }, [user, token, router]);

  const loadData = async () => {
    if (!token) return;
    setIsLoading(true);
    setError(null);
    try {
      const [usersData, productsData] = await Promise.all([
        getAllUsers(token),
        getAllProductsAdmin(token),
      ]);
      setUsers(usersData);
      setProducts(productsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load data");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;
    try {
      const productData = {
        ...productForm,
        category: productForm.category.split(",").map((c) => c.trim()),
        discounted_price: parseFloat(productForm.discounted_price),
        actual_price: parseFloat(productForm.actual_price),
        discount_percentage: productForm.discount_percentage || "0",
        rating: parseFloat(productForm.rating) || 0,
        rating_count: parseInt(productForm.rating_count) || 0,
      };
      await createProductAdmin(productData, token);
      resetProductForm();
      loadData();
      alert("Product created successfully!");
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to create product");
    }
  };

  const handleUpdateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !editingProduct) return;
    try {
      const productData = {
        ...productForm,
        category: productForm.category.split(",").map((c) => c.trim()),
        discounted_price: parseFloat(productForm.discounted_price),
        actual_price: parseFloat(productForm.actual_price),
        discount_percentage: productForm.discount_percentage || "0",
        rating: parseFloat(productForm.rating) || 0,
        rating_count: parseInt(productForm.rating_count) || 0,
      };
      await updateProductAdmin(editingProduct.product_id, productData, token);
      setEditingProduct(null);
      resetProductForm();
      loadData();
      alert("Product updated successfully!");
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to update product");
    }
  };

  const handleDeleteProduct = async (productId: string) => {
    if (!token) return;
    if (!confirm("Are you sure you want to delete this product?")) return;
    try {
      await deleteProductAdmin(productId, token);
      loadData();
      alert("Product deleted successfully!");
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to delete product");
    }
  };

  const handleEditProduct = (product: Product) => {
    setEditingProduct(product);
    setProductForm({
      product_name: product.product_name,
      category: Array.isArray(product.category) ? product.category.join(", ") : product.category,
      discounted_price: product.discounted_price.toString(),
      actual_price: product.actual_price.toString(),
      discount_percentage: product.discount_percentage || "0",
      rating: product.rating.toString(),
      rating_count: product.rating_count.toString(),
      about_product: product.about_product || "",
      img_link: product.img_link || "",
      product_link: product.product_link || "",
    });
  };

  const resetProductForm = () => {
    setEditingProduct(null);
    setProductForm({
      product_name: "",
      category: "",
      discounted_price: "",
      actual_price: "",
      discount_percentage: "",
      rating: "",
      rating_count: "",
      about_product: "",
      img_link: "",
      product_link: "",
    });
  };

  const handleLogout = async () => {
    await logout();
    router.push("/users/admin");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-red-400 text-xl">Error: {error}</div>
      </div>
    );
  }

  const stats = {
    totalUsers: users.length,
    totalProducts: products.length,
    adminUsers: users.filter((u) => u.is_admin).length,
    averageRating: products.length > 0
      ? (products.reduce((sum, p) => sum + p.rating, 0) / products.length).toFixed(2)
      : "0",
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="bg-slate-800/50 border-b border-amber-500/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-white">Admin Dashboard</h1>
              <p className="text-slate-400 text-sm">Welcome, {user?.username}</p>
            </div>
            <div className="flex gap-4">
              <Link
                href="/"
                className="px-4 py-2 text-slate-300 hover:text-white transition-colors"
              >
                View Site
              </Link>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex gap-2 border-b border-slate-700">
          <button
            onClick={() => setActiveTab("overview")}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === "overview"
                ? "text-amber-400 border-b-2 border-amber-400"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab("products")}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === "products"
                ? "text-amber-400 border-b-2 border-amber-400"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Products ({products.length})
          </button>
          <button
            onClick={() => setActiveTab("users")}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === "users"
                ? "text-amber-400 border-b-2 border-amber-400"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Users ({users.length})
          </button>
        </div>

        {/* Overview Tab */}
        {activeTab === "overview" && (
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <div className="text-slate-400 text-sm mb-2">Total Users</div>
              <div className="text-3xl font-bold text-white">{stats.totalUsers}</div>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <div className="text-slate-400 text-sm mb-2">Total Products</div>
              <div className="text-3xl font-bold text-white">{stats.totalProducts}</div>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <div className="text-slate-400 text-sm mb-2">Admin Users</div>
              <div className="text-3xl font-bold text-white">{stats.adminUsers}</div>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <div className="text-slate-400 text-sm mb-2">Avg Product Rating</div>
              <div className="text-3xl font-bold text-white">{stats.averageRating}</div>
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === "products" && (
          <div className="mt-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-white">Product Management</h2>
              <button
                onClick={resetProductForm}
                className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg transition-colors"
              >
                {editingProduct ? "Cancel Edit" : "+ New Product"}
              </button>
            </div>

            {/* Product Form */}
            {(editingProduct || !editingProduct) && (
              <form
                onSubmit={editingProduct ? handleUpdateProduct : handleCreateProduct}
                className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 mb-6"
              >
                <h3 className="text-lg font-semibold text-white mb-4">
                  {editingProduct ? "Edit Product" : "Create New Product"}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Product Name"
                    value={productForm.product_name}
                    onChange={(e) => setProductForm({ ...productForm, product_name: e.target.value })}
                    required
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="text"
                    placeholder="Category (comma-separated)"
                    value={productForm.category}
                    onChange={(e) => setProductForm({ ...productForm, category: e.target.value })}
                    required
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Discounted Price"
                    value={productForm.discounted_price}
                    onChange={(e) => setProductForm({ ...productForm, discounted_price: e.target.value })}
                    required
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Actual Price"
                    value={productForm.actual_price}
                    onChange={(e) => setProductForm({ ...productForm, actual_price: e.target.value })}
                    required
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="text"
                    placeholder="Discount Percentage"
                    value={productForm.discount_percentage}
                    onChange={(e) => setProductForm({ ...productForm, discount_percentage: e.target.value })}
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="number"
                    step="0.1"
                    placeholder="Rating"
                    value={productForm.rating}
                    onChange={(e) => setProductForm({ ...productForm, rating: e.target.value })}
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="number"
                    placeholder="Rating Count"
                    value={productForm.rating_count}
                    onChange={(e) => setProductForm({ ...productForm, rating_count: e.target.value })}
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="url"
                    placeholder="Image URL"
                    value={productForm.img_link}
                    onChange={(e) => setProductForm({ ...productForm, img_link: e.target.value })}
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <input
                    type="url"
                    placeholder="Product Link"
                    value={productForm.product_link}
                    onChange={(e) => setProductForm({ ...productForm, product_link: e.target.value })}
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500"
                  />
                  <textarea
                    placeholder="About Product"
                    value={productForm.about_product}
                    onChange={(e) => setProductForm({ ...productForm, about_product: e.target.value })}
                    rows={3}
                    className="px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 md:col-span-2"
                  />
                </div>
                <div className="mt-4 flex gap-2">
                  <button
                    type="submit"
                    className="px-6 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg transition-colors"
                  >
                    {editingProduct ? "Update Product" : "Create Product"}
                  </button>
                  {editingProduct && (
                    <button
                      type="button"
                      onClick={resetProductForm}
                      className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
                    >
                      Cancel
                    </button>
                  )}
                </div>
              </form>
            )}

            {/* Products List */}
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-900">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Name</th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Price</th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Rating</th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700">
                    {products.map((product, index) => (
                      <tr key={`${product.product_id}-${index}`} className="hover:bg-slate-800">
                        <td className="px-4 py-3 text-white">{product.product_name}</td>
                        <td className="px-4 py-3 text-white">${product.discounted_price}</td>
                        <td className="px-4 py-3 text-white">{product.rating}</td>
                        <td className="px-4 py-3">
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleEditProduct(product)}
                              className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white text-sm rounded transition-colors"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleDeleteProduct(product.product_id)}
                              className="px-3 py-1 bg-red-600 hover:bg-red-500 text-white text-sm rounded transition-colors"
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === "users" && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-white mb-6">User Management</h2>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-900">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Username</th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Email</th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Role</th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">User ID</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700">
                    {users.map((u, index) => (
                      <tr key={`${u.user_id}-${index}`} className="hover:bg-slate-800">
                        <td className="px-4 py-3 text-white">{u.username}</td>
                        <td className="px-4 py-3 text-white">{u.email}</td>
                        <td className="px-4 py-3">
                          <span
                            className={`px-2 py-1 rounded text-xs font-medium ${
                              u.is_admin
                                ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                                : "bg-slate-700 text-slate-300"
                            }`}
                          >
                            {u.is_admin ? "Admin" : "User"}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-slate-400 text-sm font-mono">{u.user_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

