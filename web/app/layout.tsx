import type { Metadata } from 'next'

import "./globals.css";
import Link from "next/link";
import { Analytics } from "@vercel/analytics/next"
import { SpeedInsights } from "@vercel/speed-insights/next"

export const metadata = {
  title: "Dispensia - Frutería",
  description: "Catálogo de productos y aplicación de listas de la compra",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="bg-[#fafafa] min-h-screen flex flex-col">
        {/* NAVBAR */}
        <header className="shadow bg-white rounded-t-2xl">
          <nav className="max-w-6xl mx-auto flex flex-col sm:flex-row justify-between items-center px-6 py-4">
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-2xl text-orange-500 flex items-center">
                <span className="mr-2">
                  <span className="text-3xl">🛒</span>
                </span>
                DISPENSIA
              </span>
            </div>
            <div className="flex gap-6 items-center mt-4 sm:mt-0">
              <Link href="/" className="text-gray-800 font-medium hover:text-orange-500 transition">Inicio</Link>
              <Link href="/products" className="text-gray-800 font-medium hover:text-orange-500 transition">Catálogo de productos</Link>
              <Link href="/shopping-list" className="text-gray-800 font-medium hover:text-orange-500 transition">Lista de la compra</Link>
            </div>
          </nav>
        </header>
        <main className="flex-grow flex justify-center items-start">{children} <Analytics /> <SpeedInsights /></main>
        <footer className="bg-gray-100 text-center text-gray-600 p-4 rounded-b-2xl border-t mt-8">
          <p>
            © {new Date().getFullYear()} Dispensia. Todos los derechos reservados.
          </p>
        </footer>
      </body>
    </html>
  );
}
