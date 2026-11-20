import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TradeBot AI | Research Terminal",
  description: "Signal-only simulated market research terminal",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
