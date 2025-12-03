type Preview = {
  product_id: number | string;
  product_name: string;
  discounted_price: number;
  rating: number;
};

export default async function Page() {
  const address = "http://localhost:8000/api/v1/previews/";
  const res = await fetch(address, {
    cache: "no-store",
  });

  if (!res.ok) {
    return (
      <div>
        <h1>Listing previews</h1>
        <p>Failed to load previews from {address}</p>
      </div>
    );
  }

  const previews: Preview[] = await res.json();
  return (
    <>
      <h1>Listing previews</h1>
      <div>
        {previews.map((preview) => (
          <div key={preview.product_id}>
            <h2>{preview.product_name}</h2>
            <h3>Price: {preview.discounted_price}</h3>
            <h3>Rating: {preview.rating}</h3>
          </div>
        ))}
      </div>
    </>
  );
}
