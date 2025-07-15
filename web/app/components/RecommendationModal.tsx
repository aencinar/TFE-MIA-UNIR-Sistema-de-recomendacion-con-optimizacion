import { UserListItem } from "@/types";

type Props = {
  show: boolean;
  onClose: () => void;
  loading: boolean;
  recommendation: UserListItem[] | null;
  onAccept: () => void;
  onReject: () => void;
};

export default function RecommendationModal({ show, onClose, loading, recommendation, onAccept, onReject }: Props) {
  if (!show) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 relative">
        <button
          className="absolute top-2 right-2 text-gray-400 hover:text-gray-700 text-xl"
          onClick={onClose}
          aria-label="Cerrar"
        >×</button>
        <h2 className="text-2xl font-bold mb-4 text-orange-700">Lista recomendada por IA</h2>
        {loading ? (
          <div className="flex flex-col items-center py-12">
            <div className="w-10 h-10 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <div className="text-orange-700 text-lg font-semibold animate-pulse">Calculando recomendación...</div>
          </div>
        ) : recommendation && recommendation.length > 0 ? (
          <>
            <ul className="mb-4 max-h-52 overflow-y-auto">
              {recommendation.map((item, idx) => (
                <li key={item.id} className="flex justify-between py-2 border-b last:border-0">
                  <span>
                    {item.name}
                    <span className="ml-2 text-xs text-gray-500">x{item.quantity}</span>
                    <span className="ml-2 text-orange-600 text-xs">€{(item.price * item.quantity).toFixed(2)}</span>
                  </span>
                </li>
              ))}
            </ul>
            <div className="font-bold mb-3">
              Total recomendado: <span className="text-green-700">
                €{recommendation.reduce((sum, i) => sum + (i.price || 0) * i.quantity, 0).toFixed(2)}
              </span>
            </div>
            <div className="flex gap-4">
              <button
                className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded font-bold"
                onClick={onAccept}
              >Aceptar</button>
              <button
                className="bg-gray-400 hover:bg-gray-600 text-white px-5 py-2 rounded font-bold"
                onClick={onReject}
              >Rechazar y ver otra</button>
            </div>
          </>
        ) : (
          <div className="text-gray-500 text-center">No hay una recomendación disponible.</div>
        )}
      </div>
    </div>
  );
}
