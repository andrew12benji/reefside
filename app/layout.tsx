import type { Metadata, Viewport } from "next";
import { Press_Start_2P } from "next/font/google";
import "./globals.css";

const pressStart = Press_Start_2P({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-press-start",
});

export const metadata: Metadata = {
  title: "REEFSIDE - Marine Conservation Simulator",
  description:
    "Protect the Great Barrier Reef in this retro-style conservation game. Complete UN SDG 14 target of 30% reef protection by 2030.",
  keywords: [
    "reef",
    "conservation",
    "game",
    "SDG 14",
    "ocean",
    "marine",
    "coral",
    "Great Barrier Reef",
  ],
  authors: [{ name: "REEFSIDE Team" }],
  openGraph: {
    title: "REEFSIDE - Marine Conservation Simulator",
    description: "Protect the Great Barrier Reef. 30x30 by 2030.",
    type: "website",
  },
};

export const viewport: Viewport = {
  themeColor: "#020C1A",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={pressStart.variable}>
      <body className="bg-background font-press antialiased">{children}</body>
    </html>
  );
}
