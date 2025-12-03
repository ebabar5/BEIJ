import ListingsClient from './ListingsClient';

// Helper function to build filter string from individual parameters (for backward compatibility)
function buildFilter(category: string | undefined, max: number | undefined, min: number | undefined): string {
  let previous: boolean = false;
  let filter: string = '';
  if (category && category !== 'undefined') {
    filter = filter.concat(category);
    previous = true;
  }
  if (max !== undefined && max !== null && !isNaN(Number(max))) {
    if (previous) filter = filter.concat("&");
    filter = filter.concat("max=", String(max));
    previous = true;
  }
  if (min !== undefined && min !== null && !isNaN(Number(min))) {
    if (previous) filter = filter.concat("&");
    filter = filter.concat("min=", String(min));
  }
  return filter;
}

async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string[] }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { slug } = await params;
  const sp = await searchParams;

  // Support both new format (filter, search, sort_by) and old format (cat, max, min) for backward compatibility
  const filter = (sp.filter as string | undefined) || 
    (sp.cat || sp.max || sp.min ? buildFilter(
      sp.cat as string | undefined,
      sp.max ? Number(sp.max) : undefined,
      sp.min ? Number(sp.min) : undefined
    ) : undefined);
  
  const search = sp.search as string | undefined;
  const sort_by = sp.sort_by as string | undefined;

  // Build API URL based on parameters
  let address = 'http://localhost:8000/api/v1/previews/';
  
  if (search) {
    // If search exists, combine with filter if present
    // Backend format: /search/keyword&filter_string
    // The filter string already contains & and =, so we combine first then encode
    if (filter) {
      const combined = `${search}&${filter}`;
      address = `http://localhost:8000/api/v1/previews/search/${encodeURIComponent(combined)}`;
    } else {
      address = `http://localhost:8000/api/v1/previews/search/${encodeURIComponent(search)}`;
    }
  } else if (filter) {
    // If filter exists, use filter endpoint
    address = `http://localhost:8000/api/v1/previews/${encodeURIComponent(filter)}`;
  }

  try {
    const res = await fetch(address, {
      cache: "no-store",
    });
    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }
    const previews = await res.json();
    return <ListingsClient initialPreviews={previews} sortBy={sort_by} />;
  } catch (error) {
    console.error('Error fetching previews:', error);
    return (
      <div>
        <h1>Error loading listings</h1>
        <p>Failed to fetch product previews. Please try again later.</p>
      </div>
    );
  }
}

export default Page;
