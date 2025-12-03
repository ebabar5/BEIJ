let base_address = 'http://localhost:8000/api/v1/previews/';

function buildFilter(category: string | undefined, max: number | undefined, min: number | undefined): string {
  //build the filter string
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

async function Page({params, searchParams,}: {
params: Promise < {slug: string[]} > ;
searchParams: Promise < {[key: string]: string | string[] | undefined } > ;})
{
  
  const {slug} = await params;
  const sp = await searchParams;//Use url parameter to build the filter
  //testing
  const category: string | undefined = Array.isArray(sp.cat) ? sp.cat[0] : sp.cat;
  const max: number | undefined = sp.max ? Number(Array.isArray(sp.max) ? sp.max[0] : sp.max) : undefined;
  const min: number | undefined = sp.min ? Number(Array.isArray(sp.min) ? sp.min[0] : sp.min) : undefined;
  //console.log("cat: %s\nMax: %f, Min: %f",category,max,min)

  let filter: string = buildFilter(category, max, min);
  let address = base_address.concat(filter);
  const res = await fetch(address);
  const previews = await res.json();


  return (<><h1>Listing previews</h1>
  <p>Server Address: {base_address}</p><p>Filter: {filter}</p>
      <div>{previews.map((preview: any) => {
    return (
      <div key={preview.product_id}>
      <h2>{preview.product_name}</h2>
      <h3>Price: {preview.discounted_price}</h3>
      <h3>Rating: {preview.rating}</h3>
      </div>

    )
  })}</div>
  </>)
}


export default Page;