"use client";

import SaveButton from "./SaveButton";
import CompareButton from "./CompareButton";

interface ProductActionsProps {
  productId: string;
  productLink: string;
}

export default function ProductActions({ productId, productLink }: ProductActionsProps) {
  return (
    <div className="flex flex-col sm:flex-row gap-3 mb-6">
      <a
        href={productLink}
        target="_blank"
        rel="noopener noreferrer"
        className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-amber-500 hover:bg-amber-400 text-white font-medium rounded-lg transition-colors"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
        </svg>
        View on Amazon
      </a>
      <SaveButton
        productId={productId}
        className="flex-1 px-6 py-3 font-medium rounded-lg"
      />
      <CompareButton
        productId={productId}
        className="flex-1"
      />
    </div>
  );
}

