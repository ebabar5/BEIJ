'use client';

import { useSearchParams, useRouter } from 'next/navigation';
import { useState, useMemo } from 'react';

interface ListingsClientProps {
  initialPreviews: any[];
  sortBy?: string;
}

export default function ListingsClient({ initialPreviews, sortBy }: ListingsClientProps) {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  // Parse filter from URL (format: "category&min=10&max=100")
  const currentFilterString = searchParams.get('filter') || '';
  const parseFilter = (filterStr: string) => {
    if (!filterStr) return { category: '', minPrice: '', maxPrice: '' };
    const parts = filterStr.split('&');
    const category = parts[0] || '';
    let minPrice = '';
    let maxPrice = '';
    for (const part of parts.slice(1)) {
      if (part.startsWith('min=')) minPrice = part.substring(4);
      if (part.startsWith('max=')) maxPrice = part.substring(4);
    }
    return { category, minPrice, maxPrice };
  };

  const { category: currentCategory, minPrice: currentMinPrice, maxPrice: currentMaxPrice } = parseFilter(currentFilterString);
  
  // Get current values from URL
  const currentSearch = searchParams.get('search') || '';
  const currentSort = searchParams.get('sort_by') || '';

  const [search, setSearch] = useState(currentSearch);
  const [category, setCategory] = useState(currentCategory);
  const [minPrice, setMinPrice] = useState(currentMinPrice);
  const [maxPrice, setMaxPrice] = useState(currentMaxPrice);
  const [sort, setSort] = useState(currentSort);

  // Build filter string in backend format: "category&min=X&max=Y"
  const buildFilterString = (cat: string, min: string, max: string) => {
    const parts: string[] = [];
    if (cat) parts.push(cat);
    if (min) parts.push(`min=${min}`);
    if (max) parts.push(`max=${max}`);
    return parts.join('&');
  };

  // Update URL when search/filter/sort changes
  const updateURL = (newSearch: string, newCategory: string, newMinPrice: string, newMaxPrice: string, newSort: string) => {
    const params = new URLSearchParams();
    if (newSearch) params.set('search', newSearch);
    const filterStr = buildFilterString(newCategory, newMinPrice, newMaxPrice);
    if (filterStr) params.set('filter', filterStr);
    if (newSort) params.set('sort_by', newSort);
    
    const queryString = params.toString();
    router.replace(`/listings${queryString ? `?${queryString}` : ''}`);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateURL(search, category, minPrice, maxPrice, sort);
  };

  const handleCategoryChange = (newCategory: string) => {
    setCategory(newCategory);
    updateURL(search, newCategory, minPrice, maxPrice, sort);
  };

  const handlePriceChange = (type: 'min' | 'max', value: string) => {
    if (type === 'min') {
      setMinPrice(value);
      updateURL(search, category, value, maxPrice, sort);
    } else {
      setMaxPrice(value);
      updateURL(search, category, minPrice, value, sort);
    }
  };

  const handleSortChange = (newSort: string) => {
    setSort(newSort);
    updateURL(search, category, minPrice, maxPrice, newSort);
  };

  // Apply client-side sorting
  const sortedPreviews = useMemo(() => {
    if (!sort && !sortBy) return initialPreviews;
    const sortValue = sort || sortBy || '';
    const sorted = [...initialPreviews];
    
    switch (sortValue) {
      case 'name':
        sorted.sort((a, b) => a.product_name.localeCompare(b.product_name));
        break;
      case 'price_asc':
        sorted.sort((a, b) => a.discounted_price - b.discounted_price);
        break;
      case 'price_desc':
        sorted.sort((a, b) => b.discounted_price - a.discounted_price);
        break;
      case 'rating_desc':
        sorted.sort((a, b) => {
          const ratingA = a.rating || 0;
          const ratingB = b.rating || 0;
          if (ratingB !== ratingA) return ratingB - ratingA;
          return (b.rating_count || 0) - (a.rating_count || 0);
        });
        break;
      default:
        return initialPreviews;
    }
    return sorted;
  }, [initialPreviews, sort, sortBy]);

  return (
    <div>
      <h1>Listing previews</h1>
      
      {/* Search Input */}
      <form onSubmit={handleSearchSubmit}>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search products..."
        />
        <button type="submit">Search</button>
      </form>

      {/* Filter Controls */}
      <div>
        <label>
          Category:
          <select value={category} onChange={(e) => handleCategoryChange(e.target.value)}>
            <option value="">All Categories</option>
            <option value="Electronics">Electronics</option>
            <option value="Clothing">Clothing</option>
            <option value="Home">Home</option>
            <option value="Sports">Sports</option>
            {/* Add more categories as needed */}
          </select>
        </label>
        
        <label>
          Min Price:
          <input
            type="number"
            value={minPrice}
            onChange={(e) => handlePriceChange('min', e.target.value)}
            placeholder="0"
            min="0"
          />
        </label>
        
        <label>
          Max Price:
          <input
            type="number"
            value={maxPrice}
            onChange={(e) => handlePriceChange('max', e.target.value)}
            placeholder="No max"
            min="0"
          />
        </label>
      </div>

      {/* Sort Dropdown */}
      <select value={sort} onChange={(e) => handleSortChange(e.target.value)}>
        <option value="">Default</option>
        <option value="name">Name</option>
        <option value="price_asc">Price: Low to High</option>
        <option value="price_desc">Price: High to Low</option>
        <option value="rating_desc">Rating: High to Low</option>
      </select>

      {/* Display Results */}
      <div>
        {sortedPreviews.map((preview: any) => (
          <div key={preview.product_id}>
            <h2>{preview.product_name}</h2>
            <h3>Price: ${preview.discounted_price}</h3>
            <h3>Rating: {preview.rating || 'N/A'}</h3>
          </div>
        ))}
      </div>
    </div>
  );
}