import type { ReactNode } from "react";

export default function SearchLayout({ children }: { children: ReactNode }) {
  return (
    <section
      style={{
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        gap: "1rem", 
      }}
    >
      {children}
    </section>
  );
}