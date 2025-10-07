import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Longevity Planning - Retirement Planning Tool",
  description: "DIY retirement planning with Monte Carlo simulations. Optimize your portfolio allocation and withdrawal strategy to maximize your odds of not running out of money.",
  keywords: ["retirement planning", "Monte Carlo simulation", "portfolio optimization", "withdrawal strategy", "financial planning"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:p-4 focus:bg-blue-600 focus:text-white focus:rounded-md"
        >
          Skip to main content
        </a>
        <main id="main-content" className="w-full">
          {children}
        </main>
      </body>
    </html>
  );
}
