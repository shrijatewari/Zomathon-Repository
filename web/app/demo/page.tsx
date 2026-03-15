import { N8nWorkflowBlock } from "@/components/ui/n8n-workflow-block-shadcnui";

export default function DemoPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,_rgba(16,185,129,0.12),_transparent_25%),linear-gradient(180deg,#07111a_0%,#090c12_45%,#05070b_100%)] p-8">
      <div className="mx-auto w-full max-w-7xl">
        <N8nWorkflowBlock />
      </div>
    </div>
  );
}
