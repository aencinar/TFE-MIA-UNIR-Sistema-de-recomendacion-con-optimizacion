import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center">
      <h1 className="text-5xl font-bold text-orange-500 mb-4">404 - Page Not Found</h1>
      <p className="text-gray-500 mb-8">
        Sorry, the page you are looking for does not exist.
      </p>
      <Link href="/" className="bg-orange-500 text-white font-bold px-6 py-3 rounded hover:bg-orange-600 transition">
        Go back to Home
      </Link>
    </div>
  );
}
