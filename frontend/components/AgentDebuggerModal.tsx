"use client";

import { useState, useEffect } from "react";
import { doc, onSnapshot } from "firebase/firestore";
import { db } from "@/lib/firebase";

export default function AgentDebuggerModal({ salaId, numeroAula, onClose }) {
  const [debugData, setDebugData] = useState(null);
  const [selectedAgent, setSelectedAgent] = useState(null);

  useEffect(() => {
    if (!salaId || !numeroAula) return;
    const docRef = doc(db, "classrooms", salaId, "aulas_debug", String(numeroAula));
    const unsubscribe = onSnapshot(docRef, (docSnap) => {
      if (docSnap.exists()) {
        setDebugData(docSnap.data());
      }
    });
    return () => unsubscribe();
  }, [salaId, numeroAula]);

  if (!debugData) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div className="bg-white p-6 rounded-lg shadow-xl">
          <p className="text-gray-600">Conectando ao terminal de agentes...</p>
          <button onClick={onClose} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Fechar</button>
        </div>
      </div>
    );
  }

  const { logs = [], agentes = {} } = debugData;

  const agentNodes = [
    { id: "gerador_bruto", label: "1. Gerador Bruto" },
    { id: "orquestrador", label: "2. Orquestrador Editorial" },
    { id: "revisor", label: "3. Revisor de Nota??o" },
    { id: "exercicios", label: "4. Agente Exerc?cios" },
    { id: "simulador", label: "5. Agente Simulador" },
  ];

  const getStatusColor = (status) => {
    switch(status) {
      case "esperando": return "bg-gray-200 border-gray-300 text-gray-500";
      case "rodando": return "bg-yellow-100 border-yellow-400 text-yellow-700 animate-pulse";
      case "concluido": return "bg-green-100 border-green-500 text-green-700";
      case "erro": return "bg-red-100 border-red-500 text-red-700";
      default: return "bg-gray-100 border-gray-300";
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-md p-4">
      <div className="bg-white w-full max-w-7xl h-[90vh] rounded-xl shadow-2xl flex flex-col overflow-hidden">
        {/* HEADER */}
        <div className="flex items-center justify-between px-6 py-4 border-b bg-gray-50">
          <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span className="text-2xl">??</span> Debugger Visual de Agentes (Aula {numeroAula})
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-red-500 transition-colors">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        {/* BODY */}
        <div className="flex flex-1 overflow-hidden">
          
          {/* LEFT PANE: Logs */}
          <div className="w-1/3 border-r bg-gray-900 flex flex-col">
            <div className="p-3 border-b border-gray-700 text-gray-300 font-mono text-sm font-semibold tracking-wider">
              > TERMINAL_LOGS
            </div>
            <div className="flex-1 p-4 overflow-y-auto font-mono text-xs text-gray-300 space-y-2 flex flex-col-reverse">
              {[...logs].reverse().map((l, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-gray-500 shrink-0">[{l.time}]</span>
                  <span className={ + "reak-words " + }>
                    {l.msg}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* CENTER PANE: Flowchart */}
          <div className={ + "${selectedAgent ? 'w-1/3' : 'w-2/3'}" +  p-6 bg-slate-50 flex flex-col items-center overflow-y-auto transition-all duration-300 relative}>
            <h3 className="text-sm font-bold text-gray-400 mb-8 uppercase tracking-widest">Pipeline de Gera??o</h3>
            
            <div className="flex flex-col items-center gap-6 relative w-full max-w-sm">
              {agentNodes.map((node, i) => {
                const state = agentes[node.id] || { status: "esperando" };
                const isSelected = selectedAgent === node.id;
                
                return (
                  <div key={node.id} className="w-full flex flex-col items-center relative z-10">
                    <button
                      onClick={() => setSelectedAgent(node.id)}
                      className={ + "w-full p-4 rounded-lg border-2 shadow-sm transition-all duration-200 flex flex-col items-center gap-1  " + }
                    >
                      <span className="font-bold">{node.label}</span>
                      <span className="text-xs font-mono uppercase px-2 py-1 bg-white/50 rounded-full">
                        {state.status}
                      </span>
                    </button>
                    {/* Arrow to next node */}
                    {i < agentNodes.length - 1 && (
                      <div className="h-6 border-l-2 border-dashed border-gray-300 my-1"></div>
                    )}
                  </div>
                );
              })}
              
              {/* Loop arrow for Revisor -> Orquestrador */}
              <div className="absolute left-[-20px] top-[150px] bottom-[280px] w-8 border-l-2 border-y-2 border-dashed border-purple-400 rounded-l-xl z-0 pointer-events-none opacity-50 flex items-center">
                <span className="absolute -left-16 text-[10px] font-bold text-purple-500 -rotate-90">LOOP DE REVIS?O</span>
              </div>
            </div>
          </div>

          {/* RIGHT PANE: Details (Conditionally rendered) */}
          {selectedAgent && (
            <div className="w-1/3 bg-white border-l flex flex-col">
              <div className="p-4 border-b bg-blue-50 flex justify-between items-center">
                <h3 className="font-bold text-blue-900">
                  Detalhes: {agentNodes.find(n => n.id === selectedAgent)?.label}
                </h3>
                <button onClick={() => setSelectedAgent(null)} className="text-blue-500 hover:text-blue-700 text-sm font-semibold">Fechar</button>
              </div>
              
              <div className="flex-1 overflow-y-auto p-4 space-y-6">
                
                {agentes[selectedAgent]?.prompt && (
                  <div>
                    <h4 className="text-xs font-bold text-gray-500 uppercase mb-2">Prompt Enviado</h4>
                    <pre className="bg-gray-100 p-3 rounded text-xs font-mono text-gray-800 whitespace-pre-wrap border overflow-x-auto">
                      {agentes[selectedAgent].prompt}
                    </pre>
                  </div>
                )}

                {agentes[selectedAgent]?.resposta && (
                  <div>
                    <h4 className="text-xs font-bold text-gray-500 uppercase mb-2">Resposta da IA</h4>
                    <pre className="bg-green-50 p-3 rounded text-xs font-mono text-green-900 whitespace-pre-wrap border border-green-200 overflow-x-auto">
                      {agentes[selectedAgent].resposta}
                    </pre>
                  </div>
                )}
                
                {/* Specific logic for Revisor loops */}
                {agentes[selectedAgent]?.loops && agentes[selectedAgent].loops.length > 0 && (
                  <div className="space-y-4">
                    <h4 className="text-xs font-bold text-purple-600 uppercase">Ciclos de Auditoria ({agentes[selectedAgent].loops.length})</h4>
                    {agentes[selectedAgent].loops.map((loop, idx) => (
                      <div key={idx} className="border border-purple-200 rounded overflow-hidden">
                        <div className="bg-purple-100 px-3 py-1 text-xs font-bold text-purple-800">Ciclo {idx + 1}</div>
                        <div className="p-2 bg-gray-50">
                          <p className="text-[10px] font-bold text-gray-500">PROMPT DO REVISOR:</p>
                          <pre className="text-[10px] whitespace-pre-wrap overflow-x-auto text-gray-700 mt-1">{loop.prompt}</pre>
                          <p className="text-[10px] font-bold text-gray-500 mt-2">RESPOSTA DO REVISOR:</p>
                          <pre className="text-[10px] whitespace-pre-wrap overflow-x-auto text-green-700 mt-1">{loop.resposta}</pre>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {!agentes[selectedAgent]?.prompt && (!agentes[selectedAgent]?.loops || agentes[selectedAgent].loops.length === 0) && (
                  <p className="text-gray-400 text-sm italic text-center mt-10">Agente ainda n?o foi acionado ou dados n?o registrados.</p>
                )}
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
