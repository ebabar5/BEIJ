let base_address = 'http://localhost:8000/api/v1/previews/';

function buildFilter(category:string,max:number,min:number){
  //build the filter string
  let previous : boolean = false;
  let filter : string = '';
  if(category!='undefined'){
    filter=filter.concat(category);
    previous = true;
  }
  if(max!=NaN && max!=undefined){
    if(previous)filter=filter.concat("&");
    filter=filter.concat("max=",max);
  }
  if(min!=NaN && min!=undefined){
    if(previous)filter=filter.concat("&");
    filter=filter.concat("min=",min);
  }
  return(filter);
}

async function Page({params, searchParams,}: {
params: Promise < {slug: string[]} > ;
searchParams: Promise < {[key: string]: string | string[] | undefined } > ;})
{
  
  const {slug} = await params;
  const sp = await searchParams;//Use url parameter to build the filter
  //testing
  const category : string = sp.cat;
  const max : number = sp.max;
  const min : number = sp.min;
  //console.log("cat: %s\nMax: %f, Min: %f",category,max,min)

  let filter:string = buildFilter(category,max,min);
  let address = base_address.concat(filter);
  const res = await fetch(address);
  const previews = await res.json();


  return (<><h1>Listing previews</h1>
  <p>Server Address: {base_address}</p><p>Filter: {filter}</p>
  <div>{previews.map((preview) => {
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