import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";
import ProductActions from "../components/ProductActions";
import ProductViewTracker from "./ProductViewTracker";
import Recommendations from "../components/Recommendations";
import { BackendAddress } from "../context/APIAddress";

interface PageProps {
  params: Promise<{ slug: string[] }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

async function getProduct(productId: string) {
  const res = await fetch(`${BackendAddress()}/products/${productId}`, { cache: "no-store" });
  if (!res.ok) {
    return null;
  }
  return res.json();
}

export default async function ProductPage({ params, searchParams }: PageProps) {
    const sp = await searchParams;
  const productId = Array.isArray(sp.id) ? sp.id[0] : sp.id;

  if (!productId) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col">
        <Header />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Product Not Found</h1>
            <p className="text-slate-500 dark:text-slate-400 mb-6">Please navigate from a product listing.</p>
            <Link
              href="/listings"
              className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-500 transition-colors"
            >
              ← Back to Products
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  const product = await getProduct(productId);

  if (!product) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col">
        <Header />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Product Not Found</h1>
            <p className="text-slate-500 dark:text-slate-400 mb-6">This product doesn&apos;t exist or has been removed.</p>
            <Link
              href="/listings"
              className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-500 transition-colors"
            >
              ← Back to Products
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Format the about text
  const formattedAbout = product.about_product
    ?.replaceAll(";", "\n")
    .replaceAll("|", "\n")
    .split("\n")
    .filter((line: string) => line.trim()) || [];

  // Calculate discount
  const discountPercent = product.actual_price > product.discounted_price
    ? Math.round((1 - product.discounted_price / product.actual_price) * 100)
    : 0;

  // Star rating
  const fullStars = Math.floor(product.rating);
  const hasHalfStar = product.rating % 1 >= 0.5;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col">
      <Header />

      <div className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-sm mb-6">
          <Link href="/listings" className="text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200">
            Products
          </Link>
          <span className="text-slate-400">/</span>
          <span className="text-slate-700 dark:text-slate-300 truncate max-w-xs">
            {product.product_name}
          </span>
        </nav>

        {/* Product Details */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-6 lg:p-8">
            {/* Image */}
            <div className="aspect-square bg-slate-100 dark:bg-slate-900 rounded-xl overflow-hidden flex items-center justify-center">
              {product.img_link ? (
                <img
                  src={product.img_link}
                  alt={product.product_name}
                  className="w-full h-full object-contain p-8"
                />
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="w-24 h-24 text-slate-300 dark:text-slate-600">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
              )}
            </div>

            {/* Details */}
            <div className="flex flex-col">
              {/* Categories */}
              {product.category && product.category.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {product.category.slice(0, 3).map((cat: string) => (
                    <Link
                      key={cat}
                      href={`/listings?cat=${cat}`}
                      className="px-2 py-1 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs rounded-md hover:bg-emerald-100 dark:hover:bg-emerald-900/30 hover:text-emerald-700 dark:hover:text-emerald-400 transition-colors"
                    >
                      {cat.replace(/([A-Z])/g, ' $1').trim()}
                    </Link>
                  ))}
                </div>
              )}

              {/* Title */}
              <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white mb-4">
                {product.product_name}
              </h1>

              {/* Rating */}
              <div className="flex items-center gap-3 mb-6">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <svg
                      key={i}
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill={i < fullStars ? "currentColor" : "none"}
                      stroke="currentColor"
                      className={`w-5 h-5 ${i < fullStars || (i === fullStars && hasHalfStar) ? "text-amber-400" : "text-slate-300 dark:text-slate-600"}`}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={i < fullStars ? 0 : 1.5} d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                    </svg>
                  ))}
                </div>
                <span className="text-lg font-medium text-slate-700 dark:text-slate-300">
                  {product.rating}
                </span>
                <span className="text-slate-400">•</span>
                <span className="text-slate-500 dark:text-slate-400">
                  {product.rating_count?.toLocaleString()} reviews
                </span>
              </div>

              {/* Price */}
              <div className="bg-slate-50 dark:bg-slate-900 rounded-xl p-4 mb-6">
                <div className="flex items-baseline gap-3">
                  <span className="text-3xl font-bold text-slate-900 dark:text-white">
                    ₹{product.discounted_price?.toLocaleString()}
                  </span>
                  {discountPercent > 0 && (
                    <>
                      <span className="text-lg text-slate-400 line-through">
                        ₹{product.actual_price?.toLocaleString()}
                      </span>
                      <span className="px-2 py-1 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-sm font-medium rounded-md">
                        {discountPercent}% off
                      </span>
                    </>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <ProductActions
                productId={product.product_id}
                productLink={product.product_link}
              />

              {/* About */}
              {formattedAbout.length > 0 && (
        <div>
                  <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-3">About this item</h2>
                  <ul className="space-y-2">
                    {formattedAbout.map((line: string, index: number) => (
                      <li key={index} className="flex items-start gap-2 text-slate-600 dark:text-slate-400">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                        </svg>
                        <span>{line.trim()}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Back Link */}
        <div className="mt-8">
          <Link
            href="/listings"
            className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
            Back to all products
          </Link>
        </div>

        {/* Track Product View */}
        <ProductViewTracker productId={product.product_id} />

        {/* Recommendations - Only show if user is logged in */}
        <Recommendations currentProductId={product.product_id} />
      </div>

      <Footer />
    </div>
  );
}
