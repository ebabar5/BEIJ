import Head from "next/head";

async function Page({filter}){

    let address = 'http://localhost:8000/api/v1/previews/'
    const res = await fetch(address);
    const previews = await res.json();
    
    console.log(filter)
    return (<><h1>Listing previews</h1>
    <p>Server Address: {address}</p><p>Filter: {filter}</p>
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

Page.getInitialProps = async ({ fil }) => {

    // Access query parameters from query object
    const {filter} = fil;
    
    // Fetch data based on query parameters
    // Return data as props
    return {filter};
};
export default Page;