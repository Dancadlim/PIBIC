"use client";

import { useState, useEffect } from "react";
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
  const [maxAulas, setMaxAulas] = useState(3);
  const [classCode, setClassCode] = useState<string | null>(null);
  
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
          const discList = discSnapshot.docs.map(d => ({ id: d.id, ...d.data() }));
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
    if (mode === "livre") return alert("Modo 'Criar do seu jeito' será implementado na Fase 2.");
    
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
        await fetch("http://localhost:8000/api/gerar_semestre", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id_sala: docRef.id,
            id_disciplina: selectedDisciplina,
            modo: mode,
            instrucoes_personalizadas: "",
            max_aulas: maxAulas 
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
            onClick={() => { setView("list"); setClassCode(null); }}
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
                          onClick={() => router.push(`/aluno/aula/${sala.id}`)}
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

                  <label className="block text-sm font-bold text-slate-700 mb-2">Quantas aulas deseja gerar no máximo?</label>
                  <select
                    className="w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-800 bg-slate-50"
                    value={maxAulas}
                    onChange={(e) => setMaxAulas(Number(e.target.value))}
                  >
                    <option value={3}>3 aulas (Teste Rápido)</option>
                    <option value={5}>5 aulas (Teste Médio)</option>
                    <option value={10}>10 aulas (Parcial)</option>
                    <option value={30}>30 aulas (Semestre Completo)</option>
                  </select>
                </div>

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
