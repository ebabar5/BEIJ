import Link from "next/link";
import { format } from "path";

const base_address = "http://localhost:8000/api/v1/products/";

async function Page({params, searchParams,}: {
params: Promise < {slug: string[]} > ;
searchParams: Promise < {[key: string]: string | string[] | undefined } > ;}){
    const {slug} = await params;
    const sp = await searchParams;
    console.log(sp);
    if(Object.keys(sp).length==0)return(<><p>Please ensure you are navigating to a listing</p></>);
    else{
        const res = await fetch(base_address.concat(sp.id));
        const product = await res.json();
        
        let formatted_about:string = product.about_product;
        formatted_about = formatted_about.replaceAll(";","\n").replaceAll("|","\n");

        return(<>
        <div>
            <Link href="/listings">← Back to Listings</Link>
            <p>{product.product_name}</p>
            <p>Full Price: {product.actual_price}</p>
            <p>Discounted Price: {product.discounted_price}</p>
            <p>Current Price on Amazon: TODO</p>
            <p>Rated: {product.rating} from {product.rating_count}</p>
            <p></p>
            <p>About:</p>
            <p style={{"whiteSpace": "pre-wrap"}}>{formatted_about}</p>

            <Link href={product.product_link}>View on Amazon</Link>
        </div>
        </>)
    }
}

export default Page;