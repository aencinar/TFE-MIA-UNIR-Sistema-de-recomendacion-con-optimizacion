import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getProducts } from "@/application/useCases/getProducts";
import { Product } from "@/domain/entities/Product";
import { ProductApiRepository } from "@/infrastructure/repositories/ProductApiRepository";

export const useProducts = () => {
    const repository = ProductApiRepository();
    const products = getProducts(repository).execute();

    return products;
};
