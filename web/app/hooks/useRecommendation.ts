import { useState } from "react";
import { UserListItem } from "@/types";

export function useRecommendation(userList: UserListItem[], budget: number | '') {
  const [show, setShow] = useState(false);
  const [recommendation, setRecommendation] = useState<UserListItem[] | null>(null);
  const [loading, setLoading] = useState(false);

  async function fetchRecommendation() {
    setLoading(true);
    setShow(true);
    try {
      const res = await fetch("/api/recommendation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          products: userList,
          budget: budget === "" ? null : Number(budget)
        }),
      });
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
      setLoading(false);
    }
  }

  return {
    show,
    setShow,
    recommendation,
    setRecommendation,
    loading,
    fetchRecommendation,
  };
}
