eroski_scrape_list = [
    # Aceite, Vinagre, Sal, Harina y Pan Rallado
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado/2059992-aceite-de-girasol/", "category_name": "Aceite", "subcategory_name": "Aceite de girasol"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado/2059989-aceite-de-oliva/", "category_name": "Aceite", "subcategory_name": "Aceite de oliva"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado/2059998-harina/", "category_name": "Harina y masas", "subcategory_name": "Harina"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado/2060000-sal/", "category_name": "Sal", "subcategory_name": "Sal"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2059988-aceite-vinagre-sal-harina-y-pan-rallado/2059995-vinagre/", "category_name": "Vinagre", "subcategory_name": "Vinagre"},

    # Aperitivos
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060006-aperitivos/", "category_name": "Aperitivos", "subcategory_name": "Aperitivos variados"}, # General category

    # Arroz, Legumbres y Pasta
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060012-arroz-legumbres-y-pasta/2060013-arroz/", "category_name": "Arroz", "subcategory_name": "Arroz"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060012-arroz-legumbres-y-pasta/2060018-legumbres/", "category_name": "Legumbre", "subcategory_name": "Legumbres"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060012-arroz-legumbres-y-pasta/2060015-pasta/", "category_name": "Pasta", "subcategory_name": "Pasta"},

    # Bebidas
    {"url": "https://supermercado.eroski.es/es/supermercado/2059808-bebidas/2060415-agua/", "category_name": "Bebidas sin alcohol", "subcategory_name": "Agua"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059808-bebidas/2060451-refrescos-con-gas/", "category_name": "Bebidas sin alcohol", "subcategory_name": "Refrescos con gas"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059808-bebidas/2060455-refrescos-sin-gas/", "category_name": "Bebidas sin alcohol", "subcategory_name": "Refrescos sin gas"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059808-bebidas/2060423-zumos/", "category_name": "Zumos", "subcategory_name": "Zumos"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059808-bebidas/2060468-cervezas/", "category_name": "Bebidas con alcohol", "subcategory_name": "Cervezas"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059808-bebidas/2060510-vinos/", "category_name": "Bebidas con alcohol", "subcategory_name": "Vinos"},

    # Cacao, Café e Infusiones
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060024-cacao-cafe-e-infusiones/2060025-cacao/", "category_name": "Cacao, café, infusiones", "subcategory_name": "Cacao"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060024-cacao-cafe-e-infusiones/2060030-cafe/", "category_name": "Cacao, café, infusiones", "subcategory_name": "Café"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060024-cacao-cafe-e-infusiones/2060040-infusiones/", "category_name": "Cacao, café, infusiones", "subcategory_name": "Infusiones"},

    # Caldos, Sopas y Cremas
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060045-caldos-sopas-y-cremas/", "category_name": "Caldos y sopas", "subcategory_name": "Caldos, sopas y cremas"},

    # Carne y Pescado (Frescos)
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059700-carniceria/2059701-aves-y-conejo/", "category_name": "Carne", "subcategory_name": "Aves y conejo"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059700-carniceria/2059712-cerdo/", "category_name": "Carne", "subcategory_name": "Cerdo"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059731-pescaderia/2059732-pescado-fresco/", "category_name": "Pescado", "subcategory_name": "Pescado fresco"},

    # Cereales y Galletas
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060070-cereales-y-galletas/2060071-cereales-de-desayuno/", "category_name": "Cereales", "subcategory_name": "Cereales de desayuno"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060070-cereales-y-galletas/2060076-galletas/", "category_name": "Galletas", "subcategory_name": "Galletas"},

    # Charcutería y Quesos
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059756-charcuteria-y-quesos/2059775-quesos/", "category_name": "Quesos", "subcategory_name": "Quesos"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059756-charcuteria-y-quesos/2059757-charcuteria-cocida/", "category_name": "Charcuteria", "subcategory_name": "Charcutería cocida"},

    # Congelados
    {"url": "https://supermercado.eroski.es/es/supermercado/2059807-congelados/2060271-platos-preparados/", "category_name": "Congelados", "subcategory_name": "Platos preparados congelados"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059807-congelados/2060266-pizzas-y-masas-congeladas/", "category_name": "Pizzas", "subcategory_name": "Pizzas congeladas"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059807-congelados/2060258-verduras-y-hortalizas-congeladas/", "category_name": "Congelados", "subcategory_name": "Verduras congeladas"},


    # Conservas
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060092-conservas-y-platos-preparados/2060093-conservas-de-pescado/", "category_name": "Conservas", "subcategory_name": "Conservas de pescado"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060092-conservas-y-platos-preparados/2060107-conservas-vegetales/", "category_name": "Conservas", "subcategory_name": "Conservas vegetales"},

    # Dulces y Pastelería (No frescos)
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060151-dulces-y-postres/2060152-azucar-y-edulcorantes/", "category_name": "Azucar, edulcorantes, otros", "subcategory_name": "Azúcar y edulcorantes"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060151-dulces-y-postres/2060160-mermeladas-y-miel/", "category_name": "Mermelada, membrillo, miel, otros", "subcategory_name": "Mermeladas y miel"},

    # Frescos (Fruta, Verduras, Panadería)
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059699-fruteria/2059703-fruta-de-hueso/", "category_name": "Fruta", "subcategory_name": "Fruta de hueso"}, # Example, specific subcategories are better
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059699-fruteria/", "category_name": "Fruta", "subcategory_name": "Fruta variada"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059717-verduras-y-hortalizas/", "category_name": "Verduras", "subcategory_name": "Verduras y hortalizas variadas"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059783-panaderia-y-pasteleria/2059785-pan-blanco/", "category_name": "Panaderia", "subcategory_name": "Pan blanco"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059783-panaderia-y-pasteleria/2059793-bolleria-y-pasteleria/", "category_name": "Dulces y pasteleria", "subcategory_name": "Bollería y pastelería fresca"},

    # Lácteos y Huevos
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060192-lacteos-y-huevos/2060193-huevos/", "category_name": "Huevos", "subcategory_name": "Huevos"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060192-lacteos-y-huevos/2060196-leche/", "category_name": "Lacteos", "subcategory_name": "Leche"},
    {"url": "https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/2060192-lacteos-y-huevos/2060205-yogures/", "category_name": "Lacteos", "subcategory_name": "Yogures"},
]
