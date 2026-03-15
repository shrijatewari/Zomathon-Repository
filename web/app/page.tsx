import { Fragment } from "react";

import {
  AlertTriangle,
  ArrowRight,
  BrainCircuit,
  Clock3,
  FileText,
  Github,
  LayoutDashboard,
  MapPinned,
  Radar,
  Route,
  Sparkles,
  TimerReset,
  Truck,
  Waves,
} from "lucide-react";

import { DisplayCardsDemo } from "@/components/display-cards-demo";
import { HeroScrollDemo } from "@/components/hero-scroll-demo";
import { GlassFilter, PrepSenseLinksDock } from "@/components/ui/liquid-glass";
import { HeroGeometric } from "@/components/ui/shape-landing-hero";

const problemCards = [
  {
    icon: Clock3,
    title: "Manual ready signals are delayed",
    description:
      "Platforms depend on merchant-marked 'food ready' timestamps that often lag actual kitchen completion by several minutes.",
  },
  {
    icon: Truck,
    title: "Riders arrive at the wrong time",
    description:
      "Inaccurate prep signals force riders to wait outside restaurants or arrive after food has already cooled down.",
  },
  {
    icon: AlertTriangle,
    title: "Customers see unreliable ETAs",
    description:
      "Noisy kitchen telemetry cascades into poor dispatch timing, weak ETA promises, and lower operational efficiency.",
  },
];

const solutionCards = [
  {
    icon: Radar,
    title: "Ground Truth Reconstruction",
    description:
      "Rebuild the true packed-time signal from observable rider and kitchen events instead of merchant taps alone.",
  },
  {
    icon: Waves,
    title: "Telemetry-Based Signals",
    description:
      "Combine pickup, arrival, merchant, and queue signals with reliability-aware weighting.",
  },
  {
    icon: BrainCircuit,
    title: "Real-Time Prediction Updates",
    description:
      "Continuously update prep-time estimates as new observations stream into the system.",
  },
  {
    icon: Route,
    title: "Dispatch Optimization",
    description:
      "Convert improved prep estimates into better rider assignment timing and lower idle time.",
  },
];

const architectureFlow = [
  "Order Event",
  "Telemetry Signals",
  "Ground Truth Reconstruction",
  "Prediction Engine",
  "Dispatch Optimization",
];

const impactStats = [
  { label: "Idle Time Reduction", value: "27.6%", note: "Lower rider wait outside kitchens" },
  { label: "ETA Error Improvement", value: "25%", note: "More stable customer promises" },
  { label: "Variance Reduction", value: "21%", note: "Better signal quality for dispatch timing" },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-zinc-100/50 via-zinc-50 to-zinc-100/40 text-zinc-900">
      <header className="sticky top-0 z-50 border-b border-zinc-200 bg-white/95 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3 lg:px-10">
          <a href="#hero" className="flex items-center gap-3 font-semibold tracking-wide">
            <span className="rounded-full bg-rose-100 px-3 py-1 text-sm text-rose-600">
              PrepSense
            </span>
            <span className="hidden text-sm text-zinc-500 md:inline">
              Kitchen Signal Intelligence
            </span>
          </a>
          <nav className="hidden items-center gap-6 text-sm text-zinc-600 md:flex">
            <a href="#problem" className="transition hover:text-zinc-950">Problem</a>
            <a href="#solution" className="transition hover:text-zinc-950">Solution</a>
            <a href="#architecture" className="transition hover:text-zinc-950">Architecture</a>
            <a href="#demo" className="transition hover:text-zinc-950">Demo</a>
          </nav>
          <a
            href="http://localhost:8504"
            target="_blank"
            rel="noreferrer"
            className="rounded-full bg-rose-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-rose-400"
          >
            Open Demo
          </a>
        </div>
      </header>

      <HeroGeometric
        badge="PrepSense"
        title1="Recover the true kitchen signal"
        title2="before the rider ever waits"
        subtitle="PrepSense combines noisy telemetry, reconstructs packed-time truth, and turns that signal into better dispatch timing."
      />

      <section className="mx-auto max-w-7xl px-6 pt-8 lg:px-10 lg:pt-12">
        <div className="grid items-center gap-6 lg:grid-cols-[1.05fr_1fr]">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
              Why PrepSense
            </p>
            <h1 className="mt-3 max-w-3xl text-3xl font-bold tracking-tight text-zinc-950 md:text-5xl">
              Recover the true kitchen signal before the rider ever waits.
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-zinc-600">
              PrepSense combines noisy telemetry, reconstructs packed-time truth,
              and turns that signal into better dispatch timing, lower rider idle
              time, and tighter customer ETAs.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <a
                href="http://localhost:8504"
                target="_blank"
                rel="noreferrer"
                className="rounded-full border border-zinc-300 bg-white px-5 py-3 text-sm font-medium text-zinc-800 transition hover:bg-zinc-50"
              >
                Open live dashboard
              </a>
            </div>
          </div>
          <DisplayCardsDemo />
        </div>
      </section>

      <section id="hero" className="mx-auto max-w-7xl px-6 pt-8 pb-4 lg:px-10 lg:pt-12">
        <HeroScrollDemo />
      </section>

      <section id="problem" className="mx-auto max-w-7xl px-6 py-12 lg:px-10 lg:py-16">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
            Problem Statement
          </p>
          <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-4xl">
            The Hidden Problem in Food Delivery
          </h2>
          <p className="mt-4 text-base leading-7 text-zinc-600">
            Platforms rely on merchant-marked &quot;Food Ready&quot; signals, which
            are often inaccurate due to manual reporting delays. That breaks ETA
            trust and wastes rider time exactly where operations are most sensitive.
          </p>
        </div>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {problemCards.map(({ icon: Icon, title, description }) => (
            <article
              key={title}
              className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm"
            >
              <div className="mb-4 inline-flex rounded-xl bg-rose-50 p-2.5 text-rose-500">
                <Icon className="size-6" />
              </div>
              <h3 className="text-lg font-semibold">{title}</h3>
              <p className="mt-2 text-sm leading-6 text-zinc-600">{description}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="solution" className="mx-auto max-w-7xl px-6 py-12 lg:px-10 lg:py-16">
        <div className="grid gap-8 lg:grid-cols-[1.1fr_1.4fr]">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
              Our Solution
            </p>
            <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-4xl">
              PrepSense Signal Intelligence Layer
            </h2>
            <p className="mt-4 text-base leading-7 text-zinc-600">
              PrepSense reconstructs the true kitchen preparation signal using
              rider telemetry and event data before it reaches the prediction and
              dispatch layers.
            </p>
            <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 p-5">
              <div className="flex items-start gap-4">
                <Sparkles className="mt-1 size-6 text-rose-500" />
                <p className="text-sm leading-7 text-zinc-700">
                  Instead of trusting a single noisy event, we combine multiple
                  telemetry signals and weight them by reliability. That means
                  cleaner prep-time estimates, sharper ETA updates, and better
                  dispatch timing.
                </p>
              </div>
            </div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {solutionCards.map(({ icon: Icon, title, description }) => (
              <article
                key={title}
                className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm"
              >
                <div className="mb-4 inline-flex rounded-xl bg-rose-50 p-2.5 text-rose-500">
                  <Icon className="size-5" />
                </div>
                <h3 className="text-lg font-semibold">{title}</h3>
                <p className="mt-2 text-sm leading-6 text-zinc-600">{description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="architecture" className="mx-auto max-w-7xl px-6 py-12 lg:px-10 lg:py-16">
        <p className="text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
          System Architecture
        </p>
        <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-4xl">
          From raw events to better dispatch timing
        </h2>
        <div className="mt-8 grid gap-3 lg:grid-cols-9">
          {architectureFlow.map((step, index) => (
            <Fragment key={step}>
              <div className="flex min-h-20 items-center justify-center rounded-2xl border border-zinc-200 bg-white p-4 text-center text-sm font-medium text-zinc-800 shadow-sm lg:col-span-1">
                {step}
              </div>
              {index < architectureFlow.length - 1 ? (
                <div className="flex items-center justify-center lg:col-span-1">
                  <ArrowRight className="size-6 text-rose-400" />
                </div>
              ) : null}
            </Fragment>
          ))}
        </div>
      </section>

      <section id="demo" className="mx-auto max-w-7xl px-6 py-12 lg:px-10 lg:py-16">
        <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
              Live Platform Simulation
            </p>
            <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-4xl">
              PrepSense in action
            </h2>
            <p className="mt-4 text-base leading-7 text-zinc-600">
              Our prototype simulates a food delivery platform in real time,
              demonstrating how PrepSense improves operational decisions.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <a
                href="http://localhost:8504"
                target="_blank"
                rel="noreferrer"
                className="rounded-full bg-rose-500 px-5 py-3 text-sm font-medium text-white transition hover:bg-rose-400"
              >
                Open Streamlit Dashboard
              </a>
              <a
                href="#impact"
                className="rounded-full border border-zinc-300 bg-white px-5 py-3 text-sm font-medium text-zinc-800 transition hover:bg-zinc-50"
              >
                See Business Impact
              </a>
            </div>
          </div>
          <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
            <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-4">
              <div className="flex items-center justify-between border-b border-zinc-200 pb-4">
                <div>
                  <p className="text-sm uppercase tracking-[0.3em] text-zinc-500">
                    Simulation Dashboard
                  </p>
                  <p className="mt-2 text-xl font-semibold text-zinc-900">Live Dispatch + Signal Monitor</p>
                </div>
                <MapPinned className="size-8 text-rose-500" />
              </div>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <div className="rounded-xl bg-white p-3 shadow-sm">
                  <p className="text-xs uppercase tracking-[0.25em] text-zinc-500">Realtime</p>
                  <p className="mt-2 text-2xl font-bold text-rose-500">200ms</p>
                  <p className="mt-2 text-sm text-zinc-600">WebSocket event streaming cadence</p>
                </div>
                <div className="rounded-xl bg-white p-3 shadow-sm">
                  <p className="text-xs uppercase tracking-[0.25em] text-zinc-500">Filtering</p>
                  <p className="mt-2 text-2xl font-bold text-rose-500">Weighted</p>
                  <p className="mt-2 text-sm text-zinc-600">Observed vs filtered signal monitoring</p>
                </div>
                <div className="rounded-xl bg-white p-3 shadow-sm">
                  <p className="text-xs uppercase tracking-[0.25em] text-zinc-500">Dispatch</p>
                  <p className="mt-2 text-2xl font-bold text-rose-500">Optimized</p>
                  <p className="mt-2 text-sm text-zinc-600">ETA-aware rider assignment decisions</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </section>

      <section id="impact" className="mx-auto max-w-7xl px-6 py-12 lg:px-10 lg:py-16">
        <p className="text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
          Business Impact
        </p>
        <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-4xl">
          Why this matters at platform scale
        </h2>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {impactStats.map((stat) => (
            <article
              key={stat.label}
              className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm"
            >
              <div className="flex items-center justify-between">
                <p className="text-sm uppercase tracking-[0.25em] text-zinc-500">
                  {stat.label}
                </p>
                <TimerReset className="size-5 text-rose-500" />
              </div>
              <p className="mt-4 text-4xl font-bold text-rose-500">{stat.value}</p>
              <p className="mt-3 text-sm leading-6 text-zinc-600">{stat.note}</p>
            </article>
          ))}
        </div>
      </section>

      <footer className="border-t border-zinc-200 bg-white">
        <div className="mx-auto grid max-w-7xl gap-6 px-6 py-10 lg:grid-cols-[1fr_auto] lg:px-10">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-rose-500">
              Team + Project
            </p>
            <h2 className="mt-3 text-2xl font-bold">Built for Zomathon Hackathon</h2>
            <p className="mt-3 max-w-2xl text-sm leading-7 text-zinc-600">
              PrepSense demonstrates how a signal-intelligence layer can sit
              between restaurant operations and dispatch systems to produce
              more trustworthy predictions and better platform decisions.
            </p>
          </div>
          <div className="flex flex-col gap-4">
            <GlassFilter />
            <PrepSenseLinksDock
              links={[
                {
                  href: "http://localhost:8504",
                  icon: <LayoutDashboard className="size-6" />,
                  label: "Dashboard",
                },
                {
                  href: "https://github.com/shrijatewari/Zomathon-Repository",
                  icon: <Github className="size-6" />,
                  label: "GitHub",
                },
                {
                  href: "https://docs.google.com/document/d/1p_1aCEe3CYLZFwiwJj0JPjoQj14DqIz86oY4T0-WugE/edit?usp=sharing",
                  icon: <FileText className="size-6" />,
                  label: "Document",
                },
              ]}
            />
          </div>
        </div>
      </footer>
    </main>
  );
}
