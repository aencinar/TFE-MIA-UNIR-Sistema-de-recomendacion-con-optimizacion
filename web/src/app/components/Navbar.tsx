"use client";

import { FC, useState } from "react";
import Link from "next/link";

interface NavbarProps {
  /**
   * Indica si el usuario está logueado o no.
   */
  isLoggedIn?: boolean;
}

const Navbar: FC<NavbarProps> = ({ isLoggedIn = false }) => {
  const [menuOpen, setMenuOpen] = useState<boolean>(false);

  const toggleMenu = (): void => {
    setMenuOpen(!menuOpen);
  };

  const handleLogout = (): void => {
    // Lógica para cerrar sesión o llamar a una función externa
    console.log("Cerrando sesión...");
    setMenuOpen(false);
  };

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo / Nombre del Portal */}
        <div className="text-xl font-bold text-gray-800">
          <Link href="/">
            Despensia
          </Link>
        </div>

        {/* Botón Hamburguesa (versión Móvil) */}
        <button
          onClick={toggleMenu}
          className="md:hidden flex items-center text-gray-700 focus:outline-none"
        >
          <svg className="h-6 w-6 fill-current" viewBox="0 0 24 24">
            <path d="M4 5h16M4 12h16M4 19h16"></path>
          </svg>
        </button>

        {/* Menú en Escritorio */}
        <div className="hidden md:flex items-center space-x-6">
          <Link
            href="/"
            className="text-gray-700 hover:text-blue-600"
          >
            Inicio
          </Link>
          <Link
            href="/categorias"
            className="text-gray-700 hover:text-blue-600"
          >
            Categorías
          </Link>
          <Link
            href="/shoppingCart"
            className="text-gray-700 hover:text-blue-600"
          >
            Genera tu carrito
          </Link>
        </div>

        {/* Opciones de Usuario (Escritorio) */}
        <div className="hidden md:flex items-center space-x-4">
          {isLoggedIn ? (
            <>
              <Link
                href="/account"
                className="text-gray-700 hover:text-blue-600"
              >
                Mi Cuenta
              </Link>
              <button
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                onClick={handleLogout}
              >
                Cerrar Sesión
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-gray-700 hover:text-blue-600"
              >
                Iniciar Sesión
              </Link>
              <Link
                href="/register"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Registrarse
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Menú Desplegable para Móvil */}
      {menuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <Link
            href="/"
            className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
            onClick={() => setMenuOpen(false)}
          >
            Inicio
          </Link>
          <Link
            href="/categorias"
            className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
            onClick={() => setMenuOpen(false)}
          >
            Categorías
          </Link>
          <Link
            href="/ofertas"
            className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
            onClick={() => setMenuOpen(false)}
          >
            Ofertas
          </Link>

          {isLoggedIn ? (
            <>
              <Link
                href="/cuenta"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                onClick={() => setMenuOpen(false)}
              >
                Mi Cuenta
              </Link>
              <button
                className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100"
                onClick={handleLogout}
              >
                Cerrar Sesión
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                onClick={() => setMenuOpen(false)}
              >
                Iniciar Sesión
              </Link>
              <Link
                href="/registro"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                onClick={() => setMenuOpen(false)}
              >
                Registrarse
              </Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
