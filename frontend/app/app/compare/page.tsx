"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useCompare } from "../context/CompareContext";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { API_BASE } from "../context/APIAddress";

interface Product {
  product_id: string;
  product_name: string;
  discounted_price: number;
  actual_price: number;
  rating: number;
  rating_count: number;
  img_link?: string;
  product_link?: string;
  category?: string[];
}

export default function ComparePage() {
  const { compareIds, removeFromCompare, clearCompare } = useCompare();
  const [products, setProducts] = useState<(Product | null)[]>([null, null]);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch product details
  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        const results = await Promise.all(
          [0, 1].map(async (index) => {
            const id = compareIds[index];
            if (!id) return null;
            const res = await fetch(`${API_BASE}/products/${id}`);
            if (!res.ok) return null;
            return res.json();
          })
        );
        setProducts(results);
      } catch (err) {
        console.error("Failed to fetch products:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [compareIds]);

  const product1 = products[0];
  const product2 = products[1];

  // Calculate discount percentages
  const getDiscount = (p: Product | null) => {
    if (!p || !p.actual_price || p.actual_price <= p.discounted_price) return 0;
    return Math.round((1 - p.discounted_price / p.actual_price) * 100);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col">
      <Header />

      <div className="flex-1 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
            Compare Products
          </h1>
          <p className="text-slate-500 dark:text-slate-400">
            {compareIds.length === 0
              ? "Select 2 products to compare"
              : compareIds.length === 1
              ? "Add one more product to compare"
              : "Side-by-side comparison"}
          </p>
        </div>

        {/* Empty State */}
        {compareIds.length === 0 && (
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 p-12 text-center">
            <div className="w-20 h-20 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="w-10 h-10 text-indigo-600 dark:text-indigo-400">
                <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
              No products to compare
            </h2>
            <p className="text-slate-500 dark:text-slate-400 mb-6 max-w-sm mx-auto">
              Browse products and click the compare icon to add items for comparison.
            </p>
            <Link
              href="/listings"
              className="inline-flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg transition-colors"
            >
              Browse Products
            </Link>
          </div>
        )}

        {/* Loading State */}
        {compareIds.length > 0 && isLoading && (
          <div className="flex items-center justify-center py-16">
            <div className="animate-spin h-8 w-8 border-2 border-indigo-500 border-t-transparent rounded-full"></div>
          </div>
        )}

        {/* Comparison Table */}
        {compareIds.length > 0 && !isLoading && (
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
            {/* Images Row */}
            <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-700">
              {[product1, product2].map((product, index) => (
                <div
                  key={index}
                  className={`p-6 ${index === 0 ? "border-r border-slate-200 dark:border-slate-700" : ""}`}
                >
                  {product ? (
                    <div className="aspect-square bg-slate-100 dark:bg-slate-900 rounded-xl overflow-hidden flex items-center justify-center relative group">
                      {product.img_link ? (
                        <img
                          src={product.img_link}
                          alt={product.product_name}
                          className="w-full h-full object-contain p-4"
                        />
                      ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="w-16 h-16 text-slate-300 dark:text-slate-600">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                        </svg>
                      )}
                      {/* Remove button */}
                      <button
                        onClick={() => removeFromCompare(product.product_id)}
                        className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  ) : (
                    <div className="aspect-square bg-slate-100 dark:bg-slate-900 rounded-xl flex items-center justify-center">
                      <div className="text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-2">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                        <p className="text-slate-400 dark:text-slate-500 text-sm">Add a product</p>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Product Name Row */}
            <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-700">
              {[product1, product2].map((product, index) => (
                <div
                  key={index}
                  className={`p-4 ${index === 0 ? "border-r border-slate-200 dark:border-slate-700" : ""}`}
                >
                  <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-1">Product</p>
                  <p className="font-medium text-slate-900 dark:text-white line-clamp-2">
                    {product?.product_name || "—"}
                  </p>
                </div>
              ))}
            </div>

            {/* Price Row */}
            <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-700 bg-indigo-50 dark:bg-indigo-900/20">
              {[product1, product2].map((product, index) => (
                <div
                  key={index}
                  className={`p-4 ${index === 0 ? "border-r border-slate-200 dark:border-slate-700" : ""}`}
                >
                  <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-1">Price</p>
                  <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                    {product?.discounted_price ? `₹${product.discounted_price.toLocaleString()}` : "—"}
                  </p>
                </div>
              ))}
            </div>

            {/* Original Price Row */}
            <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-700">
              {[product1, product2].map((product, index) => (
                <div
                  key={index}
                  className={`p-4 ${index === 0 ? "border-r border-slate-200 dark:border-slate-700" : ""}`}
                >
                  <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-1">Original Price</p>
                  <p className="text-slate-500 dark:text-slate-400 line-through">
                    {product?.actual_price ? `₹${product.actual_price.toLocaleString()}` : "—"}
                  </p>
                </div>
              ))}
            </div>

            {/* Discount Row */}
            <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-700">
              {[product1, product2].map((product, index) => {
                const discount = getDiscount(product);
                return (
                  <div
                    key={index}
                    className={`p-4 ${index === 0 ? "border-r border-slate-200 dark:border-slate-700" : ""}`}
                  >
                    <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-1">Discount</p>
                    <p className={`font-medium ${discount > 0 ? "text-green-600 dark:text-green-400" : "text-slate-400"}`}>
                      {discount > 0 ? `${discount}% off` : "—"}
                    </p>
                  </div>
                );
              })}
            </div>

            {/* Rating Row */}
            <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-700">
              {[product1, product2].map((product, index) => (
                <div
                  key={index}
                  className={`p-4 ${index === 0 ? "border-r border-slate-200 dark:border-slate-700" : ""}`}
                >
                  <p className="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-1">Rating</p>
                  {product ? (
                    <div className="flex items-center gap-2">
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <svg
                            key={i}
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill={i < Math.floor(product.rating) ? "currentColor" : "none"}
                            stroke="currentColor"
                            className={`w-4 h-4 ${i < Math.floor(product.rating) ? "text-amber-400" : "text-slate-300 dark:text-slate-600"}`}
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={i < Math.floor(product.rating) ? 0 : 1.5} d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                          </svg>
                        ))}
                      </div>
                      <span className="text-slate-700 dark:text-slate-300 font-medium">{product.rating}</span>
                      {product.rating_count && (
                        <span className="text-slate-400 text-sm">({product.rating_count.toLocaleString()})</span>
                      )}
                    </div>
                  ) : (
                    <p className="text-slate-400">—</p>
                  )}
                </div>
              ))}
            </div>

            {/* Actions Row */}
            <div className="grid grid-cols-2">
              {[product1, product2].map((product, index) => (
                <div
                  key={index}
                  className={`p-4 ${index === 0 ? "border-r border-slate-200 dark:border-slate-700" : ""}`}
                >
                  {product ? (
                    <div className="flex flex-col gap-2">
                      <Link
                        href={`/product?id=${product.product_id}`}
                        className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-center font-medium rounded-lg transition-colors"
                      >
                        View Details
                      </Link>
                      {product.product_link && (
                        <a
                          href={product.product_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="w-full py-2 bg-amber-500 hover:bg-amber-400 text-white text-center font-medium rounded-lg transition-colors"
                        >
                          View on Amazon
                        </a>
                      )}
                    </div>
                  ) : (
                    <Link
                      href="/listings"
                      className="w-full py-2 bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-center font-medium rounded-lg hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors block"
                    >
                      Add Product
                    </Link>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Clear Button */}
        {compareIds.length > 0 && !isLoading && (
          <div className="mt-6 text-center">
            <button
              onClick={clearCompare}
              className="text-slate-500 hover:text-red-500 text-sm transition-colors"
            >
              Clear comparison and start over
            </button>
          </div>
        )}

        {/* Back Link */}
        <div className="mt-8">
          <Link
            href="/listings"
            className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
            Back to products
          </Link>
        </div>
      </div>

      <Footer />
    </div>
  );
}

