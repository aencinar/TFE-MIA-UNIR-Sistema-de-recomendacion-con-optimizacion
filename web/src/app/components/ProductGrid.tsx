import React from "react";
import { Product } from "@/domain/entities/Product";

interface Props {
  products: Product[] | undefined;
}

interface ProductGridProps {
  products: Product[] | undefined;
}

const ProductGrid: React.FC<ProductGridProps> = ({ products }: Props) => {
  return (
    <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4">
      {products && products.map((product) => (
        <div
          key={product.id}
          className="bg-white rounded-lg shadow p-4 flex flex-col"
        >
          <img
            src={product.imageUrl}
            alt={product.name}
            className="rounded mb-4 mx-auto"
          />
          <h3 className="text-lg font-semibold mb-2 text-gray-800">
            {product.name}
          </h3>
          <p className="text-gray-600 mb-2">{product.description}</p>
          <div className="mt-auto">
            <p className="text-green-600 font-bold text-lg mb-2">
              Mínimo: {product.price.toFixed(2)} €
            </p>
            <button className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
              Ver Detalles
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProductGrid;
