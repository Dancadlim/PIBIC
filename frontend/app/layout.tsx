import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Plataforma UFBA",
  description: "Gerador Inteligente de Aulas",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="h-full antialiased font-sans">
      <body className="min-h-full flex flex-col bg-slate-50">{children}</body>
    </html>
  );
}
