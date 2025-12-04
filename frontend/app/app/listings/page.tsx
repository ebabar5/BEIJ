import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";
import ProductCard from "../components/ProductCard";
import FilterSidebar from "../components/FilterSidebar";
import SortDropdown from "../components/SortDropdown";
import { BackendAddress } from "../context/APIAddress";

// Fetch all products with full data (includes images)
async function getProducts(sortBy?: string) {
  const url = sortBy 
    ? `${BackendAddress()}/products/?sort_by=${sortBy}`
    : `${BackendAddress()}/products/`;
  
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    throw new Error("Failed to fetch products");
  }
  return res.json();
}

// Get unique categories from products
function extractCategories(products: any[]): string[] {
  const categorySet = new Set<string>();
  products.forEach(p => {
    if (p.category && Array.isArray(p.category)) {
      p.category.forEach((cat: string) => categorySet.add(cat));
    }
  });
  return Array.from(categorySet).sort();
}

// Filter products based on criteria
function filterProducts(
  products: any[],
  category?: string,
  minPrice?: number,
  maxPrice?: number,
  searchQuery?: string
) {
  return products.filter(p => {
    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      const nameMatch = p.product_name?.toLowerCase().includes(query);
      const categoryMatch = p.category?.some((c: string) => c.toLowerCase().includes(query));
      if (!nameMatch && !categoryMatch) {
        return false;
      }
    }
    
    // Category filter
    if (category && category !== "all") {
      if (!p.category || !p.category.includes(category)) {
        return false;
      }
    }
    
    // Price filters
    if (minPrice && p.discounted_price < minPrice) {
      return false;
    }
    if (maxPrice && p.discounted_price > maxPrice) {
      return false;
    }
    
    return true;
  });
}

interface PageProps {
  params: Promise<{ slug: string[] }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export default async function ListingsPage({ params, searchParams }: PageProps) {
  const sp = await searchParams;
  
  // Parse search params
  const category = Array.isArray(sp.cat) ? sp.cat[0] : sp.cat;
  const minPrice = sp.min ? Number(Array.isArray(sp.min) ? sp.min[0] : sp.min) : undefined;
  const maxPrice = sp.max ? Number(Array.isArray(sp.max) ? sp.max[0] : sp.max) : undefined;
  const sortBy = Array.isArray(sp.sort) ? sp.sort[0] : (Array.isArray(sp.sort_by) ? sp.sort_by[0] : sp.sort_by) || sp.sort;
  const searchQuery = Array.isArray(sp.search) ? sp.search[0] : sp.search;

  // Fetch products
  let products = [];
  let error = null;
  
  try {
    products = await getProducts(sortBy);
  } catch (e) {
    error = "Failed to load products. Please make sure the backend is running.";
  }

  // Extract categories for filter sidebar
  const categories = extractCategories(products);

  // Apply filters
  const filteredProducts = filterProducts(products, category, minPrice, maxPrice, searchQuery);

  // Count for display
  const totalCount = products.length;
  const filteredCount = filteredProducts.length;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col">
      <Header />

      <div className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {/* Page Title & Controls */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              {searchQuery ? `Search: "${searchQuery}"` : "Products"}
            </h1>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
              {filteredCount === totalCount 
                ? `${totalCount} products`
                : `${filteredCount} of ${totalCount} products`
              }
              {category && ` in ${category.replace(/([A-Z])/g, ' $1').trim()}`}
            </p>
          </div>
          
          <div className="flex items-center gap-3">
            <SortDropdown currentSort={sortBy} />
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
            <p className="text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Main Content */}
        <div className="flex gap-8">
          {/* Sidebar */}
          <FilterSidebar
            categories={categories}
            currentCategory={category}
            currentMin={minPrice}
            currentMax={maxPrice}
          />

          {/* Product Grid */}
          <main className="flex-1">
            {filteredProducts.length === 0 ? (
              <div className="text-center py-12">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="w-16 h-16 mx-auto text-slate-300 dark:text-slate-600 mb-4">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5m6 4.125l2.25 2.25m0 0l2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
                </svg>
                <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">No products found</h3>
                <p className="text-slate-500 dark:text-slate-400 mb-4">
                  {searchQuery ? "Try a different search term" : "Try adjusting your filters"}
                </p>
                <Link
                  href="/listings"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-500 transition-colors"
                >
                  {searchQuery ? "View all products" : "Clear filters"}
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredProducts.map((product: any, index: number) => (
                  <ProductCard
                    key={`${product.product_id}-${index}`}
                    product_id={product.product_id}
                    product_name={product.product_name}
                    discounted_price={product.discounted_price}
                    actual_price={product.actual_price}
                    rating={product.rating}
                    img_link={product.img_link}
                  />
                ))}
              </div>
            )}
          </main>
        </div>
      </div>

      <Footer />
    </div>
  );
}
