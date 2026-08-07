"use client";

import { useEffect, useState, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { doc, onSnapshot, collection, getDocs, updateDoc } from "firebase/firestore";
import { db, auth } from "@/lib/firebase";
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { Menu, X, Play, RefreshCw } from 'lucide-react';

function SimuladorInterativo({ temaAula, nomeSimulador, htmlCode }: { temaAula: string, nomeSimulador: string, htmlCode?: string }) {
  const [html, setHtml] = useState<string | null>(htmlCode || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const carregarSimulador = async () => {
    setLoading(true);
    setError(false);
    try {
      const res = await fetch("http://localhost:8000/api/gerar_simulador", {
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
        srcDoc={html!}
        className="w-full h-[600px] border-none bg-white"
        sandbox="allow-scripts"
        title="Simulador Interativo"
      />
    </div>
  );
}

function BlockEditor({
  valorInicial,
  caminhoBloco,
  salaId,
  aulaId,
  onSaved
}: { valorInicial: string, caminhoBloco: string, salaId: string, aulaId: string, onSaved: () => void }) {
  const [editMode, setEditMode] = useState(false);
  const [conteudo, setConteudo] = useState(valorInicial);
  const [promptIA, setPromptIA] = useState("");
  const [saving, setSaving] = useState(false);

  const salvar = async () => {
    setSaving(true);
    try {
      await fetch("http://localhost:8000/api/editar_aula_bloco", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sala_id: salaId,
          aula_id: aulaId,
          caminho_bloco: caminhoBloco,
          novo_conteudo: conteudo,
          prompt_ia: promptIA
        })
      });
      setEditMode(false);
      onSaved();
    } catch (e) {
      alert("Erro ao salvar.");
    } finally {
      setSaving(false);
    }
  };

  if (!editMode) {
    return (
      <button onClick={() => setEditMode(true)} className="text-xs bg-slate-200 text-slate-700 px-3 py-1 rounded hover:bg-slate-300 flex items-center gap-1 mb-4 font-bold shadow-sm">
        ✏️ Editar Bloco
      </button>
    );
  }

  return (
    <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-xl mb-4 shadow-inner">
      <h4 className="font-bold text-yellow-800 text-sm mb-2">Modo de Edição (Markdown/LaTeX)</h4>
      <textarea
        className="w-full h-40 p-3 border border-yellow-300 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500 font-mono text-sm bg-white text-slate-900"
        value={conteudo}
        onChange={(e) => setConteudo(e.target.value)}
      />
      <div className="mt-4">
        <label className="text-xs font-bold text-yellow-800 mb-1 block">Pedir para IA reescrever (opcional):</label>
        <input
          type="text"
          placeholder="Ex: Deixe este texto mais didático e inclua um exemplo prático."
          className="w-full p-2 border border-yellow-300 rounded text-sm bg-white"
          value={promptIA}
          onChange={(e) => setPromptIA(e.target.value)}
        />
      </div>
      <div className="flex justify-end gap-2 mt-4">
        <button onClick={() => setEditMode(false)} className="px-4 py-2 text-sm bg-white border border-slate-300 rounded hover:bg-slate-100">Cancelar</button>
        <button onClick={salvar} disabled={saving} className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 font-bold flex items-center gap-2">
          {saving ? "Salvando..." : "💾 Salvar Alterações"}
        </button>
      </div>
    </div>
  );
}

export default function ProfessorSemesterViewer() {
  const params = useParams();
  const router = useRouter();

  // Agora que o Backend garante a formatação rigorosa via o Agente Formatador LaTeX,
  // o Frontend precisa apenas isolar os blocos $$ em seus próprios parágrafos
  // para que o remark-math consiga processá-los corretamente como 'display math'.
  const processLatex = (text: string) => {
    if (!text) return "";
    // 1. O plugin remark-math já lida com $$ inline. Remover a quebra de linha agressiva.
    let processed = text;
    
    // 2. Remove espaços em branco no INÍCIO de qualquer linha!
    // Isso impede que o Markdown leia a linha como um bloco de código identado <pre> (o erro da imagem)
    processed = processed.replace(/^[ \t]+/gm, '');

    // 3. Arruma espaços acidentais em math inline gerados pela IA (ex: $ k $ -> $k$)
    // O plugin remark-math é estrito e não aceita espaços logo após o $
    processed = processed.replace(/\$\s+([^$\n]+?)\s+\$/g, '$$$1$$');

    // 4. Remove quebras de linha excessivas
    return processed.replace(/\n{4,}/g, '\n\n\n');
  };
  const id = params.id as string;

  const [classroom, setClassroom] = useState<any>(null);
  const [aulasGeradas, setAulasGeradas] = useState<any[]>([]);
  const [selectedAula, setSelectedAula] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState<'teoria' | 'exercicios' | 'referencias'>('teoria');
  
  const [modalNovaAulaOpen, setModalNovaAulaOpen] = useState(false);
  const [novaAulaTitulo, setNovaAulaTitulo] = useState("");
  const [novaAulaDescricao, setNovaAulaDescricao] = useState("");
  const [novaAulaPdf, setNovaAulaPdf] = useState("");
  const [uploadingNovaAula, setUploadingNovaAula] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (file: File) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf")) return alert("Somente PDF");
    setUploadingNovaAula(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://localhost:8000/api/upload_pdf", { method: "POST", body: formData });
      const data = await res.json();
      if (res.ok) {
        setNovaAulaPdf(data.texto_extraido);
      } else {
        alert("Erro no upload");
      }
    } catch (e) {
      alert("Erro na rede");
    } finally {
      setUploadingNovaAula(false);
    }
  };

  const handleCriarAulaAvulsa = async () => {
    if (!novaAulaTitulo || !novaAulaDescricao) return alert("Título e Descrição obrigatórios");
    try {
      const nextNum = (classroom?.total_aulas || classroom?.cronograma_oficial?.length || 0) + 1;
      await fetch("http://localhost:8000/api/gerar_aula_avulsa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sala_id: id,
          id_disciplina: classroom?.id_disciplina,
          numero_aula: nextNum,
          aula_manual: {
            titulo: novaAulaTitulo,
            descricao: novaAulaDescricao,
            texto_base_pdf: novaAulaPdf,
            gerar_exercicios: true,
            gerar_simulador: false
          }
        })
      });
      setModalNovaAulaOpen(false);
      alert("Sua aula foi enviada para geração em background!");
    } catch (e) {
      alert("Erro ao criar nova aula");
    }
  };

  const togglePublish = async (aula: any) => {
    try {
      const aulaRef = doc(db, "classrooms", id, "aulas", aula.id);
      await updateDoc(aulaRef, { publicada: !aula.publicada });
    } catch (error) {
      alert("Erro ao alterar visibilidade da aula.");
    }
  };

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
      const aulasList = snap.docs.map(d => ({ id: d.id, ...d.data() }));
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
        <div className="flex gap-2">
          <button onClick={() => router.push("/professor/dashboard")} className="text-sm bg-blue-800 px-4 py-2 rounded hover:bg-blue-700 transition">
            Voltar ao Dashboard
          </button>
        </div>
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
          <div className="p-4 mt-auto border-t border-slate-200">
            <button 
              onClick={() => setModalNovaAulaOpen(true)}
              className="w-full bg-blue-100 text-blue-700 hover:bg-blue-200 border border-blue-300 font-bold py-2 px-4 rounded transition"
            >
              + Adicionar Nova Aula
            </button>
          </div>
        </aside>

        {/* Modal de Nova Aula */}
        {modalNovaAulaOpen && (
          <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl shadow-xl w-full max-w-lg overflow-hidden">
              <div className="bg-blue-900 p-4 flex justify-between items-center text-white">
                <h3 className="font-bold text-lg">Criar Aula Extra</h3>
                <button onClick={() => setModalNovaAulaOpen(false)}><X size={20}/></button>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-1">Título da Aula</label>
                  <input className="w-full border rounded p-2" value={novaAulaTitulo} onChange={e => setNovaAulaTitulo(e.target.value)} placeholder="Ex: Exercícios Avançados" />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-1">Upload de PDF Base</label>
                  <input type="file" ref={fileInputRef} className="hidden" onChange={e => e.target.files && handleFileUpload(e.target.files[0])} accept=".pdf" />
                  <button onClick={() => fileInputRef.current?.click()} className="bg-slate-200 px-4 py-2 rounded text-sm block" disabled={uploadingNovaAula}>
                    {uploadingNovaAula ? "Extraindo..." : "Anexar PDF"}
                  </button>
                  {novaAulaPdf && <p className="text-green-600 text-xs mt-1">PDF carregado ({novaAulaPdf.length} chars)</p>}
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-1">Diretrizes (O que a IA deve criar?)</label>
                  <textarea className="w-full border rounded p-2 h-24" value={novaAulaDescricao} onChange={e => setNovaAulaDescricao(e.target.value)} placeholder="Descreva os tópicos." />
                </div>
                <button onClick={handleCriarAulaAvulsa} className="w-full bg-blue-600 text-white font-bold py-3 rounded">
                  Gerar Nova Aula
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Main Content: Visualizador da Aula Selecionada */}
        <main className="flex-1 bg-slate-50 overflow-y-auto p-8">
          {!selectedAula ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-400">
              <div className="text-6xl mb-4">📖</div>
              <p className="text-lg">Selecione uma aula no cronograma lateral para estudar.</p>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto pb-20">
              <div className="flex justify-between items-center mb-6 pb-2 border-b-2 border-slate-200">
                <h2 className="text-3xl font-bold text-blue-900">
                  Aula {selectedAula.numero_aula}: {selectedAula.titulo}
                </h2>
                <button
                  onClick={() => togglePublish(selectedAula)}
                  className={`px-4 py-2 rounded-full font-bold shadow-sm transition-colors flex items-center gap-2 ${
                    selectedAula.publicada 
                      ? 'bg-green-100 text-green-700 hover:bg-green-200 border border-green-300' 
                      : 'bg-slate-200 text-slate-600 hover:bg-slate-300 border border-slate-300'
                  }`}
                >
                  {selectedAula.publicada ? "👁️ Visível p/ Alunos" : "🙈 Oculta p/ Alunos"}
                </button>
              </div>

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
                  <div className="mt-4">
                    <BlockEditor 
                      valorInicial={selectedAula.conteudo_json.resumo_executivo_aula}
                      caminhoBloco="conteudo_json.resumo_executivo_aula"
                      salaId={classroom.id}
                      aulaId={selectedAula.id}
                      onSaved={() => {}}
                    />
                  </div>
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
                      <h3 className="text-2xl font-bold text-slate-800 mb-6 pb-2 border-b border-slate-100">
                        {idx + 1}. {titulo}
                      </h3>
                      
                      <BlockEditor 
                        valorInicial={textoProsa}
                        caminhoBloco={isLapidada ? `conteudo_json.paginas_conteudo.${idx}.discussao_teorica_prosa` : `conteudo_json.conteudo_paginas.${idx}.conteudo.conceito_intuitivo`}
                        salaId={classroom.id}
                        aulaId={selectedAula.id}
                        onSaved={() => {}}
                      />

                      <div className="prose prose-lg prose-blue max-w-none text-slate-700">
                        <div className="whitespace-pre-wrap leading-relaxed mb-6">
                          <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                            {processLatex(textoProsa)}
                          </ReactMarkdown>
                        </div>

                        {(() => {
                          const simuladorInfo = selectedAula.conteudo_json?.simuladores_da_aula?.find(
                            (s: any) => String(s.indice_pagina) === String(idx + 1)
                          );
                          if (simuladorInfo) {
                            return (
                              <SimuladorInterativo 
                                temaAula={`${selectedAula.titulo} - ${titulo}`} 
                                nomeSimulador={simuladorInfo.nome_simulador} 
                                htmlCode={simuladorInfo.codigo_html_gerado}
                              />
                            );
                          }
                          return null;
                        })()}

                        {latexCode && (
                          <div className="my-8 p-6 bg-slate-50 rounded-xl overflow-x-auto border border-slate-200 text-center">
                            <span className="text-blue-800 font-bold block mb-2 text-sm uppercase tracking-wider">Fórmula / Definição Formal</span>
                            <div className="text-lg text-left inline-block">
                              <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                {processLatex(latexCode)}
                              </ReactMarkdown>
                            </div>
                          </div>
                        )}

                        {deducoes?.length > 0 && (
                          <details className="mb-8 group bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                            <summary className="p-4 bg-slate-50 cursor-pointer font-semibold text-slate-700 flex justify-between items-center outline-none hover:bg-slate-100 transition-colors list-none">
                              <div className="flex items-center gap-2">
                                <span>🔍</span> Demonstração Passo a Passo
                              </div>
                              <span className="text-slate-400 group-open:rotate-180 transition-transform">▼</span>
                            </summary>
                            <div className="p-6 border-t border-slate-200 bg-slate-50/50 space-y-4">
                              {deducoes.map((passo: string, pIdx: number) => (
                                <div key={pIdx} className="text-slate-600 text-sm md:text-base overflow-x-auto">
                                  <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                    {processLatex(passo)}
                                  </ReactMarkdown>
                                </div>
                              ))}
                            </div>
                          </details>
                        )}

                        {exemplos?.length > 0 && (
                          <div className="mt-8">
                            <h4 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                              <span>💡</span> Exemplos Práticos Interativos
                            </h4>
                            {exemplos.map((exemplo: any, eIdx: number) => (
                              <details key={eIdx} className="bg-blue-50/40 p-6 rounded-xl mb-6 border border-blue-100 group">
                                <summary className="font-semibold text-slate-800 cursor-pointer flex justify-between items-center list-none outline-none">
                                  <div className="flex-1 pr-4">
                                    <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                      {processLatex(exemplo.contexto_e_enunciado || exemplo.enunciado)}
                                    </ReactMarkdown>
                                  </div>
                                  <span className="text-blue-600 font-bold group-open:rotate-180 transition-transform">▼</span>
                                </summary>
                                
                                <div className="mt-6">
                                  {(exemplo.desenvolvimento_aritmético_passo_a_passo || exemplo.passo_a_passo_solucao) && (
                                    <div className="bg-white p-4 rounded-lg mb-4 border border-slate-200 shadow-sm overflow-x-auto space-y-2">
                                      <h5 className="font-bold text-slate-700 mb-2 text-sm uppercase">Passo a Passo</h5>
                                      {(exemplo.desenvolvimento_aritmético_passo_a_passo || exemplo.passo_a_passo_solucao).map((passo: string, pIdx: number) => (
                                        <div key={pIdx} className="text-slate-600 text-sm">
                                          <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
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
                              </details>
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
                                {Object.entries(q.alternativas).filter(([k, v]) => v).map(([letra, texto]: any) => (
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
                              <details className="group">
                                <summary className="text-indigo-600 font-bold cursor-pointer outline-none hover:underline inline-flex items-center gap-1 list-none">
                                  <span>Ver Gabarito</span>
                                </summary>
                                <div className="mt-4 p-4 bg-indigo-50 border border-indigo-100 rounded-lg text-sm text-indigo-900">
                                  <strong className="block mb-2">Alternativa Correta: {q.alternativa_correta}</strong>
                                  <div className="mt-2 text-slate-800">
                                    <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                      {processLatex(q.gabarito_comentado)}
                                    </ReactMarkdown>
                                  </div>
                                </div>
                              </details>
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
                              <details className="group">
                                <summary className="text-indigo-600 font-bold cursor-pointer outline-none hover:underline inline-flex items-center gap-1 list-none">
                                  <span>Ver Solução Passo a Passo</span>
                                </summary>
                                <div className="mt-4 p-6 bg-white border border-slate-200 rounded-lg overflow-x-auto space-y-4">
                                  {q.gabarito_passo_a_passo.map((passo: string, pIdx: number) => (
                                    <div key={pIdx} className="text-slate-600">
                                      <ReactMarkdown remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[[rehypeKatex, {strict: false}]]}>
                                        {processLatex(passo)}
                                      </ReactMarkdown>
                                    </div>
                                  ))}
                                </div>
                              </details>
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
