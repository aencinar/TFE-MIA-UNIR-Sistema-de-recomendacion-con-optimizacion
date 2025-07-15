import { useQuery } from "@tanstack/react-query";
import { Product, ProductSchema } from "@/domain/entities/Product";
import { ProductRepository } from "@/domain/ports/ProductRepository";
import { UseCase } from "./interfaces/UseCase";


export const getProducts = (repository: ProductRepository): UseCase<Product[]> => ({
    execute: async () => {
      const response = await repository.getByFilter();
  
      //TODO Validar con zod
      const parsed = ProductSchema.array().safeParse(response);
      if (!parsed.success) {
        throw new Error("Error de validación en los productos");
      }
  
      return parsed.data;
    }
  });