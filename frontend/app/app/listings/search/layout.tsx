import type { ReactNode } from "react";

export default function SearchLayout({ children }: { children: ReactNode }) {
  return (
    <section style={{ padding: "1rem" }}>
      <h1>Search Listings</h1>
      {children}
    </section>
  );
}
