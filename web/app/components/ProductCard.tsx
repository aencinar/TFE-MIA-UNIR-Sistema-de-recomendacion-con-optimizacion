import { Product } from "@/types";

type Props = {
  product: Product;
  onAdd: (product: Product) => void;
};

export default function ProductCard({ product, onAdd }: Props) {
  return (
    <div className="bg-white rounded-2xl shadow-md hover:shadow-lg p-5 flex flex-col justify-between">
      <span className="font-semibold text-lg mb-2">{product.name}</span>
      <span className="text-xs text-gray-500 mb-2">{product.category}</span>
      <div className="flex gap-2 flex-wrap mb-4">
        <span className="bg-orange-100 text-orange-700 text-xs px-2 py-0.5 rounded">{product.subcategory}</span>
      </div>
      <span className="font-bold mb-2 text-orange-700">
        €{product.price?.toFixed(2) ?? "-"}
      </span>
      <button
        className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded font-bold mt-auto"
        onClick={() => onAdd(product)}
      >Añadir a mi lista</button>
    </div>
  );
}
