"use client";
import { LoginProvider } from "@/_components/providers/LoginProvider";
import "./globals.css";
import { Inter } from "next/font/google";
import { Quicksand } from "next/font/google";
import { Gugi } from "next/font/google";
import RelayEnvironment from "@/_lib/RelayEnvironment";
import { RelayEnvironmentProvider } from "react-relay";

const inter = Inter({ subsets: ["latin"] });
const quicksand = Quicksand({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-quicksand',
});
const gugi = Gugi({ subsets: ['latin'],weight: '400', variable: '--font-gugi' });

function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${quicksand.variable} ${gugi.variable} font-sans text-center `}>
        <RelayEnvironmentProvider environment={RelayEnvironment}>
            <LoginProvider>
              {children}
            </LoginProvider>
        </RelayEnvironmentProvider>
      </body>
    </html>
  );
}

export default RootLayout;