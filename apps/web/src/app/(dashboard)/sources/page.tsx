import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export default function SourcesPage() {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Sources</h1>
          <p className="text-muted-foreground mt-2">Manage documents, URLs, and databases for extraction.</p>
        </div>
        <Button>
          <Plus className="mr-2 size-4" />
          Add Source
        </Button>
      </div>

      <div className="border rounded-md">
        <div className="p-12 text-center text-muted-foreground flex flex-col items-center justify-center">
          <p>No sources added yet.</p>
        </div>
      </div>
    </div>
  );
}
