import ListingsClient from './ListingsClient';

async function Page({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  // Read URL parameters
  const filter = searchParams.filter as string | undefined;
  const search = searchParams.search as string | undefined;
  const sort_by = searchParams.sort_by as string | undefined;

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
    const res = await fetch(address);
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