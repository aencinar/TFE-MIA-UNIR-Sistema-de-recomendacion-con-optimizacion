import Image from "next/image";

export default function Home() {
  return (
    <div className="w-full max-w-4xl mx-auto my-12 bg-white rounded-2xl shadow-xl flex flex-col md:flex-row items-center p-8 gap-8">
      {/* Izquierda: Texto y botones */}
      <div className="flex-1 flex flex-col gap-8">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 leading-tight">
          Bienvenido a <br />
          <span className="text-black">Dispensia</span>
        </h1>
        <p className="text-gray-600 max-w-lg">
          Todo en uno para explorar y crear listas de la compra fácilmente.
        </p>
        <div className="flex gap-4">
          <a href="/products" className="bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-6 rounded transition">
            Ver Catálogo
          </a>
          <a href="/shopping-list" className="bg-black hover:bg-gray-800 text-white font-semibold py-2 px-6 rounded transition">
            Mi Lista de la Compra
          </a>
        </div>
      </div>
      {/* Derecha: Imagen */}
      <div className="flex-1 flex justify-center">
        <Image
          src="/basket.jpg"
          alt="Cesta de supermercado"
          width={380}
          height={260}
          className="rounded-2xl shadow-lg object-cover"
          priority
        />
      </div>
    </div>
  );
}
