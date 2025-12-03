export default function Loading() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header Skeleton */}
      <header className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="w-16 h-8 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
            <div className="flex gap-4">
              <div className="w-20 h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
              <div className="w-20 h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title Skeleton */}
        <div className="mb-6">
          <div className="w-32 h-8 bg-slate-200 dark:bg-slate-700 rounded animate-pulse mb-2" />
          <div className="w-24 h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
        </div>

        <div className="flex gap-8">
          {/* Sidebar Skeleton */}
          <aside className="hidden lg:block w-72 space-y-4">
            <div className="w-full h-8 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
            <div className="space-y-2">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="w-full h-6 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
              ))}
            </div>
          </aside>

          {/* Product Grid Skeleton */}
          <main className="flex-1">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {[...Array(12)].map((_, i) => (
                <div
                  key={i}
                  className="bg-white dark:bg-slate-800 rounded-xl overflow-hidden border border-slate-200 dark:border-slate-700"
                >
                  <div className="aspect-square bg-slate-200 dark:bg-slate-700 animate-pulse" />
                  <div className="p-4 space-y-3">
                    <div className="w-full h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
                    <div className="w-2/3 h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
                    <div className="w-20 h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
                    <div className="w-24 h-6 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
                  </div>
                </div>
              ))}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
