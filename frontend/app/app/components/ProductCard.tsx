"use client";

import Link from "next/link";
import Image from "next/image";
import CompareButton from "./CompareButton";

interface ProductCardProps {
  product_id: string;
  product_name: string;
  discounted_price: number;
  rating: number;
  img_link?: string;
  actual_price?: number;
}

export default function ProductCard({
  product_id,
  product_name,
  discounted_price,
  rating,
  img_link,
  actual_price,
}: ProductCardProps) {
  // Calculate discount percentage if actual price is available
  const discountPercent = actual_price 
    ? Math.round((1 - discounted_price / actual_price) * 100)
    : null;

  // Generate star rating display
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;

  return (
    <Link href={`/product?id=${product_id}`} className="group">
      <div className="bg-white dark:bg-slate-800 rounded-xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-200 dark:border-slate-700 hover:border-emerald-500/50 dark:hover:border-emerald-500/50 hover:-translate-y-1">
        {/* Image Container */}
        <div className="relative aspect-square bg-slate-100 dark:bg-slate-900 overflow-hidden">
          {img_link ? (
            <img
              src={img_link}
              alt={product_name}
              className="w-full h-full object-contain p-4 group-hover:scale-105 transition-transform duration-300"
              onError={(e) => {
                // Fallback for broken images
                (e.target as HTMLImageElement).src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='1' d='M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'/%3E%3C/svg%3E";
              }}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="w-16 h-16 text-slate-300 dark:text-slate-600">
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
            </div>
          )}
          
          {/* Discount Badge */}
          {discountPercent && discountPercent > 0 && (
            <div className="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-md">
              -{discountPercent}%
            </div>
          )}

          {/* Compare Button */}
          <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <CompareButton productId={product_id} variant="icon" />
          </div>
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Product Name */}
          <h3 className="text-sm font-medium text-slate-800 dark:text-slate-200 line-clamp-2 min-h-[2.5rem] group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
            {product_name}
          </h3>

          {/* Rating */}
          <div className="flex items-center gap-1 mt-2">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <svg
                  key={i}
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill={i < fullStars ? "currentColor" : (i === fullStars && hasHalfStar ? "url(#half)" : "none")}
                  stroke="currentColor"
                  className={`w-4 h-4 ${i < fullStars || (i === fullStars && hasHalfStar) ? "text-amber-400" : "text-slate-300 dark:text-slate-600"}`}
                >
                  <defs>
                    <linearGradient id="half">
                      <stop offset="50%" stopColor="currentColor" />
                      <stop offset="50%" stopColor="transparent" />
                    </linearGradient>
                  </defs>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={i < fullStars ? 0 : 1.5} d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                </svg>
              ))}
            </div>
            <span className="text-xs text-slate-500 dark:text-slate-400 ml-1">
              {rating.toFixed(1)}
            </span>
          </div>

          {/* Price */}
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-lg font-bold text-slate-900 dark:text-white">
              ₹{discounted_price.toLocaleString()}
            </span>
            {actual_price && actual_price > discounted_price && (
              <span className="text-sm text-slate-400 line-through">
                ₹{actual_price.toLocaleString()}
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}

