'use client';

import Image from "next/image";
import { useEffect, useState } from "react";

type Product = {
  name: string;
  price: number;
  image?: string;
  category: string;
};

const CATEGORY_MAP: { [key: number]: string } = {
    1: "Aceite", 2: "Vinagre", 3: "Sal", 4: "Especias", 5: "Salsas",
    6: "Bebidas sin alcohol", 7: "Bebidas con alcohol", 8: "Aperitivos", 9: "Arroz", 10: "Legumbre",
    11: "Pasta", 12: "Dulces y pastelería", 13: "Comida preparada", 14: "Cacao, café, infusiones",
    15: "Carne", 16: "Pescado", 17: "Cereales", 18: "Galletas", 19: "Charcutería",
    20: "Quesos", 21: "Congelados", 22: "Conservas", 23: "Caldos y sopas", 24: "Cremas",
    25: "Fruta", 26: "Verduras", 27: "Ensaladas", 28: "Huevos", 29: "Lácteos",
    30: "Panadería", 31: "Pizzas", 32: "Zumos", 33: "Bicarbonato", 34: "Sazonador", 35: "Harina y masas",
    36: "Comida mexicana", 37: "Comida oriental", 38: "Otros", 39: "Azúcar, edulcorantes, otros",
    40: "Mermelada, membrillo, miel, otros"
};

function getCategoryName(id: number | string) {
  return CATEGORY_MAP[Number(id)] || "Sin categoría";
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("Todas");

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/catalog`)
      .then(res => res.json())
      .then(data => setProducts(data.products))
      .catch(err => {
        console.error("Error al obtener productos:", err);
        setProducts([]);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-8">Cargando productos...</div>;

  const categories = ["Todas", ...Array.from(new Set(products.map(p => p.category)))];

  const filteredProducts =
    selectedCategory === "Todas"
      ? products
      : products.filter(p => p.category === selectedCategory);

  return (
    <div className="max-w-5xl mx-auto px-4">
      {/* Imagen cabecera */}
      <div className="w-full flex justify-center mb-8">
        <Image
          src="/productos_supermercado.jpg"
          alt="Persona eligiendo productos en un supermercado"
          width={900}
          height={320}
          className="rounded-2xl shadow-md object-cover h-56 w-full max-w-3xl"
          priority
        />
      </div>
      <h1 className="text-3xl font-bold mb-6 text-center">Catálogo de productos</h1>

      {/* Selector de categoría */}
      <div className="flex flex-wrap gap-3 justify-center mb-8">
        {categories.map(cat => (
          <button
            key={cat}
            className={`px-4 py-2 rounded-full border 
              ${selectedCategory === cat ? 'bg-orange-100 border-orange-500 text-orange-700 font-bold' : 'bg-white border-gray-300 text-gray-700'}
              transition-colors`}
            onClick={() => setSelectedCategory(cat)}
          >
            {getCategoryName(cat)}
          </button>
        ))}
      </div>

      {/* Grid de productos */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-7">
        {filteredProducts.map((prod, i) => (
          <div
            key={i}
            className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow p-6 flex flex-col items-center"
          >
            {prod.image && (
              <img
                src={prod.image}
                alt={prod.name}
                className="w-24 h-24 object-cover mb-4 rounded-xl border"
              />
            )}
            <div className="font-semibold text-lg text-center mb-2">{prod.name}</div>
            <div className="text-orange-600 font-bold text-xl mt-auto">
              €{prod.price}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
