import { UserListItem } from "@/types";

type Props = {
  userList: UserListItem[];
  onAdd: (item: UserListItem) => void;
  onRemove: (idx: number) => void;
  total: number;
  budget: number | '';
  sending: boolean;
  onSend: () => void;
  onRecommend: () => void;
};

export default function UserList({ userList, onAdd, onRemove, total, budget, sending, onSend, onRecommend }: Props) {
  return (
    <div>
      <h3 className="font-bold mb-2 text-lg text-orange-700">Mi lista</h3>
      <ul>
        {userList.map((item, idx) => (
          <li key={item.id} className="flex justify-between items-center py-1 border-b last:border-0">
            <span>
              {item.name}
              <span className="ml-2 text-xs text-gray-500">x{item.quantity}</span>
              <span className="ml-2 text-orange-600 text-xs">€{(item.price * item.quantity).toFixed(2)}</span>
            </span>
            <div className="flex gap-1">
              <button
                className="text-orange-600 border px-1 rounded hover:bg-orange-100"
                onClick={() => onAdd(item)}
                title="Añadir uno más"
              >+</button>
              <button
                className="text-red-500 hover:text-red-700 text-xs"
                onClick={() => onRemove(idx)}
              >Quitar</button>
            </div>
          </li>
        ))}
      </ul>
      <div className="font-bold mt-2">
        Total: <span className={budget && total > Number(budget) ? "text-red-600" : "text-green-700"}>
          €{total.toFixed(2)}
        </span>
        {budget && total > Number(budget) && (
          <span className="ml-2 text-xs text-red-600">¡Supera el presupuesto!</span>
        )}
      </div>
      <button
        className={`w-full mt-4 px-4 py-2 rounded-lg font-bold transition ${
          userList.length === 0 || sending
            ? "bg-gray-300 text-gray-400 cursor-not-allowed"
            : "bg-orange-600 text-white hover:bg-orange-700"
        }`}
        disabled={userList.length === 0 || sending}
        onClick={onSend}
      >
        {sending ? "Enviando..." : "Enviar lista"}
      </button>
      <button
        className="w-full mt-2 px-4 py-2 rounded-lg font-bold bg-indigo-600 text-white hover:bg-indigo-700 transition"
        disabled={userList.length === 0}
        onClick={onRecommend}
      >
        Recomendar lista óptima IA
      </button>
    </div>
  );
}
