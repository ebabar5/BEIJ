"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../context/AuthContext";

export default function LogoutPage() {
  const router = useRouter();
  const { isAuthenticated, logout, user } = useAuth();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [loggedOut, setLoggedOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    await logout();
    setLoggedOut(true);
    
    // Redirect to home after a brief moment
    setTimeout(() => {
      router.push("/");
    }, 2000);
  };

  // If not authenticated and not just logged out, redirect to login
  useEffect(() => {
    if (!isAuthenticated && !loggedOut && !isLoggingOut) {
      // Small delay to let auth state load
      const timer = setTimeout(() => {
        if (!isAuthenticated) {
          router.push("/users/login");
        }
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [isAuthenticated, loggedOut, isLoggingOut, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 px-4">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-orange-500/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-slate-500/10 rounded-full blur-3xl" />
      </div>

      <div className="relative w-full max-w-md">
        {/* Logo / Brand */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h1 className="text-4xl font-bold text-white tracking-tight">
              BEIJ
            </h1>
            <p className="text-slate-400 text-sm mt-1">E-Commerce Platform</p>
          </Link>
        </div>

        {/* Logout Card */}
        <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8 shadow-2xl text-center">
          {loggedOut ? (
            // Success state
            <>
              <div className="w-16 h-16 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-8 h-8 text-emerald-400">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
              </div>
              <h2 className="text-2xl font-semibold text-white mb-2">Logged out</h2>
              <p className="text-slate-400 mb-6">You have been successfully logged out.</p>
              <p className="text-slate-500 text-sm">Redirecting to home page...</p>
            </>
          ) : isLoggingOut ? (
            // Loading state
            <>
              <div className="w-16 h-16 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="animate-spin h-8 w-8 text-slate-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <h2 className="text-2xl font-semibold text-white mb-2">Logging out...</h2>
              <p className="text-slate-400">Please wait</p>
            </>
          ) : (
            // Confirmation state
            <>
              <div className="w-16 h-16 bg-orange-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 text-orange-400">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                </svg>
              </div>
              
              {user && (
                <div className="mb-6">
                  <p className="text-slate-400">Logged in as</p>
                  <p className="text-white font-medium text-lg">{user.username}</p>
                  <p className="text-slate-500 text-sm">{user.email}</p>
                </div>
              )}
              
              <h2 className="text-2xl font-semibold text-white mb-2">Ready to leave?</h2>
              <p className="text-slate-400 mb-6">Are you sure you want to log out of your account?</p>

              <div className="space-y-3">
                <button
                  onClick={handleLogout}
                  className="w-full py-3 px-4 bg-orange-600 hover:bg-orange-500 text-white font-medium rounded-lg transition-all duration-200"
                >
                  Yes, log me out
                </button>
                <Link
                  href="/"
                  className="block w-full py-3 px-4 bg-slate-700/50 hover:bg-slate-700 text-white font-medium rounded-lg transition-all duration-200"
                >
                  Cancel
                </Link>
              </div>
            </>
          )}
        </div>

        {/* Back to home */}
        {!loggedOut && !isLoggingOut && (
          <p className="text-center mt-6">
            <Link href="/" className="text-slate-500 hover:text-slate-400 text-sm transition-colors">
              ← Back to home
            </Link>
          </p>
        )}
      </div>
    </div>
  );
}
