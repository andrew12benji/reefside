"use client";

import dynamic from "next/dynamic";

// Dynamic import with SSR disabled for canvas-based game
const UnderwaterGame = dynamic(
  () => import("@/components/game/UnderwaterGame"),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-screen w-screen items-center justify-center bg-[#020C1A]">
        <div className="text-center">
          <div className="mb-4 text-2xl text-[#00E8D8]">REEFSIDE</div>
          <div className="text-sm text-[#3388AA]">Loading...</div>
        </div>
      </div>
    ),
  }
);

export default function Home() {
  return (
    <main className="h-screen w-screen overflow-hidden bg-[#020C1A]">
      <UnderwaterGame />
    </main>
  );
}
