"use client";

import { useState, useEffect, useRef } from "react";
import { 
  Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle
} from "@/components/ui/dialog";
import { 
  Play, Loader2, Database, FileText, Search, Activity, CheckCircle2, ChevronRight, AlertCircle
} from "lucide-react";
import { toast } from "sonner";

const PROJECT_ID = "proj_01J0X";

type AgentStatus = 'IDLE' | 'STARTING' | 'RUNNING' | 'REQUIRES_REVIEW' | 'COMPLETED' | 'FAILED';

export default function WorkspaceView() {
  const [objective, setObjective] = useState("");
  const [status, setStatus] = useState<AgentStatus>('IDLE');
  const [currentAgent, setCurrentAgent] = useState<string>("Planner");
  const [logs, setLogs] = useState<{timestamp: string, message: string, agent: string}[]>([]);
  
  const [sources, setSources] = useState<Record<string, unknown>[]>([]);
  const [evidence, setEvidence] = useState<Record<string, unknown>[]>([]);
  const [records, setRecords] = useState<Record<string, unknown>[]>([]);
  
  // Custom Tabs state
  const [activeTab, setActiveTab] = useState<'sources' | 'evidence' | 'records'>('records');

  // Review state
  const [reviewType, setReviewType] = useState<'SCHEMA' | 'PLAN' | null>(null);
  const [reviewData, setReviewData] = useState<Record<string, unknown> | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const fetchStateRest = async (rId: string) => {
    try {
      const res = await fetch(`/api/v1/projects/${PROJECT_ID}/runs/${rId}`);
      if (res.ok) {
        const data = await res.json();
        setStatus(data.status);
        setCurrentAgent(data.currentAgent || "Planner");
      }
    } catch (e) {
      console.error("REST fallback failed", e);
    }
  };

  const connectWebSocket = (rId: string) => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/v1/websockets/runs/${rId}`;
    
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("Connected to run execution stream");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'LOG') {
          setLogs(prev => [...prev, {
            timestamp: new Date().toLocaleTimeString(),
            message: data.message,
            agent: data.agent || currentAgent
          }]);
        } else if (data.type === 'STATUS_UPDATE') {
          setStatus(data.status);
          if (data.currentAgent) setCurrentAgent(data.currentAgent);
        } else if (data.type === 'REVIEW_REQUIRED') {
          setStatus('REQUIRES_REVIEW');
          setReviewType(data.reviewType);
          setReviewData(data.reviewData);
        } else if (data.type === 'DATA_ACQUIRED') {
          if (data.dataType === 'SOURCE') setSources(prev => [...prev, data.payload]);
          if (data.dataType === 'EVIDENCE') setEvidence(prev => [...prev, data.payload]);
          if (data.dataType === 'RECORD') setRecords(prev => [...prev, data.payload]);
        }
      } catch (e) {
        console.error("Failed to parse WS message", e);
      }
    };

    ws.onclose = () => {
      console.log("WS closed. Fallback to polling...");
      if (status === 'RUNNING') {
        setTimeout(() => fetchStateRest(rId), 3000);
      }
    };
  };

  const startRun = async () => {
    if (!objective.trim()) {
      toast.error("Please enter a research objective.");
      return;
    }

    setStatus('STARTING');
    setLogs([{ timestamp: new Date().toLocaleTimeString(), message: "Initializing research run...", agent: "System" }]);
    
    try {
      const res = await fetch(`/api/v1/projects/${PROJECT_ID}/runs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ objective })
      });
      
      if (!res.ok) throw new Error("API failed");
      
      const data = await res.json();
      setRunId(data.id);
      setStatus('RUNNING');
      toast.success("Research run started");
      connectWebSocket(data.id);
    } catch (error) {
      console.error(error);
      setStatus('RUNNING');
      toast.success("Run started (Mocked Fallback)");
      startMockExecutionStream();
    }
  };
  
  const startMockExecutionStream = () => {
    let step = 0;
    const interval = setInterval(() => {
      step++;
      const now = new Date().toLocaleTimeString();
      
      if (step === 1) {
        setLogs(p => [...p, { timestamp: now, message: "Analyzing objective to formulate research plan", agent: "Planner" }]);
      } else if (step === 3) {
        setLogs(p => [...p, { timestamp: now, message: "Research plan formulated.", agent: "Planner" }]);
        setStatus('REQUIRES_REVIEW');
        setReviewType('PLAN');
        setReviewData({
          title: "Comprehensive Research Plan",
          steps: ["1. Initial Querying", "2. Data Scraping", "3. Synthesis"]
        });
        clearInterval(interval);
      } else if (step === 4) {
        setCurrentAgent("Discovery");
        setLogs(p => [...p, { timestamp: now, message: "Starting web discovery...", agent: "Discovery" }]);
      } else if (step === 6) {
        setSources(p => [...p, { id: 1, title: "Dataset Engineering Guide", url: "https://example.com" }]);
        setLogs(p => [...p, { timestamp: now, message: "Found relevant source: Dataset Engineering Guide", agent: "Discovery" }]);
      } else if (step === 8) {
        setCurrentAgent("Analyst");
        setLogs(p => [...p, { timestamp: now, message: "Extracting evidence from sources...", agent: "Analyst" }]);
        setEvidence(p => [...p, { id: 1, text: "High quality data requires iterative cleaning." }]);
      } else if (step === 10) {
        setStatus('REQUIRES_REVIEW');
        setReviewType('SCHEMA');
        setReviewData({
          fields: [
            { name: "instruction", type: "string" },
            { name: "output", type: "string" }
          ]
        });
        clearInterval(interval);
      } else if (step === 11) {
        setRecords(p => [...p, { id: 1, instruction: "Explain data cleaning", output: "Data cleaning is the process..." }]);
        setLogs(p => [...p, { timestamp: now, message: "Generated 1 dataset record.", agent: "Analyst" }]);
      } else if (step === 12) {
        setStatus('COMPLETED');
        setLogs(p => [...p, { timestamp: now, message: "Research run completed successfully.", agent: "System" }]);
        clearInterval(interval);
      }
    }, 2000);
    
    (window as unknown as Record<string, unknown>).mockInterval = interval;
  };
  
  const handleApprove = async () => {
    setStatus('RUNNING');
    setReviewType(null);
    setReviewData(null);
    setLogs(p => [...p, { timestamp: new Date().toLocaleTimeString(), message: `${reviewType} approved by human. Resuming...`, agent: "System" }]);
    toast.success("Approved successfully");
    startMockExecutionStream();
  };

  const handleReject = async () => {
    setStatus('IDLE');
    setReviewType(null);
    setReviewData(null);
    setLogs(p => [...p, { timestamp: new Date().toLocaleTimeString(), message: `${reviewType} rejected by human. Halting...`, agent: "System" }]);
    toast.error("Review rejected");
  };

  const progressValue = status === 'COMPLETED' ? 100 : currentAgent === 'Planner' ? 33 : currentAgent === 'Discovery' ? 66 : 90;

  return (
    <div className="flex flex-col h-full gap-6 p-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Research Workspace</h1>
          <p className="text-muted-foreground mt-2">Design, execute, and monitor agentic dataset creation.</p>
        </div>
        {status !== 'IDLE' && (
          <Badge variant={status === 'RUNNING' ? 'default' : status === 'REQUIRES_REVIEW' ? 'destructive' : 'secondary'} className="text-sm px-3 py-1">
            {status === 'RUNNING' && <Loader2 className="w-3 h-3 mr-2 animate-spin inline" />}
            {status.replace('_', ' ')}
          </Badge>
        )}
      </div>

      {status === 'IDLE' ? (
        <Card className="border-2 border-dashed shadow-sm">
          <CardHeader>
            <CardTitle>Start New Research Run</CardTitle>
            <CardDescription>Enter your objective to kick off the autonomous research agents.</CardDescription>
          </CardHeader>
          <CardContent>
            <textarea 
              placeholder="e.g., Build a dataset of 50 high-quality reasoning traces for medical diagnosis tasks..."
              className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50 resize-none"
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
            />
          </CardContent>
          <CardFooter className="flex justify-end">
            <Button onClick={startRun} className="bg-primary text-primary-foreground hover:bg-primary/90">
              <Play className="w-4 h-4 mr-2" />
              Launch Agents
            </Button>
          </CardFooter>
        </Card>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 flex-1 min-h-0">
          
          <Card className="xl:col-span-1 flex flex-col shadow-sm border-border overflow-hidden">
            <CardHeader className="bg-secondary/50 border-b pb-4">
              <CardTitle className="flex items-center text-lg">
                <Activity className="w-5 h-5 mr-2 text-primary" />
                Live Execution
              </CardTitle>
              <div className="flex items-center gap-2 mt-4 text-sm font-medium">
                <span className={currentAgent === 'Planner' ? 'text-primary' : 'text-muted-foreground'}>Planner</span>
                <ChevronRight className="w-4 h-4 text-muted-foreground" />
                <span className={currentAgent === 'Discovery' ? 'text-primary' : 'text-muted-foreground'}>Discovery</span>
                <ChevronRight className="w-4 h-4 text-muted-foreground" />
                <span className={currentAgent === 'Analyst' ? 'text-primary' : 'text-muted-foreground'}>Analyst</span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-muted mt-4">
                <div className="h-full bg-primary transition-all duration-500 ease-in-out" style={{ width: `${progressValue}%` }} />
              </div>
            </CardHeader>
            <CardContent className="flex-1 p-0 overflow-hidden relative">
              <div className="h-full max-h-[500px] xl:max-h-[calc(100vh-300px)] overflow-y-auto p-4 space-y-4" ref={scrollRef}>
                {logs.map((log, i) => (
                  <div key={i} className="flex flex-col gap-1 text-sm border-b pb-3 last:border-0">
                    <div className="flex items-center justify-between text-muted-foreground text-xs">
                      <span className="font-medium text-foreground">{log.agent}</span>
                      <span>{log.timestamp}</span>
                    </div>
                    <p className="font-mono text-xs text-foreground/80 leading-relaxed">{log.message}</p>
                  </div>
                ))}
                {status === 'RUNNING' && (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground animate-pulse pt-2">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    Agent thinking...
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card className="xl:col-span-2 flex flex-col shadow-sm border-border overflow-hidden">
            <CardHeader className="bg-secondary/50 border-b pb-0 pt-4 px-4">
              <div className="flex justify-between items-center mb-0">
                <CardTitle className="text-lg flex items-center mb-4">
                  <Database className="w-5 h-5 mr-2 text-primary" />
                  Data Inspection
                </CardTitle>
              </div>
              <div className="flex items-center gap-1 bg-muted p-1 rounded-t-lg">
                <button
                  onClick={() => setActiveTab('sources')}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${activeTab === 'sources' ? 'bg-background text-foreground shadow' : 'text-muted-foreground hover:bg-background/50'}`}
                >
                  <Search className="w-4 h-4 mr-2" /> Sources ({sources.length})
                </button>
                <button
                  onClick={() => setActiveTab('evidence')}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${activeTab === 'evidence' ? 'bg-background text-foreground shadow' : 'text-muted-foreground hover:bg-background/50'}`}
                >
                  <FileText className="w-4 h-4 mr-2" /> Evidence ({evidence.length})
                </button>
                <button
                  onClick={() => setActiveTab('records')}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${activeTab === 'records' ? 'bg-background text-foreground shadow' : 'text-muted-foreground hover:bg-background/50'}`}
                >
                  <Database className="w-4 h-4 mr-2" /> Records ({records.length})
                </button>
              </div>
            </CardHeader>
            <CardContent className="p-0 flex-1 overflow-hidden bg-background">
              <div className="h-full max-h-[500px] xl:max-h-[calc(100vh-320px)] overflow-y-auto p-4">
                {activeTab === 'sources' && (
                  sources.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-muted-foreground min-h-[200px]">
                      <Search className="w-8 h-8 mb-2 opacity-20" />
                      <p>No sources acquired yet.</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {sources.map((s, i) => (
                        <div key={i} className="p-3 bg-card border rounded-md shadow-sm">
                          <h4 className="font-semibold text-sm">{s.title}</h4>
                          <a href={s.url} target="_blank" rel="noreferrer" className="text-xs text-blue-500 hover:underline">{s.url}</a>
                        </div>
                      ))}
                    </div>
                  )
                )}

                {activeTab === 'evidence' && (
                  evidence.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-muted-foreground min-h-[200px]">
                      <FileText className="w-8 h-8 mb-2 opacity-20" />
                      <p>No evidence extracted yet.</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {evidence.map((e, i) => (
                        <div key={i} className="p-3 bg-card border rounded-md shadow-sm text-sm">
                          {e.text}
                        </div>
                      ))}
                    </div>
                  )
                )}

                {activeTab === 'records' && (
                  records.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-muted-foreground min-h-[200px]">
                      <Database className="w-8 h-8 mb-2 opacity-20" />
                      <p>No records generated yet.</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {records.map((r, i) => (
                        <div key={i} className="p-4 bg-card border rounded-md shadow-sm space-y-2">
                          {Object.entries(r).filter(([k]) => k !== 'id').map(([k, v]) => (
                            <div key={k}>
                              <span className="text-xs font-semibold text-muted-foreground uppercase">{k}</span>
                              <p className="text-sm mt-1 bg-secondary/30 p-2 rounded">{String(v)}</p>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  )
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <Dialog open={status === 'REQUIRES_REVIEW'} onOpenChange={(open) => {
        if (!open && status === 'REQUIRES_REVIEW') {
          toast.info("Review is required to proceed.");
        }
      }}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center text-xl">
              <AlertCircle className="w-5 h-5 mr-2 text-destructive" />
              Human Review Required: {reviewType === 'SCHEMA' ? 'Dataset Schema' : 'Research Plan'}
            </DialogTitle>
            <DialogDescription>
              The agent has paused execution and requested human approval before proceeding.
            </DialogDescription>
          </DialogHeader>
          
          <div className="bg-secondary/20 p-4 rounded-md border min-h-[200px] mt-4">
            {reviewType === 'PLAN' && reviewData && (
              <div>
                <h3 className="font-bold mb-2">{reviewData.title}</h3>
                <ul className="space-y-2">
                  {reviewData.steps?.map((step: string, i: number) => (
                    <li key={i} className="flex items-start">
                      <CheckCircle2 className="w-4 h-4 mr-2 text-primary mt-0.5" />
                      <span className="text-sm">{step}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {reviewType === 'SCHEMA' && reviewData && (
              <div>
                <h3 className="font-bold mb-3">Proposed Schema Definition</h3>
                <div className="grid gap-3">
                  {reviewData.fields && Array.isArray(reviewData.fields) && reviewData.fields.map((field: Record<string, unknown>, i: number) => (
                    <div key={i} className="flex justify-between items-center p-2 bg-background border rounded">
                      <span className="font-mono text-sm font-semibold">{field.name}</span>
                      <Badge variant="outline">{field.type}</Badge>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          <DialogFooter className="mt-6 flex sm:justify-between">
            <Button variant="outline" onClick={handleReject} className="border-destructive text-destructive hover:bg-destructive/10">
              Reject & Modify
            </Button>
            <Button onClick={handleApprove} className="bg-primary text-primary-foreground hover:bg-primary/90">
              Approve & Continue
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
