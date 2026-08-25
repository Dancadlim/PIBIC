import React, { useEffect, useState } from 'react';
import { doc, onSnapshot } from 'firebase/firestore';
import { db } from '@/lib/firebase';
import { X } from 'lucide-react';

export default function AgentDebuggerModal({ salaId, numeroAula, onClose }: { salaId: string, numeroAula: number, onClose: () => void }) {
  const [agentes, setAgentes] = useState<any>({});
  const [logs, setLogs] = useState<{time: string, msg: string, type: string}[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [numSubtopics, setNumSubtopics] = useState<number>(0);

  useEffect(() => {
    if (!salaId || !numeroAula) return;
    const docRef = doc(db, 'classrooms', salaId, 'aulas_debug', String(numeroAula));
    
    const unsubscribe = onSnapshot(docRef, (docSnap) => {
      if (docSnap.exists()) {
        const data = docSnap.data();
        setAgentes(data.agentes || {});
        setLogs(data.logs || []);
        setNumSubtopics(data.num_subtopics || 0);
      }
    });
    return () => unsubscribe();
  }, [salaId, numeroAula]);

  const agentNodes = [
    { id: "gerador_bruto", label: "Gerador de Conte?do" },
    { id: "revisor", label: "Revisor (Cr?tico)" },
    { id: "orquestrador", label: "Orquestrador Editorial" },
    { id: "simulador", label: "Agente Simulador" },
    { id: "exercicios", label: "Agente de Exerc?cios" },
  ];

  const getBorderColor = (status: string) => {
    if (status === "rodando") return "border-yellow-400 bg-yellow-50 text-yellow-700 animate-pulse";
    if (status === "concluido") return "border-green-500 bg-green-50 text-green-700";
    if (status === "erro") return "border-red-500 bg-red-50 text-red-700";
    if (status === "ignorado") return "border-slate-300 bg-slate-100 text-slate-400 opacity-50 cursor-not-allowed";
    return "border-gray-200 bg-white text-gray-400";
  };

  const renderNode = (id: string, label: string) => {
    const state = agentes[id] || { status: "esperando" };
    const isSelected = selectedAgent === id;
    return (
      <button
        key={id}
        onClick={() => setSelectedAgent(id)}
        className={`w-full max-w-sm p-4 rounded-lg border-2 shadow-sm transition-all duration-200 flex flex-col items-center gap-1 ${getBorderColor(state.status)} ${isSelected ? 'ring-4 ring-indigo-200 scale-105' : 'hover:scale-105'} relative z-10`}
      >
        <span className="font-bold text-center text-sm">{label}</span>
        <span className="text-xs font-mono uppercase px-2 py-1 bg-white/50 rounded-full">
          {state.status}
        </span>
      </button>
    );
  };

  return (
    <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-7xl h-[90vh] rounded-xl shadow-2xl flex flex-col overflow-hidden">
        
        {/* HEADER */}
        <div className="bg-slate-900 px-6 py-4 flex justify-between items-center text-white border-b border-slate-700 shrink-0">
          <div>
            <h2 className="text-xl font-bold flex items-center gap-2">
              <span>🤖</span> Debugger Visual de Agentes (Aula {numeroAula})
            </h2>
            <p className="text-slate-400 text-xs mt-1 font-mono">ID: {salaId}</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-slate-700 rounded-full transition">
            <X size={24} />
          </button>
        </div>

        {/* BODY */}
        <div className="flex flex-1 overflow-hidden">
          
          {/* LEFT PANE: Logs */}
          <div className="w-1/3 border-r bg-gray-900 flex flex-col">
            <div className="p-3 border-b border-gray-700 text-gray-300 font-mono text-sm font-semibold tracking-wider">
              &gt; TERMINAL_LOGS
            </div>
            <div className="flex-1 p-4 overflow-y-auto font-mono text-xs text-gray-300 space-y-2 flex flex-col-reverse">
              {[...logs].reverse().map((l, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-gray-500 shrink-0">[{l.time}]</span>
                  <span className={`break-words ${l.type === 'error' ? 'text-red-400' : l.type === 'success' ? 'text-green-400' : 'text-gray-300'}`}>
                    {l.msg}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* CENTER PANE: Flowchart */}
          <div className={`${selectedAgent ? 'w-1/3' : 'w-2/3'} p-6 bg-slate-50 flex flex-col items-center overflow-y-auto transition-all duration-300 relative`}>
            <h3 className="text-sm font-bold text-gray-400 mb-8 uppercase tracking-widest">Pipeline de Geração</h3>
            
                        <div className="flex flex-col items-center relative w-full max-w-lg">
              
              
              
              {renderNode("gerador_bruto", "Roteirista de Aula (Macro)")}
              
              {numSubtopics > 0 && (
                <div className="w-full my-6 flex gap-4 overflow-x-auto pb-4 justify-center">
                  {Array.from({ length: numSubtopics }).map((_, i) => (
                    <div key={i} className="flex flex-col items-center min-w-[200px] border border-slate-200 bg-white p-4 rounded-xl shadow-sm relative">
                      <div className="text-xs font-bold text-slate-400 absolute -top-3 bg-white px-2">SUBT?PICO {i + 1}</div>
                      
                      {renderNode(`gerador_bruto_${i + 1}`, `Gerador ${i + 1}`)}
                      <div className="flex items-center justify-center my-2 h-8">
                         <div className="border-l-2 border-indigo-300 h-full border-dashed flex flex-col items-center justify-center">
                            <span className="bg-indigo-100 text-indigo-700 text-[10px] font-bold px-1 rounded-full relative z-10 ">?</span>
                         </div>
                      </div>
                      {renderNode(`revisor_${i + 1}`, `Revisor ${i + 1}`)}
                    </div>
                  ))}
                </div>
              )}
              
              {numSubtopics === 0 && <div className="h-6 border-l-2 border-dashed border-gray-300 my-1"></div>}
              
              {renderNode("orquestrador", "Orquestrador Editorial")}
              
              <div className="h-6 border-l-2 border-dashed border-gray-300 my-1"></div>
              {renderNode("validador_latex", "Validador LaTeX")}
              
              {/* Branching paths for Parallel Agents */}
              <div className="flex w-full mt-1 relative h-6">
                 {/* Horizontal connecting line */}
                 <div className="absolute top-1/2 left-[25%] right-[25%] border-t-2 border-dashed border-gray-300"></div>
                 {/* Vertical line connecting from Orquestrador to horizontal line */}
                 <div className="absolute top-0 left-1/2 bottom-1/2 border-l-2 border-dashed border-gray-300"></div>
                 {/* Downward connecting lines to left and right nodes */}
                 <div className="absolute top-1/2 left-[25%] bottom-0 border-l-2 border-dashed border-gray-300"></div>
                 <div className="absolute top-1/2 right-[25%] bottom-0 border-r-2 border-dashed border-gray-300"></div>
              </div>
              
              <div className="flex w-full justify-between gap-4 mt-1">
                 <div className="flex-1 flex flex-col items-center">
                    {renderNode("simulador", "Agente Simulador")}
                 </div>
                 <div className="flex-1 flex flex-col items-center">
                    {renderNode("exercicios", "Agente de Exerc?cios")}
                 </div>
              </div>

            </div>
            </div>

            {/* RIGHT PANE: Prompt/Response Inspector */}
          {selectedAgent && (
            <div className="w-1/3 bg-white border-l shadow-xl flex flex-col animate-in slide-in-from-right-8">
              <div className="p-4 border-b bg-indigo-50 flex justify-between items-center">
                <h3 className="font-bold text-indigo-900">
                  Inspetor: {selectedAgent}
                </h3>
                <button onClick={() => setSelectedAgent(null)} className="text-indigo-400 hover:text-indigo-700">
                  <X size={18} />
                </button>
              </div>
              
              <div className="flex-1 overflow-y-auto p-4 space-y-6">
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase mb-2">Prompt Enviado</h4>
                  <div className="bg-slate-900 text-green-400 p-3 rounded-lg text-[10px] font-mono whitespace-pre-wrap overflow-x-auto">
                    {agentes[selectedAgent]?.prompt || "Nenhum prompt registrado ainda..."}
                  </div>
                </div>
                
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase mb-2">Resposta Bruta (JSON/Markdown)</h4>
                  <div className="bg-slate-100 text-slate-800 p-3 rounded-lg text-[10px] font-mono whitespace-pre-wrap border overflow-x-auto">
                    {agentes[selectedAgent]?.resposta || "Nenhuma resposta recebida ainda..."}
                  </div>
                </div>

                {agentes[selectedAgent]?.loop_data && (
                  <div>
                    <h4 className="text-xs font-bold text-purple-500 uppercase mb-2">Histórico de Ciclos (Revisor)</h4>
                    <div className="space-y-2">
                      {agentes[selectedAgent].loop_data.map((ciclo: any, idx: number) => (
                        <div key={idx} className="p-2 border border-purple-200 bg-purple-50 rounded text-xs">
                          <span className="font-bold text-purple-700">Ciclo {idx + 1}: </span> 
                          {ciclo.critica}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
          
        </div>
      </div>
    </div>
  );
}
