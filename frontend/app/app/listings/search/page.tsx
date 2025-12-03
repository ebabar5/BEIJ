import { redirect } from 'next/navigation';

export default function Page({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  // Redirect search page to main listings page
  // This ensures users can navigate to listings from search
  const sp = await searchParams;
  const search = sp.q || sp.search;
  
  const params = new URLSearchParams();
  if (search) {
    params.set('search', Array.isArray(search) ? search[0] : search);
  }
  
  redirect(`/listings${params.toString() ? `?${params.toString()}` : ''}`);
}