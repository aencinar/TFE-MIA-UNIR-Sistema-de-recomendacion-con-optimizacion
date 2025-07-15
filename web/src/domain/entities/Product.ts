import { z } from "zod";

export const ProductSchema = z.object({
    id: z.string(),
    name: z.string(),
    description: z.string(),
    price: z.number(),
    imageUrl: z.string().optional()
})

export type Product = z.infer<typeof ProductSchema>;