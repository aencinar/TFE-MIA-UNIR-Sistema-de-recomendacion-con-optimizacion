// types.ts

export type Product = {
  id: number;
  name: string;
  categoryId: number;
  subcategory: string;
  price: number;
  product_code: string;
};

export type UserListItem = Product & { quantity: number };
export type Category = { id: number; name: string };

export const RESTRICTIONS = [
  { id: "lactose", label: "Sin lactosa" },
  { id: "gluten", label: "Celiaco" },
  { id: "soja", label: "Sin soja" },
  { id: "vegan", label: "Vegano" }
];

export const CATEGORY_MAP: { [key: number]: string } = {
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

export function getCategoryName(id: number | string) {
  return CATEGORY_MAP[Number(id)] || "Sin categoría";
}
export function getRestrictionName(id: string) {
  const found = RESTRICTIONS.find(r => r.id === id);
  return found ? found.label : "estandar";
}
