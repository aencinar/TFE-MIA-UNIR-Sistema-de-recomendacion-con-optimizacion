import type { Product } from "../entities/Product";

export interface ProductRepository {
  getByFilter: () => Promise<Product[] | Error>;
}