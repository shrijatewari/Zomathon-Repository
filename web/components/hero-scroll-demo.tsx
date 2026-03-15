"use client";

import Image from "next/image";
import React from "react";

import { ContainerScroll } from "@/components/ui/container-scroll-animation";

const CANVA_LINK =
  "https://www.canva.com/design/DAHDkGZnlIo/pXaNkGuETQUoD0XNKfYM5Q/edit?utm_content=DAHDkGZnlIo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton";

export function HeroScrollDemo() {
  return (
    <div className="flex flex-col overflow-hidden pb-[140px] pt-[140px] md:pb-[180px] md:pt-[180px]">
      <ContainerScroll
        titleComponent={
          <>
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
              Platform Simulation
            </p>
            <h1 className="text-4xl font-semibold text-zinc-950 md:text-6xl">
              PrepSense: Intelligent Kitchen Prep Time Prediction
            </h1>
            <p className="mx-auto mt-6 max-w-3xl text-base leading-7 text-zinc-600 md:text-xl">
              Reconstructing kitchen signals to improve delivery efficiency,
              rider utilization, and ETA accuracy at scale.
            </p>
          </>
        }
      >
        <a
          href={CANVA_LINK}
          target="_blank"
          rel="noopener noreferrer"
          className="relative block h-full w-full overflow-hidden rounded-2xl border border-rose-200 bg-white shadow-[0_30px_80px_rgba(15,23,42,0.12)]"
        >
          <Image
            src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=1600&q=80"
            alt="Food delivery - View PrepSense presentation"
            fill
            className="object-cover object-center"
            draggable={false}
            priority
          />
          <div className="absolute inset-0 flex items-center justify-center bg-black/20 transition hover:bg-black/30">
            <span className="rounded-full bg-rose-500 px-8 py-4 text-lg font-semibold text-white shadow-lg transition hover:bg-rose-400">
              Click on this to view the presentation
            </span>
          </div>
        </a>
      </ContainerScroll>
    </div>
  );
}
