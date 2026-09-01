"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { doc, onSnapshot, collection, getDocs } from "firebase/firestore";
import { db, auth } from "@/lib/firebase";
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { Menu, X, Play, RefreshCw } from 'lucide-react';
import { sanitizeLatex } from '@/app/utils/latexSanitizer';

function SimuladorInterativo({ temaAula, nomeSimulador, htmlCode }: { temaAula: string, nomeSimulador: string, htmlCode?: string }) {
  const [html, setHtml] = useState<string | null>(htmlCode || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [iframeHeight, setIframeHeight] = useState(800);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data && event.data.type === 'resize' && event.data.height) {
         setIframeHeight(event.data.height + 50);
      }
    };
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const carregarSimulador = async () => {
    setLoading(true);
    setError(false);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/gerar_simulador`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tema_aula: temaAula, nome_simulador: nomeSimulador })
      });
      if (!res.ok) throw new Error("Erro na API");
      const data = await res.json();
      setHtml(data.html_code);
    } catch (e) {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (!html && !loading && !error) {
    return (
      <div className="my-8 bg-indigo-50 border border-indigo-100 rounded-xl p-8 text-center shadow-sm">
        <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Play className="text-indigo-600" size={32} />
        </div>
        <h4 className="text-xl font-bold text-indigo-900 mb-2">Simulador: {nomeSimulador}</h4>
        <p className="text-indigo-700 mb-6 max-w-md mx-auto">
          Acesse uma experiência visual interativa gerada por Inteligência Artificial em tempo real para consolidar este conceito.
        </p>
        <button 
          onClick={carregarSimulador}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-bold shadow-md transition-all flex items-center gap-2 mx-auto"
        >
          <span>✨</span> Gerar e Abrir Simulador
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="my-8 bg-slate-50 border border-slate-200 rounded-xl p-12 text-center shadow-inner">
        <RefreshCw className="animate-spin text-indigo-500 mx-auto mb-4" size={32} />
        <p className="text-slate-600 font-medium animate-pulse">Engenheiro de IA programando o simulador...</p>
        <p className="text-slate-400 text-sm mt-2">Isso pode levar até 20 segundos (código sendo escrito do zero)</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="my-8 bg-red-50 text-red-600 p-6 rounded-xl border border-red-200 text-center">
        <p>Ocorreu um erro ao gerar a simulação.</p>
        <button onClick={carregarSimulador} className="mt-4 underline text-red-800">Tentar Novamente</button>
      </div>
    );
  }

  const injectedHtml = html ? (() => {
    const fallbackAndResizeScript = `<script>
      (function() {
        let lastHeight = 0;
        function notifyParent() {
          const contentDiv = document.querySelector('.max-w-4xl') || document.querySelector('.max-w-5xl') || document.body;
          const h = Math.max(contentDiv ? contentDiv.scrollHeight + 30 : document.body.scrollHeight, 650);
          if (Math.abs(h - lastHeight) > 15) {
            lastHeight = h;
            window.parent.postMessage({ type: 'resize', height: h }, '*');
          }
        }
        window.addEventListener('load', notifyParent);
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
          notifyParent();
        }
        setTimeout(notifyParent, 400);
        setTimeout(notifyParent, 1200);

        // Fallback: garante que se os sliders dispararem ou se o Plotly demorou a carregar, o gráfico renderize
        function ensurePlotRendered() {
          if (typeof Plotly !== 'undefined') {
            const sliders = document.querySelectorAll('input[type="range"]');
            if (sliders.length > 0) {
              sliders[0].dispatchEvent(new Event('input', { bubbles: true }));
            }
          } else {
            setTimeout(ensurePlotRendered, 150);
          }
        }
        setTimeout(ensurePlotRendered, 300);
        setTimeout(ensurePlotRendered, 1000);
      })();
    </script>`;
    if (html.includes('</body>')) {
      return html.replace('</body>', `${fallbackAndResizeScript}</body>`);
    }
    return html + fallbackAndResizeScript;
  })() : null;

  return (
    <div className="my-8 border border-slate-200 rounded-xl overflow-hidden shadow-lg bg-white">
      <div className="bg-slate-800 text-slate-100 px-4 py-3 flex justify-between items-center">
        <div className="font-bold text-sm flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-red-500"></span>
          <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
          <span className="w-3 h-3 rounded-full bg-green-500"></span>
          <span className="ml-2 text-slate-300">Lab Virtual: {nomeSimulador}</span>
        </div>
      </div>
      <iframe 
        srcDoc={injectedHtml!}
        style={{ height: `${iframeHeight}px` }}
        className="w-full border-none bg-white"
        sandbox="allow-scripts allow-same-origin"
        scrolling="no"
        title="Simulador Interativo"
      />
    </div>
  );
}

export default function SemesterViewer() {
  const params = useParams();
  const router = useRouter();

  // Agora que o Backend garante a formatação rigorosa via o Agente Formatador LaTeX,
  const processLatex = (text: string) => sanitizeLatex(text);
  const id = params.id as string;

  const [classroom, setClassroom] = useState<any>(null);
  const [aulasGeradas, setAulasGeradas] = useState<any[]>([]);
  const [selectedAula, setSelectedAula] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState<'teoria' | 'exercicios' | 'referencias'>('teoria');

  useEffect(() => {
    if (!id) return;

    // Listener em tempo real da Sala (para pegar o progresso e o cronograma mestre)
    const unsubSala = onSnapshot(doc(db, "classrooms", id), (docSnap) => {
      if (docSnap.exists()) {
        setClassroom(docSnap.data());
      } else {
        alert("Sala não encontrada!");
        router.push("/aluno/dashboard");
      }
      setLoading(false);
    });

    // Listener da subcoleção de Aulas Geradas
    const unsubAulas = onSnapshot(collection(db, "classrooms", id, "aulas"), (snap) => {
      const aulasList = snap.docs
        .map(d => ({ id: d.id, ...d.data() }))
        .filter((a: any) => a.publicada === true);
      setAulasGeradas(aulasList);
    });

    return () => {
      unsubSala();
      unsubAulas();
    };
  }, [id, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Carregando cronograma do semestre...</p>
        </div>
      </div>
    );
  }

  const status = classroom?.status || "";
  const isGenerating = status.startsWith("fatiando") || status.startsWith("gerando");

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <header className="bg-blue-900 text-white p-4 shadow-md flex justify-between items-center z-10 shrink-0">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 hover:bg-blue-800 rounded-lg transition"
            title={isSidebarOpen ? "Esconder cronograma" : "Mostrar cronograma"}
          >
            {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <div>
            <h1 className="text-xl font-bold">{classroom?.id_disciplina} - {classroom?.nome_disciplina}</h1>
            <p className="text-xs text-blue-200">Sala: {classroom?.code} | Status: {status}</p>
          </div>
        </div>
        <button onClick={() => router.back()} className="text-sm bg-blue-800 px-4 py-2 rounded hover:bg-blue-700 transition">
          Voltar
        </button>
      </header>

      <div className="flex flex-1 overflow-hidden relative">
        {/* Sidebar: Cronograma (Menu de Aulas) */}
        <aside className={`bg-white border-r border-slate-200 overflow-y-auto flex flex-col shrink-0 transition-all duration-300 ${isSidebarOpen ? 'w-80' : 'w-0 hidden'}`}>
          <div className="p-4 border-b border-slate-100 bg-slate-50">
            <h2 className="font-bold text-slate-800">Plano de Ensino</h2>
            {isGenerating && (
              <div className="mt-2 text-xs text-blue-600 bg-blue-50 p-2 rounded border border-blue-100 animate-pulse flex items-center gap-2">
                <span>🤖</span> IA gerando aulas ({classroom?.aulas_geradas || 0} de {classroom?.total_aulas || '?'})
              </div>
            )}
          </div>
          
          <div className="p-4 space-y-2">
            {classroom?.cronograma_oficial ? (
              classroom.cronograma_oficial.map((aulaMeta: any, idx: number) => {
                const numero = aulaMeta.numero_aula || (idx + 1);
                // Verifica se o conteúdo completo dessa aula já foi gerado
                const aulaCompleta = aulasGeradas.find(a => String(a.numero_aula) === String(numero) || a.id === String(numero));
                
                const isSelected = selectedAula?.id === aulaCompleta?.id && aulaCompleta != null;

                return (
                  <div 
                    key={idx}
                    onClick={() => {
                      if (aulaCompleta) {
                        setSelectedAula(aulaCompleta);
                        setActiveTab('teoria');
                      }
                    }}
                    className={`p-3 rounded-lg border text-sm transition-all ${
                      aulaCompleta 
                        ? isSelected ? 'bg-blue-50 border-blue-300 shadow-sm cursor-pointer' : 'bg-white border-slate-200 hover:border-blue-200 cursor-pointer'
                        : 'bg-slate-50 border-dashed border-slate-200 opacity-60 cursor-not-allowed'
                    }`}
                  >
                    <div className="flex justify-between items-start mb-1">
                      <span className={`font-bold ${aulaCompleta ? 'text-blue-700' : 'text-slate-500'}`}>Aula {numero}</span>
                      {aulaCompleta && <span className="text-[10px] bg-green-100 text-green-700 px-1 rounded uppercase font-bold">Pronta</span>}
                    </div>
                    <p className={`font-medium line-clamp-2 ${aulaCompleta ? 'text-slate-800' : 'text-slate-500'}`}>
                      {aulaMeta.titulo}
                    </p>
                  </div>
                );
              })
            ) : (
               <div className="text-center p-6 text-slate-400 text-sm">
                 O cronograma ainda não foi estruturado pelo Coordenador.
               </div>
            )}
          </div>
        </aside>

        {/* Main Content: Visualizador da Aula Selecionada */}
        <main className="flex-1 bg-slate-50 overflow-y-auto p-8">
          {!selectedAula ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-400">
              <div className="text-6xl mb-4">📖</div>
              <p className="text-lg">Selecione uma aula no cronograma lateral para estudar.</p>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto pb-20">
              <h2 className="text-3xl font-bold text-blue-900 mb-6 pb-2 border-b-2 border-slate-200">
                Aula {selectedAula.numero_aula}: {selectedAula.titulo}
              </h2>

              {/* TABS NAVIGATION */}
              <div className="flex gap-2 mb-8 bg-slate-200/50 p-1.5 rounded-lg w-fit border border-slate-200">
                <button
                  onClick={() => setActiveTab('teoria')}
                  className={`px-6 py-2.5 rounded-md font-semibold text-sm transition-all ${
                    activeTab === 'teoria' 
                      ? 'bg-white text-blue-900 shadow-sm border border-slate-200/60' 
                      : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  <span className="mr-2">📖</span> Teoria e Simuladores
                </button>
                <button
                  onClick={() => setActiveTab('exercicios')}
                  className={`px-6 py-2.5 rounded-md font-semibold text-sm transition-all ${
                    activeTab === 'exercicios' 
                      ? 'bg-white text-blue-900 shadow-sm border border-slate-200/60' 
                      : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  <span className="mr-2">📝</span> Caderno de Exercícios
                </button>
                <button
                  onClick={() => setActiveTab('referencias')}
                  className={`px-6 py-2.5 rounded-md font-semibold text-sm transition-all ${
                    activeTab === 'referencias' 
                      ? 'bg-white text-blue-900 shadow-sm border border-slate-200/60' 
                      : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  <span className="mr-2">📚</span> Referências
                </button>
              </div>

              {/* CONTEÚDO TEÓRICO (Ativo se aba = teoria) */}
              <div className={activeTab === 'teoria' ? 'block' : 'hidden'}>
                {/* Resumo Executivo / TOC */}
              {selectedAula.conteudo_json?.resumo_executivo_aula && (
                <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-xl mb-10 shadow-sm">
                  <h3 className="text-lg font-bold text-blue-900 mb-2 flex items-center gap-2">
                    <span>🎯</span> Resumo da Aula
                  </h3>
                  <p className="text-blue-800 leading-relaxed">
                    {selectedAula.conteudo_json.resumo_executivo_aula}
                  </p>
                </div>
              )}

              {(() => {
                const paginas = selectedAula.conteudo_json?.paginas_conteudo || selectedAula.conteudo_json?.conteudo_paginas || [];
                return paginas.map((pagina: any, idx: number) => {
                  const isLapidada = !!pagina.discussao_teorica_prosa;
                  const titulo = pagina.titulo_subtopico || pagina.titulo || `Subtópico ${idx + 1}`;
                  const textoProsa = isLapidada 
                    ? pagina.discussao_teorica_prosa 
                    : (pagina.conteudo?.conceito_intuitivo + "\n\n" + pagina.conteudo?.conceito_formal);
                  const latexCode = isLapidada 
                    ? pagina.formalismo_latex 
                    : "";
                  const deducoes = isLapidada
                    ? (pagina.deducao_analitica_linhas || [])
                    : (pagina.conteudo?.deducao_formal_passo_a_passo || []);
                  const exemplos = isLapidada 
                    ? pagina.exemplos_praticos_ricos 
                    : (pagina.conteudo?.exemplo_canonico ? [pagina.conteudo.exemplo_canonico] : []);

                  return (
                    <section key={idx} className="mb-12 bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
                      <h3 className="text-2xl font-bold text-slate-800 mb-6 pb-2 border-b border-slate-100 flex items-center gap-2">
                        <span>{idx + 1}.</span>
                        <span><ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]} components={{p: "span"}}>{processLatex(titulo)}</ReactMarkdown></span>
                      </h3>
                      
                      <div className="prose prose-lg prose-blue max-w-none text-slate-700">
                        <div className="leading-relaxed mb-6 space-y-4">
                          <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                            {processLatex(textoProsa)}
                          </ReactMarkdown>
                        </div>

                        {(() => {
                          const simuladores = selectedAula.conteudo_json?.simuladores_da_aula?.filter(
                            (s: any) => String(s.indice_pagina) === String(idx + 1)
                          );
                          if (simuladores && simuladores.length > 0) {
                            return (
                              <div className="space-y-6 my-6">
                                {simuladores.map((simuladorInfo: any, sIdx: number) => (
                                  <SimuladorInterativo 
                                    key={`sim-${idx}-${sIdx}`}
                                    temaAula={`${selectedAula.titulo} - ${titulo}`} 
                                    nomeSimulador={simuladorInfo.nome_simulador} 
                                    htmlCode={simuladorInfo.codigo_html_gerado}
                                  />
                                ))}
                              </div>
                            );
                          }
                          return null;
                        })()}

                        {latexCode && latexCode !== "null" && (
                          <div className="my-8 p-6 bg-slate-50 rounded-xl border border-slate-200 text-center">
                            <span className="text-blue-800 font-bold block mb-2 text-sm uppercase tracking-wider">Fórmula / Definição Formal</span>
                            <div className="text-lg text-left inline-block w-full break-words">
                              <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                {processLatex(latexCode)}
                              </ReactMarkdown>
                            </div>
                          </div>
                        )}

                        {deducoes?.length > 0 && deducoes[0] !== "null" && (
                          <div className="mb-8 bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                            <div className="p-4 bg-slate-50 font-semibold text-slate-700 flex items-center gap-2 border-b border-slate-200">
                                <span>🔍</span> Demonstração Passo a Passo
                            </div>
                            <div className="p-6 bg-slate-50/50 space-y-4">
                              {deducoes.map((passo: string, pIdx: number) => (
                                <div key={pIdx} className="text-slate-700 text-sm md:text-base leading-relaxed break-words">
                                  <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                    {processLatex(passo)}
                                  </ReactMarkdown>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {exemplos?.length > 0 && (
                          <div className="mt-8">
                            <h4 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                              <span>💡</span> Exemplos Práticos
                            </h4>
                            {exemplos.map((exemplo: any, eIdx: number) => (
                              <div key={eIdx} className="bg-blue-50/40 p-6 rounded-xl mb-6 border border-blue-100">
                                <div className="font-semibold text-slate-800 mb-4 border-b border-blue-200 pb-2">
                                  <div className="flex-1 pr-4 overflow-x-auto overflow-y-hidden">
                                    <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                      {processLatex(exemplo.contexto_e_enunciado || exemplo.enunciado)}
                                    </ReactMarkdown>
                                  </div>
                                </div>
                                
                                <div className="mt-6">
                                  {(exemplo.desenvolvimento_aritmético_passo_a_passo || exemplo.passo_a_passo_solucao) && (
                                    <div className="bg-white p-4 rounded-lg mb-4 border border-slate-200 shadow-sm overflow-x-auto overflow-y-hidden space-y-2">
                                      <h5 className="font-bold text-slate-700 mb-2 text-sm uppercase">Passo a Passo</h5>
                                      {(exemplo.desenvolvimento_aritmético_passo_a_passo || exemplo.passo_a_passo_solucao).map((passo: string, pIdx: number) => (
                                        <div key={pIdx} className="text-slate-600 text-sm">
                                          <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                            {processLatex(passo)}
                                          </ReactMarkdown>
                                        </div>
                                      ))}
                                    </div>
                                  )}

                                  <div className="bg-green-50 p-4 rounded-lg mt-4 border border-green-200">
                                    <strong className="text-green-800 block mb-1">Conclusão:</strong>
                                    <div className="text-green-900">
                                      <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                        {processLatex(exemplo.conclusao_e_laudo_comercial || exemplo.resultado_final)}
                                      </ReactMarkdown>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </section>
                  );
                });
              })()}
              </div> {/* Fim Aba Teoria */}

              {/* ABA EXERCÍCIOS */}
              <div className={activeTab === 'exercicios' ? 'block' : 'hidden'}>

              {selectedAula.conteudo_json?.exercicios_da_aula && (
                <section className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 mt-12">
                  <h3 className="text-2xl font-bold text-slate-800 mb-8 pb-4 border-b-2 border-slate-100 flex items-center gap-3">
                    <span>📝</span> Caderno de Exercícios
                  </h3>

                  <div className="space-y-12">
                    {/* Múltipla Escolha */}
                    {selectedAula.conteudo_json.exercicios_da_aula.questoes_multipla_escolha?.length > 0 && (
                      <div>
                        <h4 className="text-xl font-bold text-indigo-900 mb-6 flex items-center gap-2">
                          <span className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 text-sm">A</span>
                          Múltipla Escolha
                        </h4>
                        <div className="space-y-8">
                          {selectedAula.conteudo_json.exercicios_da_aula.questoes_multipla_escolha.map((q: any, i: number) => (
                            <div key={`mc-${i}`} className="bg-slate-50 p-6 rounded-xl border border-slate-200">
                              <div className="font-semibold text-slate-800 mb-6 flex items-start gap-2">
                                <span className="text-indigo-600 font-bold">{i + 1}.</span>
                                <span className="flex-1">
                                  <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                    {processLatex(q.enunciado)}
                                  </ReactMarkdown>
                                </span>
                              </div>
                              <div className="space-y-3 mb-6">
                                {Object.entries(q.alternativas).filter(([k, v]) => v).sort(([a], [b]) => a.localeCompare(b)).map(([letra, texto]: any) => (
                                  <label key={letra} className="flex gap-4 p-4 rounded-lg border border-slate-200 bg-white hover:border-indigo-300 cursor-pointer transition-colors items-start">
                                    <input type="radio" name={`q-${i}`} className="mt-1" />
                                    <div>
                                      <strong className="text-slate-700 mr-2">{letra})</strong>
                                      <span className="flex-1 text-slate-600">
                                        <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                          {processLatex(texto)}
                                        </ReactMarkdown>
                                      </span>
                                    </div>
                                  </label>
                                ))}
                              </div>
                              <div className="mt-4">
                                <div className="text-indigo-600 font-bold inline-flex items-center gap-1">
                                  <span>Gabarito:</span>
                                </div>
                                <div className="mt-4 p-4 bg-indigo-50 border border-indigo-100 rounded-lg text-sm text-indigo-900">
                                  <strong className="block mb-2">Alternativa Correta: {q.alternativa_correta}</strong>
                                  <div className="mt-2 text-slate-800">
                                    <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                      {processLatex(q.gabarito_comentado)}
                                    </ReactMarkdown>
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Discursivas */}
                    {selectedAula.conteudo_json.exercicios_da_aula.questoes_discursivas?.length > 0 && (
                      <div>
                        <h4 className="text-xl font-bold text-indigo-900 mb-6 mt-12 flex items-center gap-2">
                          <span className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 text-sm">✏️</span>
                          Questões Discursivas
                        </h4>
                        <div className="space-y-8">
                          {selectedAula.conteudo_json.exercicios_da_aula.questoes_discursivas.map((q: any, i: number) => (
                            <div key={`disc-${i}`} className="bg-slate-50 p-6 rounded-xl border border-slate-200">
                              <div className="font-semibold text-slate-800 mb-4 flex items-start gap-2">
                                <span className="text-indigo-600 font-bold">Q{i + 1}.</span>
                                <span className="flex-1">
                                  <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                    {processLatex(q.enunciado)}
                                  </ReactMarkdown>
                                </span>
                              </div>
                              <div className="mt-4">
                                <div className="text-indigo-600 font-bold inline-flex items-center gap-1">
                                  <span>Solução Passo a Passo:</span>
                                </div>
                                <div className="mt-4 p-6 bg-white border border-slate-200 rounded-lg overflow-x-auto overflow-y-hidden space-y-4">
                                  {q.gabarito_passo_a_passo.map((passo: string, pIdx: number) => (
                                    <div key={pIdx} className="text-slate-600">
                                      <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                        {processLatex(passo)}
                                      </ReactMarkdown>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </section>
              )}
              </div> {/* Fim Aba Exercícios */}

              {/* ABA REFERÊNCIAS */}
              <div className={activeTab === 'referencias' ? 'block' : 'hidden'}>

              {selectedAula.conteudo_json?.referencias_bibliograficas_finais?.length > 0 && (
                <section className="bg-slate-800 text-slate-300 p-8 rounded-2xl mt-12">
                  <h3 className="text-xl font-bold text-white mb-6">📚 Referências da Aula</h3>
                  <ul className="space-y-3">
                    {selectedAula.conteudo_json.referencias_bibliograficas_finais.map((ref: string, rIdx: number) => (
                      <li key={rIdx} className="flex gap-3">
                        <span className="text-blue-400">•</span>
                        <span>{ref}</span>
                      </li>
                    ))}
                  </ul>
                </section>
              )}
              </div> {/* Fim Aba Referências */}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
