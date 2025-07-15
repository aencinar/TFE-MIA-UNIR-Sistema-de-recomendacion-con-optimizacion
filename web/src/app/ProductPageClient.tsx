"use client";

import { useQuery } from "@tanstack/react-query";
import { Product } from "@/domain/entities/Product";

type Props = {
  initialData: Product[];
};

export default function ProductPageClient({ initialData }: Props) {
  const { data, isLoading } = useQuery<Product[]>({
    queryKey: ["products"],
    queryFn: async () => initialData, // opcional: puedes hacer refetch si quieres
    initialData,
  });

  return (
    <div>
      <h1>Productos</h1>
      {isLoading && <p>Cargando...</p>}
      <ul>
        {data.map((product) => (
          <li key={product.id}>
            {product.name} - ${product.price}
          </li>
        ))}
      </ul>
    </div>
  );
}
