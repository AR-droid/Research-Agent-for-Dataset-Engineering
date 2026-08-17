"use client";

import { useState, useRef, useEffect } from "react";
import { Loader2 } from "lucide-react";

type Stage = 1 | 2 | 3;

export default function WorkspaceView() {
  const [stage, setStage] = useState<Stage>(1);
  const [objective, setObjective] = useState("");
  
  // Logs and Results
  const [logs, setLogs] = useState<{stage: string, message: string}[]>([]);
  const [results, setResults] = useState<{sources: any[], content_snippet: string} | null>(null);
  const [plan, setPlan] = useState<any>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  useEffect(() => {
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const startRun = () => {
    if (!objective.trim()) return;
    
    setStage(2);
    setLogs([]);
    setResults(null);
    setPlan(null);
    
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/v1/demo-run`;
    
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({ objective }));
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "LOG") {
          setLogs(p => [...p, { stage: data.stage, message: data.message }]);
        } else if (data.type === "PLAN") {
          setPlan(data.data);
        } else if (data.type === "RESULTS") {
          setResults({ sources: data.sources, content_snippet: data.content_snippet });
          setStage(3);
        } else if (data.type === "ERROR") {
          setLogs(p => [...p, { stage: "ERR", message: `ERROR: ${data.message}` }]);
        }
      } catch (e) {
        console.error(e);
      }
    };

    ws.onclose = () => {
      if (stage !== 3) {
        setLogs(p => [...p, { stage: "SYS", message: "Connection closed." }]);
      }
    };
  };

  return (
    <div className="flex h-screen w-full bg-white text-black font-sans selection:bg-black selection:text-white">
      {/* Left Sidebar Layout (from reference) */}
      <div className="w-[300px] border-r border-[#EAEAEA] flex flex-col p-8 shrink-0">
        <div className="mb-12">
          <div className="flex items-center gap-2 mb-6">
            <div className="w-8 h-8 rounded-full border border-black flex items-center justify-center">
              <div className="w-4 h-4 rounded-full border border-black" />
            </div>
          </div>
          <h1 className="text-2xl font-bold tracking-tight mb-2">ARES-101</h1>
          <p className="text-sm text-gray-500 leading-relaxed">
            Input a research objective. Our agents will autonomously plan, scrape, and synthesize the data.
          </p>
        </div>

        <div className="space-y-8 flex-1">
          {/* Stage 1 Indicator */}
          <div className={`relative pl-4 border-l-2 ${stage >= 1 ? 'border-black' : 'border-transparent'}`}>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-1">STAGE 01</div>
            <div className={`text-sm font-medium ${stage >= 1 ? 'text-black' : 'text-gray-400'}`}>Objective</div>
            <div className="text-xs text-gray-400 mt-1">{stage > 1 ? 'done ✓' : 'pending'}</div>
          </div>

          {/* Stage 2 Indicator */}
          <div className={`relative pl-4 border-l-2 ${stage >= 2 ? 'border-black' : 'border-transparent'}`}>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-1">STAGE 02</div>
            <div className={`text-sm font-medium ${stage >= 2 ? 'text-black' : 'text-gray-400'}`}>Research</div>
            <div className="text-xs text-gray-400 mt-1">{stage > 2 ? 'done ✓' : stage === 2 ? 'running...' : 'pending'}</div>
          </div>

          {/* Stage 3 Indicator */}
          <div className={`relative pl-4 border-l-2 ${stage >= 3 ? 'border-black' : 'border-transparent'}`}>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-1">STAGE 03</div>
            <div className={`text-sm font-medium ${stage >= 3 ? 'text-black' : 'text-gray-400'}`}>Response</div>
            <div className="text-xs text-gray-400 mt-1">{stage === 3 ? 'done ✓' : 'pending'}</div>
          </div>
        </div>

        <div className="text-xs text-gray-400 font-mono mt-auto pt-8 border-t border-[#EAEAEA]">
          ● 127.0.0.1:8000
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-12 lg:p-24 bg-[#FAFAFA]">
        <div className="max-w-3xl mx-auto space-y-24">
          
          {/* Stage 1 Section */}
          <section className={stage > 1 ? 'opacity-50 pointer-events-none' : ''}>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-4">STAGE 01</div>
            <h2 className="text-2xl font-bold mb-2">Research Objective</h2>
            <p className="text-sm text-gray-500 mb-8 max-w-xl leading-relaxed">
              Define the topic you want ARES to investigate. The agents will break this down into a multi-step research plan.
            </p>
            
            <div className="bg-[#F4F4F4] p-8 border border-[#EAEAEA] rounded-none">
              <textarea 
                className="w-full bg-transparent border-none outline-none resize-none text-sm placeholder:text-gray-400 min-h-[100px]"
                placeholder="e.g. What is the latest scientific consensus on the LK-99 room temperature superconductor claims in 2024?"
                value={objective}
                onChange={(e) => setObjective(e.target.value)}
                disabled={stage > 1}
              />
            </div>
            
            <div className="mt-6 flex items-center gap-4">
              <button 
                onClick={startRun}
                disabled={stage > 1 || !objective.trim()}
                className="bg-black text-white px-8 py-3 text-xs font-bold tracking-widest uppercase hover:bg-gray-800 disabled:opacity-50 transition-colors"
              >
                START
              </button>
              {stage > 1 && <span className="text-xs text-gray-500">✓ Objective submitted successfully</span>}
            </div>
          </section>

          {/* Stage 2 Section */}
          {(stage >= 2) && (
            <section className={stage > 2 ? 'opacity-50' : ''}>
              <div className="text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-4">STAGE 02</div>
              <h2 className="text-2xl font-bold mb-2">Agent Execution</h2>
              <p className="text-sm text-gray-500 mb-8 max-w-xl leading-relaxed">
                Live trace of the LangChain orchestrator routing tasks between Planner, Discovery, and Analyst agents.
              </p>
              
              <div className="bg-[#111111] text-[#00FF00] p-6 border border-black rounded-none min-h-[250px] font-mono text-xs overflow-y-auto max-h-[400px]">
                {logs.map((l, i) => (
                  <div key={i} className="mb-2 leading-relaxed">
                    <span className="text-gray-500 mr-4">[{l.stage}]</span>
                    {l.message}
                  </div>
                ))}
                {stage === 2 && (
                  <div className="flex items-center gap-2 mt-4 text-gray-500 animate-pulse">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>Agent is thinking...</span>
                  </div>
                )}
                <div ref={logsEndRef} />
              </div>
            </section>
          )}

          {/* Stage 3 Section */}
          {stage === 3 && results && (
            <section className="animate-in fade-in slide-in-from-bottom-8 duration-700">
              <div className="text-[10px] uppercase tracking-wider text-gray-500 font-semibold mb-4">STAGE 03</div>
              <h2 className="text-2xl font-bold mb-2">Research Results</h2>
              <p className="text-sm text-gray-500 mb-8 max-w-xl leading-relaxed">
                The extracted evidence and raw data snippets acquired from the open web.
              </p>
              
              <div className="space-y-8">
                {results.sources && results.sources.length > 0 && (
                  <div>
                    <h3 className="text-sm font-bold uppercase tracking-wider mb-4 border-b pb-2">Discovered Sources</h3>
                    <div className="grid gap-4">
                      {results.sources.map((s, i) => (
                        <a key={i} href={s.url} target="_blank" rel="noreferrer" className="block p-4 border border-[#EAEAEA] hover:border-black transition-colors bg-white group">
                          <div className="text-sm font-bold group-hover:underline">{s.title}</div>
                          <div className="text-xs text-gray-400 mt-1 truncate">{s.url}</div>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
                
                <div>
                  <h3 className="text-sm font-bold uppercase tracking-wider mb-4 border-b pb-2">Extracted Snippet</h3>
                  <div className="bg-white p-6 border border-[#EAEAEA] text-sm text-gray-700 leading-relaxed font-serif whitespace-pre-wrap">
                    {results.content_snippet}...
                  </div>
                </div>
              </div>
              
              <div className="mt-12">
                <button 
                  onClick={() => { setStage(1); setObjective(""); setLogs([]); setResults(null); }}
                  className="bg-black text-white px-8 py-3 text-xs font-bold tracking-widest uppercase hover:bg-gray-800 transition-colors"
                >
                  START NEW RESEARCH
                </button>
              </div>
            </section>
          )}

        </div>
      </div>
    </div>
  );
}
