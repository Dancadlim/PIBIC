"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { db } from "@/lib/firebase";
import { collection, getDocs, addDoc, serverTimestamp } from "firebase/firestore";

export default function CriarSalaPersonalizada() {
  const router = useRouter();
  
  // Data
  const [disciplinas, setDisciplinas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // General Settings
  const [selectedDisciplina, setSelectedDisciplina] = useState("");
  const [tomPersonalidade, setTomPersonalidade] = useState("");
  const [nivelExercicios, setNivelExercicios] = useState("");
  
  // Logic Tree State
  const [modoAulas, setModoAulas] = useState<"padrao" | "auto" | "manual">("padrao");
  const [qtdManual, setQtdManual] = useState<number>(30);
  const [formatoCriacao, setFormatoCriacao] = useState<"ia_decide" | "so_temas" | "desenhar_aula">("ia_decide");
  const [aulasComplementares, setAulasComplementares] = useState(false);

  // Upload Global (Quando não for Bloco-a-Bloco)
  const [uploadingGlobal, setUploadingGlobal] = useState(false);
  const [arquivoGlobalPdf, setArquivoGlobalPdf] = useState("");
  const [arquivoGlobalNome, setArquivoGlobalNome] = useState("");
  const [observacoesGlobais, setObservacoesGlobais] = useState("");
  const globalPdfRef = useRef<HTMLInputElement>(null);

  // Blocos Manuais (Quando for Manual -> Desenhar Aula)
  const [aulasManuais, setAulasManuais] = useState<any[]>([{
    id: 1,
    titulo: "",
    descricao: "",
    texto_base_pdf: "",
    nome_arquivo: "",
    uploading: false,
    gerar_exercicios: true,
    sugestoes_exercicios: "",
    gerar_simulador: false,
    sugestoes_simulador: ""
  }]);
  const fileInputRefs = useRef<any>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const discSnapshot = await getDocs(collection(db, "disciplinas"));
        const discList = discSnapshot.docs.map(d => ({ id: d.id, ...(d.data() as any) }));
        setDisciplinas(discList);
        if (discList.length > 0) setSelectedDisciplina(discList[0].id_disciplina);
      } catch (error) {
        console.error("Erro ao carregar disciplinas:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const isBlocoABloco = formatoCriacao === "desenhar_aula" || formatoCriacao === "so_temas";

  const handleGlobalFileUpload = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    setUploadingGlobal(true);
    
    const formData = new FormData();
    let validFilesCount = 0;
    
    for (let i = 0; i < files.length; i++) {
        if (files[i].name.toLowerCase().endsWith(".pdf")) {
            formData.append("files", files[i]);
            validFilesCount++;
        }
    }
    
    if (validFilesCount === 0) {
        alert("Somente arquivos PDF são suportados.");
        setUploadingGlobal(false);
        return;
    }

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/upload_pdf`, { method: "POST", body: formData });
      const data = await res.json();
      if (res.ok) {
        // Se mandou múltiplos, o backend concatena.
        setArquivoGlobalPdf(data.texto_extraido);
        setArquivoGlobalNome(`${validFilesCount} arquivo(s) processado(s) com sucesso`);
      } else {
        alert("Erro no upload: " + data.detail);
      }
    } catch (e) {
      alert("Erro de rede");
    } finally {
      setUploadingGlobal(false);
    }
  };

  const handleBlocoFileUpload = async (index: number, file: File) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf")) return alert("Somente arquivos PDF.");
    
    const updated = [...aulasManuais];
    updated[index].uploading = true;
    setAulasManuais(updated);

    const formData = new FormData();
    formData.append("files", file);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/upload_pdf`, { method: "POST", body: formData });
      const data = await res.json();
      const nextUpdated = [...aulasManuais];
      
      if (res.ok) {
        nextUpdated[index].texto_base_pdf = data.texto_extraido;
        nextUpdated[index].nome_arquivo = file.name;
      } else {
        alert("Erro no upload: " + data.detail);
      }
      nextUpdated[index].uploading = false;
      setAulasManuais(nextUpdated);
    } catch (e) {
      alert("Erro na rede ao enviar PDF");
      const nextUpdated = [...aulasManuais];
      nextUpdated[index].uploading = false;
      setAulasManuais(nextUpdated);
    }
  };

  const addBloco = () => {
    setAulasManuais([...aulasManuais, {
      id: aulasManuais.length + 1,
      titulo: "",
      descricao: "",
      texto_base_pdf: "",
      nome_arquivo: "",
      uploading: false,
      gerar_exercicios: true,
      sugestoes_exercicios: "",
      gerar_simulador: false,
      sugestoes_simulador: ""
    }]);
  };

  const handleSubmit = async () => {
    if (!selectedDisciplina) return alert("Selecione uma disciplina.");
    if (modoAulas === "manual" && (qtdManual < 1 || qtdManual > 100)) {
        return alert("Quantidade manual deve ser entre 1 e 100.");
    }
    
    setSubmitting(true);
    
    try {
      const code = Math.floor(1000 + Math.random() * 9000).toString();
      const disc = disciplinas.find(d => d.id_disciplina === selectedDisciplina);
      
      const docRef = await addDoc(collection(db, "classrooms"), {
        code,
        teacherId: "TEST_PROFESSOR_123", // mockUser
        id_disciplina: selectedDisciplina,
        nome_disciplina: disc?.nome || "Disciplina",
        createdAt: serverTimestamp(),
        status: "creating_semester",
        modo_criacao: "livre"
      });

      // Mapeamento
      let payloadTipoCarga = "padrao_30";
      let payloadLimite = 30;

      if (modoAulas === "padrao") {
          payloadTipoCarga = "auto_ementa"; 
      } else if (modoAulas === "auto") {
          payloadTipoCarga = "auto_ia"; 
      } else if (modoAulas === "manual") {
          payloadTipoCarga = "manual";
          payloadLimite = qtdManual;
      }

      // Constrói as instruções customizadas adicionando as observações globais
      let customInstructions = `Tom/Personalidade: ${tomPersonalidade}\nNível Exercícios: ${nivelExercicios}`;
      if (!isBlocoABloco && observacoesGlobais.trim() !== "") {
          customInstructions += `\nObservações Gerais (Materiais/Foco): ${observacoesGlobais}`;
      }

      const formattedBlocos = isBlocoABloco ? aulasManuais.map(a => ({
          titulo: a.titulo || "Sem título",
          descricao: a.descricao + (a.gerar_exercicios && a.sugestoes_exercicios ? `\n(Dica p/ Exercícios: ${a.sugestoes_exercicios})` : "") + (a.gerar_simulador && a.sugestoes_simulador ? `\n(Dica p/ Simulador: ${a.sugestoes_simulador})` : ""),
          texto_base_pdf: a.texto_base_pdf || "",
          gerar_exercicios: a.gerar_exercicios,
          gerar_simulador: a.gerar_simulador
      })) : [];

      const payload = {
        id_sala: docRef.id,
        id_disciplina: selectedDisciplina,
        modo: "livre",
        instrucoes_personalizadas: customInstructions,
        max_aulas: payloadLimite, 
        limite_execucao: payloadLimite,
        tipo_carga_horaria: payloadTipoCarga,
        permitir_aprofundamento: aulasComplementares,
        tipo_crie_seu_jeito: isBlocoABloco ? "bloco_a_bloco" : "automatico",
        arquivo_global_pdf: isBlocoABloco ? "" : arquivoGlobalPdf,
        aulas_manuais: formattedBlocos
      };

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      fetch(`${apiUrl}/api/gerar_semestre`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).catch(err => {
        console.error("Erro ao chamar API de geração", err);
      });

      router.push("/professor/dashboard");

    } catch (error) {
      console.error("Erro ao criar sala:", error);
      alert("Erro ao criar a sala.");
      setSubmitting(false);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center text-slate-500">Carregando...</div>;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans pb-20">
      <nav className="bg-blue-900 text-white px-6 py-4 flex justify-between items-center shadow-md sticky top-0 z-50">
        <div>
          <h1 className="text-xl font-bold">Painel do Professor</h1>
        </div>
        <button onClick={() => router.push("/professor/dashboard")} className="text-sm bg-blue-800 px-4 py-2 rounded hover:bg-blue-700 transition">Voltar</button>
      </nav>

      <main className="max-w-4xl mx-auto mt-8 p-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
            <div className="flex items-center gap-4 mb-6">
                <div className="text-4xl">✏️</div>
                <div>
                    <h2 className="text-2xl font-bold text-slate-800">Crie do Seu Jeito</h2>
                    <p className="text-slate-500">Controle absoluto sobre a criação do semestre. Anexe seus próprios PDFs, dite as regras e esculpe aula por aula (se quiser).</p>
                </div>
            </div>

            <div className="mb-8">
                <label className="block text-sm font-bold text-slate-700 mb-2">Disciplina da Grade Oficial</label>
                <select
                className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-800 bg-slate-50"
                value={selectedDisciplina}
                onChange={(e) => setSelectedDisciplina(e.target.value)}
                >
                {disciplinas.map((d) => (
                    <option key={d.id_disciplina} value={d.id_disciplina}>
                    {d.id_disciplina} - {d.nome}
                    </option>
                ))}
                </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                <div>
                    <label className="block text-sm font-bold text-slate-700 mb-2">Tom e Personalidade do Conteúdo</label>
                    <textarea
                    placeholder="Ex: Quero um tom provocativo, estilo professor descolado que usa cultura pop..."
                    className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 bg-slate-50"
                    rows={3}
                    value={tomPersonalidade}
                    onChange={(e) => setTomPersonalidade(e.target.value)}
                    />
                </div>
                <div>
                    <label className="block text-sm font-bold text-slate-700 mb-2">Nível e Foco dos Exercícios</label>
                    <textarea
                    placeholder="Ex: Nível de dificuldade alto, foco em raciocínio lógico e menos decoreba..."
                    className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 bg-slate-50"
                    rows={3}
                    value={nivelExercicios}
                    onChange={(e) => setNivelExercicios(e.target.value)}
                    />
                </div>
            </div>

            <div className="mb-8 border-t border-slate-200 pt-8">
                <h3 className="text-xl font-bold text-slate-800 mb-6">Quantidade de Aulas (Cronograma)</h3>
                <div className="space-y-3">
                    <label className="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-lg cursor-pointer hover:border-blue-400">
                        <input type="radio" checked={modoAulas === "padrao"} onChange={() => setModoAulas("padrao")} className="w-4 h-4 text-blue-600" />
                        <span className="font-medium text-slate-700">Usar carga horária oficial da ementa (Ex: 30 aulas)</span>
                    </label>
                    <label className="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-lg cursor-pointer hover:border-blue-400">
                        <input type="radio" checked={modoAulas === "auto"} onChange={() => setModoAulas("auto")} className="w-4 h-4 text-blue-600" />
                        <span className="font-medium text-slate-700">A IA decide com base no material que eu enviar</span>
                    </label>
                    <label className="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-lg cursor-pointer hover:border-blue-400">
                        <input type="radio" checked={modoAulas === "manual"} onChange={() => setModoAulas("manual")} className="w-4 h-4 text-blue-600" />
                        <span className="font-medium text-slate-700">Manual (Quantidade exata estrita)</span>
                    </label>
                </div>
            </div>

            {modoAulas === "manual" && (
                <div className="mb-8 p-6 bg-blue-50 rounded-xl border border-blue-100 animate-fade-in">
                    <div className="flex items-center gap-4">
                        <label className="text-sm font-bold text-blue-900 w-48">Total Exato de Aulas:</label>
                        <input 
                            type="number" min="1" max="100" 
                            value={qtdManual} 
                            onChange={e => setQtdManual(Number(e.target.value))} 
                            className="p-2 border border-blue-200 rounded w-24 text-center font-bold text-blue-900 shadow-inner"
                        />
                    </div>
                </div>
            )}

            <div className="mb-8 p-6 bg-indigo-50 rounded-xl border border-indigo-100">
                <h4 className="text-lg font-bold text-indigo-900 mb-4">Como você deseja estruturar o conteúdo?</h4>
                <div className="flex flex-col md:flex-row gap-4">
                    <button 
                        onClick={() => setFormatoCriacao("ia_decide")}
                        className={`flex-1 py-4 px-4 rounded-xl font-bold border-2 transition-all ${formatoCriacao === "ia_decide" ? "bg-indigo-600 border-indigo-600 text-white shadow-md" : "bg-white border-indigo-200 text-indigo-700 hover:bg-indigo-100"}`}
                    >
                        <span className="block text-2xl mb-2">🤖</span>
                        Deixar o trabalho pra IA
                        <span className="block text-xs font-normal opacity-80 mt-1">Piscina global de PDFs</span>
                    </button>
                    <button 
                        onClick={() => setFormatoCriacao("so_temas")}
                        className={`flex-1 py-4 px-4 rounded-xl font-bold border-2 transition-all ${formatoCriacao === "so_temas" ? "bg-indigo-600 border-indigo-600 text-white shadow-md" : "bg-white border-indigo-200 text-indigo-700 hover:bg-indigo-100"}`}
                    >
                        <span className="block text-2xl mb-2">📝</span>
                        Colocar apenas os temas
                        <span className="block text-xs font-normal opacity-80 mt-1">IA pesquisa e escreve o resto</span>
                    </button>
                    <button 
                        onClick={() => setFormatoCriacao("desenhar_aula")}
                        className={`flex-1 py-4 px-4 rounded-xl font-bold border-2 transition-all ${formatoCriacao === "desenhar_aula" ? "bg-indigo-600 border-indigo-600 text-white shadow-md" : "bg-white border-indigo-200 text-indigo-700 hover:bg-indigo-100"}`}
                    >
                        <span className="block text-2xl mb-2">🛠️</span>
                        Desenhar aula a aula
                        <span className="block text-xs font-normal opacity-80 mt-1">O Artesão de Aulas completo</span>
                    </button>
                </div>
            </div>

            {/* ZONA CONDICIONAL: GLOBAL VS BLOCO-A-BLOCO */}
            {!isBlocoABloco ? (
                <div className="mt-12 p-8 border-2 border-dashed border-slate-300 rounded-2xl bg-slate-50 text-center animate-fade-in">
                    <div className="text-5xl mb-4">📚</div>
                    <h3 className="text-xl font-bold text-slate-800 mb-2">Piscina Global de Arquivos</h3>
                    <p className="text-slate-500 mb-6 max-w-lg mx-auto">Jogue todos os seus PDFs aqui. A IA vai ler absolutamente tudo e dividir o conteúdo nas aulas automaticamente.</p>
                    
                    <input type="file" ref={globalPdfRef} className="hidden" accept=".pdf" multiple onChange={e => handleGlobalFileUpload(e.target.files)} />
                    <button 
                        onClick={() => globalPdfRef.current?.click()}
                        className="bg-slate-800 text-white px-8 py-3 rounded-full font-bold shadow-md hover:bg-slate-700 transition"
                        disabled={uploadingGlobal}
                    >
                        {uploadingGlobal ? "Extraindo textos..." : "📎 Anexar Múltiplos PDFs"}
                    </button>
                    {arquivoGlobalNome && <p className="text-green-600 mt-4 font-bold bg-green-50 inline-block px-4 py-2 rounded-full border border-green-200">✓ {arquivoGlobalNome}</p>}

                    <div className="mt-8 text-left">
                        <label className="block text-sm font-bold text-slate-700 mb-2">Observações Globais (Opcional)</label>
                        <textarea
                            placeholder="Ex: Baseie-se mais na aula 4 do material. Evite a demonstração do capítulo 2..."
                            className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 bg-white shadow-sm"
                            rows={3}
                            value={observacoesGlobais}
                            onChange={(e) => setObservacoesGlobais(e.target.value)}
                        />
                    </div>
                </div>
            ) : (
                <div className="mt-12 animate-fade-in">
                    <h3 className="text-2xl font-bold text-slate-800 mb-6 flex items-center gap-2">🛠️ Artesão de Aulas</h3>
                    
                    <div className="space-y-8">
                    {aulasManuais.map((bloco, idx) => (
                        <div key={idx} className="border border-slate-300 bg-white shadow-sm p-6 rounded-2xl relative">
                            <div className="absolute -top-4 -left-4 bg-blue-600 text-white w-10 h-10 flex items-center justify-center rounded-full font-black text-lg border-4 border-slate-50 shadow">
                                {idx + 1}
                            </div>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6 mt-2">
                                <div>
                                    <label className="block text-sm font-bold text-slate-700 mb-2">Título da Aula (Tema)</label>
                                    <input 
                                        type="text" 
                                        className="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500" 
                                        placeholder="Ex: Introdução à Dinâmica"
                                        value={bloco.titulo}
                                        onChange={(e) => { const n = [...aulasManuais]; n[idx].titulo = e.target.value; setAulasManuais(n); }}
                                    />
                                </div>
                                {formatoCriacao === "desenhar_aula" && (
                                    <div>
                                        <label className="block text-sm font-bold text-slate-700 mb-2">Arquivo Base da Aula (PDF único)</label>
                                        <div className="flex items-center gap-2">
                                            <input 
                                                type="file" accept=".pdf" className="hidden"
                                                ref={el => { fileInputRefs.current[idx] = el; }}
                                                onChange={(e) => { if (e.target.files && e.target.files[0]) handleBlocoFileUpload(idx, e.target.files[0]); }}
                                            />
                                            <button 
                                                onClick={() => fileInputRefs.current[idx]?.click()}
                                                className="bg-slate-100 border border-slate-300 text-slate-700 px-4 py-3 rounded-lg text-sm font-bold hover:bg-slate-200 flex-1 flex justify-center items-center transition"
                                                disabled={bloco.uploading}
                                            >
                                                {bloco.uploading ? "Lendo..." : "📎 Escolher PDF"}
                                            </button>
                                        </div>
                                        {bloco.nome_arquivo && <p className="text-xs text-green-600 mt-2 font-bold px-2">✓ {bloco.nome_arquivo}</p>}
                                    </div>
                                )}
                            </div>
                            
                            {formatoCriacao === "desenhar_aula" && (
                                <>
                                    <div className="mb-6">
                                        <label className="block text-sm font-bold text-slate-700 mb-2">Diretrizes / O que cobrir?</label>
                                        <textarea 
                                            className="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500" 
                                            rows={2}
                                            placeholder="Ex: Explicar detalhadamente a segunda lei de Newton com exemplos do dia a dia."
                                            value={bloco.descricao}
                                            onChange={(e) => { const n = [...aulasManuais]; n[idx].descricao = e.target.value; setAulasManuais(n); }}
                                        />
                                    </div>

                                    <div className="flex flex-col gap-4 p-4 bg-slate-50 border border-slate-200 rounded-xl">
                                        <div>
                                            <label className="flex items-center gap-2 font-bold text-slate-800 cursor-pointer">
                                                <input type="checkbox" checked={bloco.gerar_exercicios} onChange={(e) => { const n = [...aulasManuais]; n[idx].gerar_exercicios = e.target.checked; setAulasManuais(n); }} className="w-4 h-4" />
                                                Gerar Exercícios ao Final
                                            </label>
                                            {bloco.gerar_exercicios && (
                                                <input 
                                                    type="text" 
                                                    placeholder="Sugestões? (Ex: 3 abertas, 2 múltipla escolha sobre atrito). Deixe em branco p/ IA decidir."
                                                    className="w-full mt-2 p-2 border border-slate-300 rounded text-sm"
                                                    value={bloco.sugestoes_exercicios}
                                                    onChange={(e) => { const n = [...aulasManuais]; n[idx].sugestoes_exercicios = e.target.value; setAulasManuais(n); }}
                                                />
                                            )}
                                        </div>
                                        <hr className="border-slate-200" />
                                        <div>
                                            <label className="flex items-center gap-2 font-bold text-slate-800 cursor-pointer">
                                                <input type="checkbox" checked={bloco.gerar_simulador} onChange={(e) => { const n = [...aulasManuais]; n[idx].gerar_simulador = e.target.checked; setAulasManuais(n); }} className="w-4 h-4" />
                                                Injetar Simulador Interativo
                                            </label>
                                            {bloco.gerar_simulador && (
                                                <input 
                                                    type="text" 
                                                    placeholder="Onde ou sobre o que? (Ex: Mostrar um bloco deslizando). Deixe em branco p/ IA decidir."
                                                    className="w-full mt-2 p-2 border border-slate-300 rounded text-sm"
                                                    value={bloco.sugestoes_simulador}
                                                    onChange={(e) => { const n = [...aulasManuais]; n[idx].sugestoes_simulador = e.target.value; setAulasManuais(n); }}
                                                />
                                            )}
                                        </div>
                                    </div>
                                </>
                            )}
                        </div>
                    ))}
                    </div>
                    
                    <button onClick={addBloco} className="mt-8 w-full py-4 border-2 border-dashed border-blue-400 text-blue-600 font-black text-lg rounded-2xl hover:bg-blue-50 transition shadow-sm">
                        ➕ ADICIONAR PRÓXIMA AULA
                    </button>
                </div>
            )}

            <div className="mt-8 mb-4">
                <label className="flex items-center gap-3 p-4 border border-slate-300 rounded-xl bg-white cursor-pointer hover:bg-slate-50 transition-colors shadow-sm">
                    <input 
                    type="checkbox" 
                    checked={aulasComplementares}
                    onChange={(e) => setAulasComplementares(e.target.checked)}
                    className="w-5 h-5 text-indigo-600 rounded"
                    />
                    <div>
                    <span className="block font-bold text-slate-800">Permitir Aprofundamento / Aulas Complementares</span>
                    <span className="text-sm text-slate-500">Se ativo, a IA poderá criar blocos extras para fixação ou aprofundamento ao final do cronograma.</span>
                    </div>
                </label>
            </div>

            <div className="pt-8 mt-4 border-t border-slate-200 flex justify-end gap-4">
                <button 
                  onClick={() => router.push("/professor/dashboard")}
                  className="px-8 py-4 rounded-xl font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 transition"
                >
                  Cancelar
                </button>
                <button 
                  onClick={handleSubmit}
                  disabled={submitting}
                  className="flex-1 max-w-sm bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-black text-lg shadow-xl transition-all flex justify-center items-center gap-2"
                >
                  {submitting ? "Processando..." : "Construir Semestre 🚀"}
                </button>
            </div>
        </div>
      </main>
    </div>
  );
}
