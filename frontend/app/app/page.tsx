import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div>
      <div className="justify-center">
          <h1>Title bar</h1>
          <p>
            <Link href="/listings">Listings</Link> |
            {" "}<Link href="/users">Users</Link> |
            {" "}<a>Search</a>
          </p>
        </div>
      <main className="flex bg-white dark:bg-black sm:items-start">
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <a
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >Documentation
          </a>
        </div>
        <div>
          
        </div>
      </main>
    </div>
  );
}
