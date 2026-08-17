import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

export default function DatasetsPage() {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Datasets</h1>
          <p className="text-muted-foreground mt-2">View, filter, and export generated dataset artifacts.</p>
        </div>
        <Button variant="outline">
          <Download className="mr-2 size-4" />
          Export All
        </Button>
      </div>

      <div className="border rounded-md">
        <div className="p-12 text-center text-muted-foreground flex flex-col items-center justify-center">
          <p>No datasets generated yet.</p>
        </div>
      </div>
    </div>
  );
}
