"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { auth, db } from "@/lib/firebase";
import { signOut, onAuthStateChanged } from "firebase/auth";
import { collection, addDoc, serverTimestamp, getDocs, doc, getDoc, query, where, orderBy, deleteDoc, onSnapshot } from "firebase/firestore";

export default function ProfessorDashboard() {
  const router = useRouter();
  
  // User Profile
  const [professorName, setProfessorName] = useState("");
  const [professorDept, setProfessorDept] = useState("");

  // States
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<"list" | "create">("list");
  const [selectedDisciplina, setSelectedDisciplina] = useState("MAT186");
  const [limiteExecucao, setLimiteExecucao] = useState(3);
  const [tipoCargaHoraria, setTipoCargaHoraria] = useState("padrao_30");
  const [permitirAprofundamento, setPermitirAprofundamento] = useState(false);
  const [classCode, setClassCode] = useState<string | null>(null);

  // States para "Crie do Seu Jeito"
  const [modoCriacao, setModoCriacao] = useState<"selecao" | "livre">("selecao");
  const [tipoCrieSeuJeito, setTipoCrieSeuJeito] = useState<"automatico" | "bloco_a_bloco">("bloco_a_bloco");
  const [arquivoGlobalPdf, setArquivoGlobalPdf] = useState("");
  const [arquivoGlobalNome, setArquivoGlobalNome] = useState("");
  const [uploadingGlobal, setUploadingGlobal] = useState(false);
  const globalPdfRef = useRef<HTMLInputElement>(null);

  const [tomPersonalidade, setTomPersonalidade] = useState("");
  const [nivelExercicios, setNivelExercicios] = useState("");
  const [observacoesAdicionais, setObservacoesAdicionais] = useState("");
  
  // Estado dos Blocos Manuais
  const [aulasManuais, setAulasManuais] = useState<any[]>([{
    id: 1,
    titulo: "",
    descricao: "",
    texto_base_pdf: "",
    nome_arquivo: "",
    gerar_exercicios: true,
    gerar_simulador: false,
    uploading: false
  }]);

  const fileInputRefs = useRef<any>({});
  
  const handleFileUpload = async (index: number, file: File) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      alert("Somente arquivos PDF são suportados no momento.");
      return;
    }
    const updated = [...aulasManuais];
    updated[index].uploading = true;
    setAulasManuais(updated);

    const formData = new FormData();
    formData.append("files", file);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/upload_pdf`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        const nextUpdated = [...aulasManuais];
        nextUpdated[index].texto_base_pdf = data.texto_extraido;
        nextUpdated[index].nome_arquivo = file.name;
        nextUpdated[index].uploading = false;
        setAulasManuais(nextUpdated);
      } else {
        alert("Erro no upload: " + data.detail);
        const nextUpdated = [...aulasManuais];
        nextUpdated[index].uploading = false;
        setAulasManuais(nextUpdated);
      }
    } catch (e) {
      alert("Erro na rede ao enviar PDF");
      const nextUpdated = [...aulasManuais];
      nextUpdated[index].uploading = false;
      setAulasManuais(nextUpdated);
    }
  };

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

  const addBloco = () => {
    setAulasManuais([...aulasManuais, {
      id: aulasManuais.length + 1,
      titulo: "",
      descricao: "",
      texto_base_pdf: "",
      nome_arquivo: "",
      gerar_exercicios: true,
      gerar_simulador: false,
      uploading: false
    }]);
  };
  
  // Data
  const [minhasSalas, setMinhasSalas] = useState<any[]>([]);
  const [disciplinas, setDisciplinas] = useState<any[]>([]);

  useEffect(() => {
    let unsubscribeSalas: (() => void) | undefined;

    const unsubscribeAuth = onAuthStateChanged(auth, async (user) => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        // 1. Buscar Perfil do Professor
        const userDoc = await getDoc(doc(db, "users", user.uid));
        if (userDoc.exists()) {
          setProfessorName(userDoc.data().nome);
          setProfessorDept(userDoc.data().departamento);
        }

        // 2. Buscar Salas em TEMPO REAL (onSnapshot)
        const qSalas = query(
          collection(db, "classrooms"), 
          where("teacherId", "==", user.uid),
          orderBy("createdAt", "desc")
        );
        
        unsubscribeSalas = onSnapshot(qSalas, (snapshot) => {
          const salasList = snapshot.docs.map(d => ({ id: d.id, ...d.data() }));
          setMinhasSalas(salasList);
        }, (error) => {
          console.warn("Aviso: Índice de salas ainda construindo. As turmas aparecerão em breve.");
        });

        // 3. Buscar Disciplinas disponíveis no Banco
        try {
          const discSnapshot = await getDocs(collection(db, "disciplinas"));
          const discList = discSnapshot.docs.map(d => ({ id: d.id, ...(d.data() as any) }));
          setDisciplinas(discList);
          if (discList.length > 0) setSelectedDisciplina(discList[0].id_disciplina);
        } catch (error) {
          console.error("Erro ao carregar disciplinas:", error);
        }

      } catch (error) {
        console.error("Erro ao carregar dados do dashboard:", error);
      } finally {
        setLoading(false);
      }
    });

    return () => {
      unsubscribeAuth();
      if (unsubscribeSalas) unsubscribeSalas();
    };
  }, []);

  const handleLogout = async () => {
    await signOut(auth);
    router.push("/login");
  };

  const deleteClassroom = async (salaId: string) => {
    if (confirm("Tem certeza que deseja apagar esta sala?")) {
      try {
        await deleteDoc(doc(db, "classrooms", salaId));
        setMinhasSalas(minhasSalas.filter(s => s.id !== salaId));
      } catch (e) {
        console.error("Erro ao apagar sala:", e);
        alert("Erro ao apagar sala.");
      }
    }
  };

  const createClassroom = async (mode: "inteligente" | "livre") => {
    if (!selectedDisciplina) return alert("Selecione uma disciplina.");
    
    // Se escolheu 'livre' direto da seleção, abre o formulário
    if (mode === "livre" && modoCriacao === "selecao") {
      if (tipoCargaHoraria === "manual") {
          setTipoCrieSeuJeito("bloco_a_bloco");
      }
      setModoCriacao("livre");
      return;
    }

    setLoading(true);
    try {
      const code = Math.floor(1000 + Math.random() * 9000).toString();
      const disc = disciplinas.find(d => d.id_disciplina === selectedDisciplina);

      // Salva a "Sala do Semestre" no Firestore
      const docRef = await addDoc(collection(db, "classrooms"), {
        code,
        teacherId: auth.currentUser?.uid,
        id_disciplina: selectedDisciplina,
        nome_disciplina: disc?.nome || "Disciplina",
        createdAt: serverTimestamp(),
        status: "creating_semester" // Novo status: criando cronograma do semestre
      });

      setClassCode(code);
      
      // Chamada para a API Python geradora do semestre (Nível 2)
      // Usaremos max_aulas=3 por padrão para travar custos durante testes
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        await fetch(`${apiUrl}/api/gerar_semestre`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id_sala: docRef.id,
            id_disciplina: selectedDisciplina,
            modo: mode,
            instrucoes_personalizadas: mode === "livre" ? 
              `Tom/Personalidade: ${tomPersonalidade}\nNível Exercícios: ${nivelExercicios}\nObservações: ${observacoesAdicionais}` 
              : "",
            max_aulas: 30, // Sempre passa 30 para o Roteirista arquitetar o semestre cheio
            limite_execucao: limiteExecucao,
            tipo_carga_horaria: tipoCargaHoraria,
            permitir_aprofundamento: permitirAprofundamento,
            tipo_crie_seu_jeito: tipoCrieSeuJeito,
            arquivo_global_pdf: arquivoGlobalPdf,
            aulas_manuais: mode === "livre" ? aulasManuais.map(a => ({
                titulo: a.titulo || "Sem título",
                descricao: a.descricao || "Sem descrição",
                texto_base_pdf: a.texto_base_pdf || "",
                gerar_exercicios: a.gerar_exercicios,
                gerar_simulador: a.gerar_simulador
            })) : []
          })
        });
      } catch (e) {
        console.error("Erro ao chamar API de geração:", e);
      }

    } catch (error) {
      console.error("Erro ao criar sala:", error);
      alert("Erro ao criar a sala.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-slate-500">Carregando painel...</div>;
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      <nav className="bg-blue-900 text-white px-6 py-4 flex justify-between items-center shadow-md">
        <div>
          <h1 className="text-xl font-bold">Painel do Professor</h1>
          <p className="text-xs text-blue-200">{professorName} | {professorDept}</p>
        </div>
        <button onClick={handleLogout} className="text-sm bg-blue-800 px-4 py-2 rounded hover:bg-blue-700 transition">Sair</button>
      </nav>

      <main className="max-w-5xl mx-auto mt-8 p-6">
        
        {/* Hub de Navegação */}
        <div className="flex gap-4 mb-8">
          <button 
            onClick={() => { setView("list"); setClassCode(null); setModoCriacao("selecao"); }}
            className={`px-6 py-2 rounded-full font-medium transition ${view === "list" ? "bg-blue-600 text-white" : "bg-white text-slate-600 border border-slate-300"}`}
          >
            📚 Minhas Turmas Ativas
          </button>
          <button 
            onClick={() => setView("create")}
            className={`px-6 py-2 rounded-full font-medium transition ${view === "create" ? "bg-blue-600 text-white" : "bg-white text-slate-600 border border-slate-300"}`}
          >
            ✨ Gerar Novo Semestre
          </button>
        </div>

        {/* View: Lista de Turmas */}
        {view === "list" && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-slate-800 mb-6">Salas e Semestres Gerenciados</h2>
            
            {minhasSalas.length === 0 ? (
              <div className="text-center py-12 bg-slate-50 rounded-lg border border-dashed border-slate-300">
                <p className="text-slate-500 mb-4">Você ainda não gerou nenhuma turma para este semestre.</p>
                <button onClick={() => setView("create")} className="text-blue-600 font-medium hover:underline">
                  Gerar sua primeira turma agora
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {minhasSalas.map(sala => (
                  <div key={sala.id} className="border border-slate-200 rounded-lg p-5 hover:shadow-md transition-shadow bg-white flex flex-col">
                    <div className="flex justify-between items-start mb-2">
                      <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded">
                        Código: {sala.code}
                      </span>
                      <span className="text-xs text-slate-400">
                        {sala.createdAt ? new Date(sala.createdAt.toDate()).toLocaleDateString() : 'Recente'}
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-slate-800 mt-2">{sala.id_disciplina}</h3>
                    <p className="text-sm text-slate-500 flex-1">{sala.nome_disciplina}</p>
                    
                    <div className="mt-4 pt-4 border-t border-slate-100 flex flex-col gap-3">
                      {sala.status === "gerando_aulas" && (
                        <div>
                          <div className="flex justify-between text-xs text-blue-600 mb-1 font-semibold">
                            <span>Gerando Aulas...</span>
                            <span>{sala.aulas_geradas || 0} / {sala.total_aulas || '?'}</span>
                          </div>
                          <div className="w-full bg-slate-200 rounded-full h-2">
                            <div className="bg-blue-600 h-2 rounded-full transition-all duration-500" style={{ width: `${Math.min(100, ((sala.aulas_geradas || 0) / (sala.total_aulas || 1)) * 100)}%` }}></div>
                          </div>
                        </div>
                      )}
                      
                      {sala.status === "pronto" && (
                        <div className="p-2 bg-green-50 border border-green-200 rounded text-green-700 text-xs font-bold text-center">
                          ✅ Aulas criadas com sucesso!
                        </div>
                      )}
                      
                      {sala.status?.startsWith("erro") && (
                        <div className="p-2 bg-red-50 border border-red-200 rounded text-red-700 text-xs font-bold text-center">
                          ❌ Falha na Geração: {sala.status}
                        </div>
                      )}

                      <div className="flex justify-between gap-2 mt-2">
                        <button 
                          onClick={() => router.push(`/professor/aula/${sala.id}`)}
                          className="flex-1 text-sm bg-slate-100 text-slate-700 py-2 rounded hover:bg-slate-200 transition font-medium"
                        >
                          📊 Acessar Sala
                        </button>
                        <button className="text-sm text-blue-600 hover:text-blue-800 px-2" title="Copiar Sala para outra turma">
                          Copiar
                        </button>
                        <button onClick={() => deleteClassroom(sala.id)} className="text-sm text-red-600 hover:text-red-800 px-2" title="Apagar Turma">
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* View: Criar Semestre */}
        {view === "create" && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-slate-800 mb-2">Construir Semestre Inteiro</h2>
            <p className="text-slate-500 mb-8">Selecione a disciplina. Nossa IA montará o cronograma e todas as aulas do semestre.</p>

            {!classCode ? (
              <div className="max-w-2xl">
                <div className="mb-8">
                  <label className="block text-sm font-bold text-slate-700 mb-2">Disciplina da Grade Oficial</label>
                  <select
                    className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-800 bg-slate-50 mb-6"
                    value={selectedDisciplina}
                    onChange={(e) => setSelectedDisciplina(e.target.value)}
                  >
                    {disciplinas.map((d) => (
                      <option key={d.id_disciplina} value={d.id_disciplina}>
                        {d.id_disciplina} - {d.nome}
                      </option>
                    ))}
                  </select>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Carga Horária / Quantidade de Aulas</label>
                      <select
                        className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-800 bg-slate-50"
                        value={tipoCargaHoraria}
                        onChange={(e) => setTipoCargaHoraria(e.target.value)}
                      >
                        <option value="padrao_30">Padrão 30 Aulas</option>
                        <option value="auto_ementa">Auto (via CH da Ementa: 30, 45, 60, 90h)</option>
                        <option value="manual">Manual (Aulas definidas abaixo)</option>
                      </select>
                    </div>
                    {tipoCargaHoraria !== "manual" && (
                      <div>
                        <label className="block text-sm font-bold text-slate-700 mb-2">Limite (Apenas para Testes Rápidos)</label>
                        <select
                          className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-800 bg-slate-50"
                          value={limiteExecucao}
                          onChange={(e) => setLimiteExecucao(Number(e.target.value))}
                        >
                          <option value={1}>Executar 1 aula (Teste Mega Rápido)</option>
                          <option value={3}>Executar 3 aulas (Teste Rápido)</option>
                          <option value={5}>Executar 5 aulas (Teste Médio)</option>
                          <option value={30}>Executar Todas (Semestre Completo)</option>
                        </select>
                      </div>
                    )}
                  </div>

                  <div className="mb-6">
                    <label className="flex items-center gap-3 p-4 border border-slate-300 rounded-xl bg-white cursor-pointer hover:bg-slate-50">
                      <input 
                        type="checkbox" 
                        checked={permitirAprofundamento}
                        onChange={(e) => setPermitirAprofundamento(e.target.checked)}
                        className="w-5 h-5 text-blue-600 rounded"
                      />
                      <div>
                        <span className="block font-bold text-slate-800">Permitir Aulas Complementares de Aprofundamento</span>
                        <span className="text-sm text-slate-500">A IA poderá gerar até 5 aulas extras fora da ementa para aprofundar temas difíceis.</span>
                      </div>
                    </label>
                  </div>
                </div>

                {modoCriacao === "selecao" ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Botão A: 100% Ementa */}
                  <div className="border border-slate-200 rounded-xl p-6 hover:border-blue-400 transition-colors cursor-pointer group" onClick={() => createClassroom("inteligente")}>
                    <div className="text-3xl mb-3">✨</div>
                    <h3 className="font-bold text-slate-800 text-lg mb-2 group-hover:text-blue-600">Criar Sala Inteligente</h3>
                    <p className="text-sm text-slate-500">A IA construirá todo o semestre utilizando estritamente a ementa e a bibliografia oficial cadastrada no sistema.</p>
                  </div>

                  {/* Botão B: Personalizado */}
                  <div className="border border-slate-200 rounded-xl p-6 hover:border-blue-400 transition-colors cursor-pointer group" onClick={() => createClassroom("livre")}>
                    <div className="text-3xl mb-3">✏️</div>
                    <h3 className="font-bold text-slate-800 text-lg mb-2 group-hover:text-blue-600">Criar do Seu Jeito</h3>
                    <p className="text-sm text-slate-500">Faça upload de seus slides, notas de aula e digite diretrizes para a IA priorizar o seu próprio material.</p>
                  </div>
                  </div>
                ) : (
                  <div className="mt-8 border-t border-slate-200 pt-8 animate-fade-in">
                    <h3 className="text-xl font-bold text-blue-900 mb-6 flex items-center gap-2">
                      <span>✏️</span> Configurações do "Crie do Seu Jeito"
                    </h3>
                    
                    <div className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-bold text-slate-700 mb-2">Tom e Personalidade do Conteúdo / Chatbot</label>
                          <textarea
                            placeholder="Ex: Quero um tom provocativo, estilo professor descolado..."
                            className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-800 bg-white"
                            rows={3}
                            value={tomPersonalidade}
                            onChange={(e) => setTomPersonalidade(e.target.value)}
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-bold text-slate-700 mb-2">Nível e Foco dos Exercícios</label>
                          <textarea
                            placeholder="Ex: Nível de dificuldade alto estilo ENADE..."
                            className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-800 bg-white"
                            rows={3}
                            value={nivelExercicios}
                            onChange={(e) => setNivelExercicios(e.target.value)}
                          />
                        </div>
                      </div>

                      <div className="flex gap-4 border-b border-slate-200 pb-2 mt-8">
                        <button
                          onClick={() => setTipoCrieSeuJeito("automatico")}
                          className={`pb-2 px-2 font-bold transition-colors ${tipoCrieSeuJeito === "automatico" ? "text-blue-600 border-b-2 border-blue-600" : "text-slate-500 hover:text-slate-800"}`}
                        >
                          Plano Automático (Arquivo Único)
                        </button>
                        <button
                          onClick={() => setTipoCrieSeuJeito("bloco_a_bloco")}
                          className={`pb-2 px-2 font-bold transition-colors ${tipoCrieSeuJeito === "bloco_a_bloco" ? "text-blue-600 border-b-2 border-blue-600" : "text-slate-500 hover:text-slate-800"}`}
                        >
                          Manual (Aula a Aula)
                        </button>
                      </div>

                      {tipoCrieSeuJeito === "automatico" && (
                        <div className="mt-8 bg-blue-50 border border-blue-200 p-6 rounded-xl">
                          <h4 className="text-lg font-bold text-blue-900 mb-2">Despejo Global de Material</h4>
                          <p className="text-sm text-blue-700 mb-4">A IA vai ler o PDF completo e decidir como quebrar as aulas sozinha, baseado na quantidade de aulas que você definiu nas Configurações da Turma.</p>
                          
                          <input type="file" ref={globalPdfRef} className="hidden" accept=".pdf" multiple onChange={e => handleGlobalFileUpload(e.target.files)} />
                          <button 
                            onClick={() => globalPdfRef.current?.click()}
                            className="bg-blue-600 text-white px-6 py-3 rounded font-bold shadow hover:bg-blue-700 transition w-full md:w-auto flex justify-center items-center gap-2"
                            disabled={uploadingGlobal}
                          >
                            {uploadingGlobal ? "Analisando PDF..." : "📎 Anexar Livro/Apostila Completa (PDF)"}
                          </button>
                          {arquivoGlobalNome && <p className="text-green-700 mt-3 font-bold">✓ {arquivoGlobalNome} processado com sucesso!</p>}
                        </div>
                      )}

                      {tipoCrieSeuJeito === "bloco_a_bloco" && (
                        <div className="mt-8">
                          <h4 className="text-lg font-bold text-slate-800 mb-4">Blocos de Aula Personalizados</h4>
                          <div className="space-y-4">
                          {aulasManuais.map((bloco, idx) => (
                            <div key={idx} className="border border-slate-300 bg-slate-50 p-6 rounded-xl relative">
                              <div className="absolute top-4 right-4 bg-slate-200 text-slate-600 px-2 py-1 text-xs rounded font-bold">Aula {idx + 1}</div>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                <div>
                                  <label className="block text-xs font-bold text-slate-600 mb-1">Título da Aula</label>
                                  <input 
                                    type="text" 
                                    className="w-full p-2 border border-slate-300 rounded" 
                                    placeholder="Ex: Limites e Continuidade"
                                    value={bloco.titulo}
                                    onChange={(e) => { const n = [...aulasManuais]; n[idx].titulo = e.target.value; setAulasManuais(n); }}
                                  />
                                </div>
                                <div>
                                  <label className="block text-xs font-bold text-slate-600 mb-1">Upload de PDF (Slide/Apostila)</label>
                                  <div className="flex items-center gap-2">
                                    <input 
                                      type="file" 
                                      accept=".pdf"
                                      className="hidden"
                                      ref={el => fileInputRefs.current[idx] = el}
                                      onChange={(e) => {
                                        if (e.target.files && e.target.files[0]) handleFileUpload(idx, e.target.files[0]);
                                      }}
                                    />
                                    <button 
                                      onClick={() => fileInputRefs.current[idx]?.click()}
                                      className="bg-slate-200 text-slate-700 px-4 py-2 rounded text-sm hover:bg-slate-300 flex-1 flex justify-center items-center gap-2"
                                      disabled={bloco.uploading}
                                    >
                                      {bloco.uploading ? "Extraindo texto..." : "📎 Escolher PDF"}
                                    </button>
                                  </div>
                                  {bloco.nome_arquivo && <p className="text-xs text-green-600 mt-1 font-bold">✓ {bloco.nome_arquivo} ({bloco.texto_base_pdf.length} caracteres extraídos)</p>}
                                </div>
                              </div>
                              <div className="mb-4">
                                <label className="block text-xs font-bold text-slate-600 mb-1">Diretrizes/Descrição Específica (O que cobrir?)</label>
                                <textarea 
                                  className="w-full p-2 border border-slate-300 rounded" 
                                  rows={2}
                                  placeholder="Ex: Foque na demonstração do teorema de Rolle. Ignore a parte de L'Hopital pois será dada na Aula 3."
                                  value={bloco.descricao}
                                  onChange={(e) => { const n = [...aulasManuais]; n[idx].descricao = e.target.value; setAulasManuais(n); }}
                                />
                              </div>
                              <div className="flex gap-4">
                                <label className="flex items-center gap-2 text-sm text-slate-700">
                                  <input type="checkbox" checked={bloco.gerar_exercicios} onChange={(e) => { const n = [...aulasManuais]; n[idx].gerar_exercicios = e.target.checked; setAulasManuais(n); }} />
                                  Gerar Exercícios
                                </label>
                                <label className="flex items-center gap-2 text-sm text-slate-700">
                                  <input type="checkbox" checked={bloco.gerar_simulador} onChange={(e) => { const n = [...aulasManuais]; n[idx].gerar_simulador = e.target.checked; setAulasManuais(n); }} />
                                  Propor Simulador
                                </label>
                              </div>
                            </div>
                          ))}
                        </div>
                        <button onClick={addBloco} className="mt-4 w-full py-3 border-2 border-dashed border-blue-300 text-blue-600 font-bold rounded-xl hover:bg-blue-50 transition">
                          + Adicionar Próxima Aula
                        </button>
                        </div>
                      )}

                      <div className="flex gap-4 pt-4 mt-8 border-t border-slate-200">
                        <button 
                          onClick={() => setModoCriacao("selecao")}
                          className="px-6 py-3 rounded-lg font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 transition"
                        >
                          Voltar
                        </button>
                        <button 
                          onClick={() => createClassroom("livre")}
                          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-bold shadow-md transition-all flex justify-center items-center gap-2"
                        >
                          Gerar Semestre Personalizado 🚀
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-8 bg-green-50 border border-green-200 rounded-xl flex flex-col items-center text-center">
                <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-3xl mb-4">✓</div>
                <h3 className="text-green-800 font-bold text-xl mb-2">Sala Criada com Sucesso!</h3>
                <p className="text-slate-600 mb-2 max-w-md">O cronograma do semestre está sendo arquitetado. Compartilhe o código abaixo com seus alunos para eles entrarem no lobby:</p>
                <div className="text-6xl font-mono font-black text-green-700 tracking-widest bg-white px-10 py-5 rounded-2xl shadow-sm border border-green-300 mb-6">
                  {classCode}
                </div>
                
                <div className="bg-white p-4 rounded-lg shadow-sm border border-blue-200 mb-6 max-w-md w-full">
                  <div className="flex items-start">
                    <div className="text-2xl mr-3">🤖</div>
                    <div className="text-left">
                      <h4 className="font-bold text-blue-800 text-sm">Pode fechar esta tela!</h4>
                      <p className="text-xs text-slate-600 mt-1">Os agentes de inteligência artificial já começaram a construir as aulas do semestre nos bastidores. O processo pode levar alguns minutos. Você pode acompanhar a barra de progresso em tempo real na aba <b>Minhas Turmas Ativas</b>.</p>
                    </div>
                  </div>
                </div>

                <button onClick={() => { setView("list"); setClassCode(null); }} className="text-blue-600 font-medium hover:underline px-6 py-2 rounded-full border border-blue-200 hover:bg-blue-50 transition">
                  Ir para Minhas Turmas Ativas
                </button>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
