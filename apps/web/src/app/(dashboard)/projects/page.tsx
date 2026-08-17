import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus } from "lucide-react";

export default function ProjectsPage() {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Projects</h1>
          <p className="text-muted-foreground mt-2">Manage your research projects and workspaces.</p>
        </div>
        <Button>
          <Plus className="mr-2 size-4" />
          New Project
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>AI Safety Alignment</CardTitle>
            <CardDescription>Analyzing policy documents and papers</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-muted-foreground">Updated 2 days ago</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Climate Tech Market</CardTitle>
            <CardDescription>Synthesizing market reports and data</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-muted-foreground">Updated 5 days ago</div>
          </CardContent>
        </Card>
        
        <Card className="flex flex-col items-center justify-center border-dashed cursor-pointer hover:bg-muted/50 transition-colors">
          <CardContent className="flex flex-col items-center pt-6 pb-6 text-center">
            <Plus className="size-8 text-muted-foreground mb-4" />
            <h3 className="font-semibold text-lg">Create New Project</h3>
            <p className="text-sm text-muted-foreground mt-2">Start a new research workspace</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
