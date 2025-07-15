import { useEffect, useState } from "react";
import { Product, Category } from "@/types";

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

export function useProductCatalog(selectedCategories: number[], selectedRestrictions: string[], page: number) {
  const [catalog, setCatalog] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    setLoading(true);

    const params = new URLSearchParams();
    selectedCategories.forEach(cat => params.append("categories", String(cat)));
    selectedRestrictions.forEach(r => params.append("restrictions", r));
    params.append("page", String(page || 1));

    fetch(`${apiUrl}/api/catalog?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        setCatalog(data.products.map((p: any) => ({
          ...p,
          id: p.id ?? p.product_code ?? p._id ?? Math.random(),
          categoryId: p.category
        })));
      })
      .finally(() => setLoading(false));

    setCategories(
      Object.entries(CATEGORY_MAP).map(([id, name]) => ({
        id: Number(id),
        name
      }))
    );
  }, [selectedCategories, selectedRestrictions, page]);

  return { catalog, categories, loading };
}
