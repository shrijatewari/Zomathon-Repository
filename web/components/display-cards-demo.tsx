"use client";

import { Activity, Route, Sparkles } from "lucide-react";

import DisplayCards from "@/components/ui/display-cards";

const prepsenseCards = [
  {
    icon: <Sparkles className="size-4 text-rose-200" />,
    title: "Signal Intelligence",
    description: "Filter noisy kitchen telemetry",
    date: "Weighted event filtering",
    titleClassName: "text-rose-500",
    className:
      "[grid-area:stack] border-rose-200 bg-rose-50/90 hover:-translate-y-10 before:absolute before:left-0 before:top-0 before:h-[100%] before:w-[100%] before:rounded-xl before:bg-background/50 before:bg-blend-overlay before:outline-1 before:outline-border before:transition-opacity before:duration-700 before:content-[''] hover:grayscale-0 hover:before:opacity-0 grayscale-[100%]",
  },
  {
    icon: <Activity className="size-4 text-sky-200" />,
    title: "Prediction Engine",
    description: "Update prep estimates live",
    date: "Confidence-aware ETA updates",
    titleClassName: "text-sky-500",
    className:
      "[grid-area:stack] translate-x-12 translate-y-10 border-sky-200 bg-sky-50/90 hover:-translate-y-1 before:absolute before:left-0 before:top-0 before:h-[100%] before:w-[100%] before:rounded-xl before:bg-background/50 before:bg-blend-overlay before:outline-1 before:outline-border before:transition-opacity before:duration-700 before:content-[''] hover:grayscale-0 hover:before:opacity-0 grayscale-[100%]",
  },
  {
    icon: <Route className="size-4 text-emerald-200" />,
    title: "Dispatch Timing",
    description: "Send riders at the right moment",
    date: "Operational efficiency layer",
    titleClassName: "text-emerald-500",
    className:
      "[grid-area:stack] translate-x-24 translate-y-20 border-emerald-200 bg-emerald-50/90 hover:translate-y-10",
  },
];

export function DisplayCardsDemo() {
  return (
    <div className="flex min-h-[220px] w-full items-center justify-center py-4 md:min-h-[260px] md:py-6">
      <div className="w-full max-w-3xl">
        <DisplayCards cards={prepsenseCards} />
      </div>
    </div>
  );
}
