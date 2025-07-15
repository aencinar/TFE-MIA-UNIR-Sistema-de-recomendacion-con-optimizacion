import ProductGrid from "@/components/ProductGrid";
import { useProducts } from "./hooks/useProducts";

export default async function Home() {
  const products = await useProducts();

  return (
    <div>
      <main className="container mx-auto px-4 mt-8 min-h-screen flex flex-col items-center gap-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Listado de Productos
        </h1>
        <ProductGrid products={products} />
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
      </footer>
    </div>
  );
}
