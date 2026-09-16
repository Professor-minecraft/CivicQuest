import type { Metadata, Viewport } from "next";
import { Geist, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });
const jakarta = Plus_Jakarta_Sans({ variable: "--font-jakarta", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CivicQuest — Small quests. A better city.",
  description: "Explore MPLADS public works, document local progress, and earn XP through auditor-reviewed civic quests. Your neighborhood, your impact.",
};
export const viewport: Viewport = { themeColor: "#f8f9f6", width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" className={`${geist.variable} ${jakarta.variable}`}><body>{children}</body></html>;
}
