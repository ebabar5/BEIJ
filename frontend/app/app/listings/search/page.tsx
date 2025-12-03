import { redirect } from 'next/navigation';

export default function Page({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  // Redirect search page to main listings page with search parameter
  // This ensures search is handled consistently on the listings page
  const search = searchParams.q || searchParams.search;
  const params = new URLSearchParams();
  if (search) {
    params.set('search', Array.isArray(search) ? search[0] : search);
  }
  
  redirect(`/listings${params.toString() ? `?${params.toString()}` : ''}`);
}