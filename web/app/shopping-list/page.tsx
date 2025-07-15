'use client';

import { useEffect, useState } from "react";
import {
  Product, UserListItem, Category,
  RESTRICTIONS, CATEGORY_MAP,
  getCategoryName, getRestrictionName
} from "@/types";

const PAGE_SIZE = 40;

export default function ProductCatalogWithSidebar() {
  const [catalog, setCatalog] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [page, setPage] = useState<number>(1);
  const [selectedCategories, setSelectedCategories] = useState<number[]>([]);
  const [selectedRestrictions, setSelectedRestrictions] = useState<string[]>([]);
  const [search, setSearch] = useState("");
  const [userList, setUserList] = useState<UserListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [budget, setBudget] = useState<number | ''>('');
  const [sending, setSending] = useState(false);

  const [showRecommendationModal, setShowRecommendationModal] = useState(false);
  const [recommendation, setRecommendation] = useState<UserListItem[] | null>(null);
  const [loadingRecommendation, setLoadingRecommendation] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const [hasMore, setHasMore] = useState(true);


  useEffect(() => {
    setLoading(true);

    const params = new URLSearchParams();
    selectedCategories.forEach(cat => params.append("categories", String(cat)));
    selectedRestrictions.forEach(r => params.append("restrictions", getRestrictionName(r)));
    params.append("page", String(page));
    params.append("size", String(PAGE_SIZE));

    fetch(`${apiUrl}/api/catalog?${params.toString()}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    })
      .then(res => res.json())
      .then(data => {
        setPage(data.page);

        setCatalog(prev =>
          page === 1
            ? data.products.map((p: any) => ({
                ...p,
                id: p.id ?? p.product_code ?? p._id ?? Math.random(),
                categoryId: p.category
              }))
            : [
                ...prev,
                ...data.products.map((p: any) => ({
                  ...p,
                  id: p.id ?? p.product_code ?? p._id ?? Math.random(),
                  categoryId: p.category
                })),
              ]
        );
        setHasMore(data.products.length === PAGE_SIZE);
      })
      .finally(() => setLoading(false));

    setCategories(
      Object.entries(CATEGORY_MAP).map(([id, name]) => ({
        id: Number(id),
        name
      }))
    );
    // eslint-disable-next-line
  }, [selectedCategories, selectedRestrictions, page, search]);


  function addToList(product: Product) {
    setUserList(list => {
      const idx = list.findIndex(item => item.id === product.id);
      if (idx > -1) {
        return list.map((item, i) =>
          i === idx ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...list, { ...product, quantity: 1 }];
    });
  }
  function removeFromList(idx: number) {
    setUserList(list => {
      if (list[idx].quantity > 1) {
        return list.map((item, i) =>
          i === idx ? { ...item, quantity: item.quantity - 1 } : item
        );
      }
      return list.filter((_, i) => i !== idx);
    });
  }

  // Cálculo del total y presupuesto
  const total = userList.reduce((sum, item) => sum + (item.price || 0) * item.quantity, 0);

  // Enviar la lista de la compra
  function handleSend() {
    setSending(true);
    const productsPayload = userList.map(item => ({
      _id: item.id,
      product_code: item.product_code,
      name: item.name
    }));

    fetch(`${apiUrl}/api/recommendation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        products: productsPayload,
        budget: budget === "" ? null : Number(budget),
        lactoseFree: selectedRestrictions.includes("lactose"),
        glutenFree: selectedRestrictions.includes("gluten"),
        soyFree: selectedRestrictions.includes("soja"),
        vegan: selectedRestrictions.includes("vegan"),
      }),
    })
      .then(res => {
        if (res.ok) {
          alert("¡Lista enviada correctamente!");
        } else {
          alert("Error al enviar la lista");
        }
      })
      .catch(() => alert("Error de red al enviar la lista"))
      .finally(() => setSending(false));
  }

  function toggleCategory(catId: number) {
    setSelectedCategories(c =>
      c.includes(catId) ? c.filter(id => id !== catId) : [...c, catId]
    );
    setPage(1);
  }
  function toggleRestriction(rid: string) {
    setSelectedRestrictions(r =>
      r.includes(rid) ? r.filter(x => x !== rid) : [...r, rid]
    );
    setPage(1);
  }


  async function fetchRecommendation() {
    setLoadingRecommendation(true);
    setShowRecommendationModal(true);
    try {
      const res = await fetch(`${apiUrl}/api/recommendation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          products: userList.map(item => ({
            _id: item.id.toString(),
            product_code: item.id.toString(),
            name: item.name
          })),
          budget: parseFloat(budget as any),
          lactoseFree: selectedRestrictions.includes("lactose"),
          glutenFree: selectedRestrictions.includes("gluten"),
          soyFree: selectedRestrictions.includes("soja"),
          vegan: selectedRestrictions.includes("vegan"),
        }),
      });
      if (!res.ok) throw new Error();
      const data = await res.json();
      setRecommendation(
        data.products.map((p: any) => ({
          id: parseInt(p.product_code),
          name: p.name,
          categoryId: p.category,
          subcategory: p.subcategory,
          price: p.price,
          quantity: 1
        }))
      );
    } catch {
      setRecommendation([]);
    } finally {
      setLoadingRecommendation(false);
    }
  }

  return (
    <div className="flex w-full min-h-screen bg-gray-50">
      {/* --- SIDEBAR --- */}
      <aside className="w-72 bg-white shadow-lg p-6 flex flex-col gap-8">
        <div>
          <h3 className="font-bold mb-2 text-lg text-orange-700">Buscar producto</h3>
          <input
            className="w-full border rounded px-3 py-2"
            type="text"
            placeholder="Buscar por nombre..."
            value={search}
            onChange={e => {
              setSearch(e.target.value);
              setPage(1);
            }}
            disabled={loading}
          />
        </div>
        <div>
          <h3 className="font-bold mb-2 text-lg text-orange-700">Filtrar por categoría</h3>
          <div className="max-h-56 overflow-y-auto space-y-1">
            {categories.map(cat => (
              <label key={cat.id} className="flex items-center gap-2 text-gray-700 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedCategories.includes(cat.id)}
                  onChange={() => toggleCategory(cat.id)}
                  className="accent-orange-600"
                  disabled={loading}
                />
                {cat.name}
              </label>
            ))}
          </div>
        </div>
        <div>
          <h3 className="font-bold mb-2 text-lg text-orange-700">Restricciones</h3>
          <div className="space-y-1">
            {RESTRICTIONS.map(r => (
              <label key={r.id} className="flex items-center gap-2 text-gray-700 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedRestrictions.includes(r.id)}
                  onChange={() => toggleRestriction(r.id)}
                  className="accent-orange-600"
                  disabled={loading}
                />
                {r.label}
              </label>
            ))}
          </div>
        </div>
        <div className="mb-4">
          <label className="mr-2 font-semibold">Presupuesto (€):</label>
          <input
            type="number"
            min={0}
            className="border rounded px-2 py-1 w-24"
            value={budget}
            onChange={e => setBudget(e.target.value === '' ? '' : Number(e.target.value))}
            placeholder="Máximo"
          />
        </div>
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
                    onClick={() => addToList(item)}
                    title="Añadir uno más"
                  >+</button>
                  <button
                    className="text-red-500 hover:text-red-700 text-xs"
                    onClick={() => removeFromList(idx)}
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
          {/* Botón pedir recomendación IA */}
          <button
            className="w-full mt-2 px-4 py-2 rounded-lg font-bold bg-indigo-600 text-white hover:bg-indigo-700 transition"
            disabled={userList.length === 0}
            onClick={fetchRecommendation}
          >
            Recomendar lista óptima IA
          </button>
        </div>
      </aside>

      {/* --- GRID DE PRODUCTOS --- */}
      <main className="flex-1 p-10">
        <h2 className="text-2xl font-bold text-orange-700 mb-4">Catálogo de productos</h2>
        {loading ? (
          <div className="flex flex-col items-center justify-center h-64">
            <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <div className="text-orange-700 text-lg font-semibold animate-pulse">Cargando productos...</div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-7">
              {catalog.map(product => (
                <div
                  key={product.id}
                  className="bg-white rounded-2xl shadow-md hover:shadow-lg p-5 flex flex-col justify-between"
                >
                  <span className="font-semibold text-lg mb-2">{product.name}</span>
                  <span className="text-xs text-gray-500 mb-2">{getCategoryName(product.categoryId)}</span>
                  <div className="flex gap-2 flex-wrap mb-4">
                    <span className="bg-orange-100 text-orange-700 text-xs px-2 py-0.5 rounded">{product.subcategory}</span>
                  </div>
                  <span className="font-bold mb-2 text-orange-700">
                    €{product.price?.toFixed(2) ?? "-"}
                  </span>
                  <button
                    className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded font-bold mt-auto"
                    onClick={() => addToList(product)}
                  >Añadir a mi lista</button>
                </div>
              ))}
            </div>
            {/* Botón "Cargar más" */}
            {hasMore && (
              <div className="flex justify-center mt-8">
                <button
                  className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg shadow font-bold"
                  onClick={() => setPage(page => page + 1)}
                >
                  Cargar más productos
                </button>
              </div>
            )}
            {/* Mensaje si no hay productos */}
            {catalog.length === 0 && (
              <div className="text-gray-400 text-center my-12">
                No hay productos que cumplan los filtros seleccionados.
              </div>
            )}
          </>
        )}
      </main>

      {/* MODAL RECOMENDACIÓN IA */}
      {showRecommendationModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 relative">
            <button
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-700 text-xl"
              onClick={() => setShowRecommendationModal(false)}
              aria-label="Cerrar"
            >×</button>
            <h2 className="text-2xl font-bold mb-4 text-orange-700">Lista recomendada por IA</h2>

            {loadingRecommendation ? (
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
                  Total recomendado: <span className="text-green-700">€
                    {recommendation.reduce((sum, i) => sum + (i.price || 0) * i.quantity, 0).toFixed(2)}
                  </span>
                </div>
                <div className="flex gap-4">
                  <button
                    className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded font-bold"
                    onClick={() => {
                      setUserList(recommendation);
                      setShowRecommendationModal(false);
                    }}
                  >Aceptar</button>
                  <button
                    className="bg-gray-400 hover:bg-gray-600 text-white px-5 py-2 rounded font-bold"
                    onClick={async () => {
                      setRecommendation(null);
                      setLoadingRecommendation(true);
                      try {
                        const res = await fetch("/api/recommendation", {
                          method: "POST",
                          headers: { "Content-Type": "application/json" },
                          body: JSON.stringify({
                            products: userList,
                            budget: budget === "" ? null : Number(budget)
                          }),
                        });
                        if (!res.ok) throw new Error("Error obteniendo recomendación");
                        const data = await res.json();
                        setRecommendation(
                          data.products.map((p: any) => ({
                            ...p,
                            id: p.id ?? p.product_code ?? p._id ?? Math.random(),
                            categoryId: p.category
                          }))
                        );
                      } catch {
                        setRecommendation([]);
                      } finally {
                        setLoadingRecommendation(false);
                      }
                    }}
                  >Rechazar y ver otra</button>
                </div>
              </>
            ) : (
              <div className="text-gray-500 text-center">No hay una recomendación disponible.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
