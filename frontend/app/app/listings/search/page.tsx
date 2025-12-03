type Preview = {
  product_id: number | string;
  product_name: string;
  discounted_price: number;
  rating: number;
};

type SearchParams = {
  filter?: string | string[];
};

type PageProps = {
  searchParams: Promise<SearchParams>;
};

export default async function Page({ searchParams }: PageProps) {
  // unwrap searchParams
  const params = await searchParams;

  const rawFilter = params.filter;
  const filterValue =
    Array.isArray(rawFilter) ? rawFilter[0] : rawFilter ?? "";
  const filter = filterValue.trim();

  const base = "http://localhost:8000/api/v1/previews";

  // if no filter just show all previews
  if (filter === "") {
    const resAll = await fetch(`${base}/`, { cache: "no-store" });

    if (!resAll.ok) {
      return (
        <>
          <h2>Search results</h2>
          <p>Failed to load listings.</p>
        </>
      );
    }

    const previews: Preview[] = await resAll.json();

    return (
      <>
        <form
          action="/listings/search"
          style={{ marginBottom: "1rem" }}
        >
          <label>
            Search:&nbsp;
            <input
              type="text"
              name="filter"
              defaultValue={filter}
              placeholder="Search by product name..."
            />
          </label>
          <button type="submit" style={{ marginLeft: "0.5rem" }}>
            Go
          </button>
        </form>

        <h2 style={{ marginBottom: "0.5rem" }}>Search results</h2>
        <p>Filter: (none)</p>

        <div style={{ marginTop: "1rem" }}>
          {previews.map((preview) => (
            <div
              key={preview.product_id}
              style={{
                border: "1px solid #444",
                borderRadius: "8px",
                padding: "0.5rem 1rem",
                marginBottom: "0.5rem",
              }}
            >
              <h3>{preview.product_name}</h3>
              <p>Price: {preview.discounted_price}</p>
              <p>Rating: {preview.rating}</p>
            </div>
          ))}
        </div>
      </>
    );
  }

  // if there is a filter then try backend wide search first 
  const wideAddress = `${base}/search/w=${encodeURIComponent(filter)}`;
  const resWide = await fetch(wideAddress, { cache: "no-store" });

  if (!resWide.ok) {
    return (
      <>
        <h2>Search results</h2>
        <p>Failed to load listings.</p>
      </>
    );
  }

  const wideResults: Preview[] = await resWide.json();

  let previews: Preview[] = wideResults;
  let fallbackMessage: string | null = null;

  // if backend wide search found nothing, fall back to client-side search
  if (wideResults.length === 0) {
    const resAll = await fetch(`${base}/`, { cache: "no-store" });

    if (resAll.ok) {
      const allPreviews: Preview[] = await resAll.json();
      const lower = filter.toLowerCase();

      previews = allPreviews.filter((p) =>
        p.product_name.toLowerCase().includes(lower)
      );

      if (previews.length > 0) {
        fallbackMessage =
          'No exact matches found; showing close matches instead.';
      }
    }
  }

  return (
    <>
      {/* Search form */}
      <form
        action="/listings/search"
        style={{ marginBottom: "1rem" }}
      >
        <label>
          Search:&nbsp;
          <input
            type="text"
            name="filter"
            defaultValue={filter}
            placeholder="Search by product name..."
          />
        </label>
        <button type="submit" style={{ marginLeft: "0.5rem" }}> 
          Go 
        </button>
      </form>

      <h2 style={{ marginBottom: "0.5rem" }}>Search results</h2>
      <p>Filter: {filter}</p>

      <div style={{ marginTop: "1rem" }}>
        {fallbackMessage && <p>{fallbackMessage}</p>}

        {previews.length === 0 && !fallbackMessage && (
          <p>No listings found.</p>
        )}

        {previews.map((preview) => (
          <div
            key={preview.product_id}
            style={{
              border: "1px solid #444",
              borderRadius: "8px",
              padding: "0.5rem 1rem",
              marginBottom: "0.5rem",
            }}
          >
            <h3>{preview.product_name}</h3>
            <p>Price: {preview.discounted_price}</p>
            <p>Rating: {preview.rating}</p>
          </div>
        ))}
      </div>
    </>
  );
}
