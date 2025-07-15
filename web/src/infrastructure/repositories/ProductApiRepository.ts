import type { Product } from "@/domain/entities/Product";
import { ProductRepository } from "@/domain/ports/ProductRepository";
import { RequestProxy } from './RequestProxy';
import { getURL } from './urlHandler';

export function ProductApiRepository(): ProductRepository {
  return {
    async getByFilter(): Promise<Product[] | Error>{
      const requestProxy = RequestProxy();
      const url = getURL(`/api/products`);
      return await requestProxy.http<Product[]>({
				url,
				method: 'GET',
				onSuccess: (data: any) => data,
				onFailure: (error: Error) => error,
			});
    },
  }
}
