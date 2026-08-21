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
  // Removed old form states and handlers (they moved to dedicated pages)
  
  // Data
  const [minhasSalas, setMinhasSalas] = useState<any[]>([]);
  const [disciplinas, setDisciplinas] = useState<any[]>([]);

  useEffect(() => {
    let unsubscribeSalas: (() => void) | undefined;

    // DESVINCULAÇÃO DE LOGIN PARA TESTES
    // const unsubscribeAuth = onAuthStateChanged(auth, async (user) => {
    //   if (!user) {
    //     setLoading(false);
    //     return;
    //   }
    
    const mockUser = { uid: "TEST_PROFESSOR_123" };
    const loadData = async (user: any) => {

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
          // if (discList.length > 0) setSelectedDisciplina(discList[0].id_disciplina);
        } catch (error) {
          console.error("Erro ao carregar disciplinas:", error);
        }

      } catch (error) {
        console.error("Erro ao carregar dados do dashboard:", error);
      } finally {
        setLoading(false);
      }
    };
    
    loadData(mockUser);

    return () => {
      // unsubscribeAuth();
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

  // Removed createClassroom
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
            onClick={() => { setView("list"); }}
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
                          <div className="w-full bg-slate-200 rounded-full h-2 mb-2">
                            <div className="bg-blue-600 h-2 rounded-full transition-all duration-500" style={{ width: `${Math.min(100, ((sala.aulas_geradas || 0) / (sala.total_aulas || 1)) * 100)}%` }}></div>
                          </div>
                          {sala.detalhe_progresso && (
                            <div className="text-[10px] text-slate-500 italic animate-pulse">
                              {sala.detalhe_progresso}
                            </div>
                          )}
                        </div>
                      )}
                      
                      {sala.status === "pronto" && (
                        <div className="p-2 bg-green-50 border border-green-200 rounded text-green-700 text-xs font-bold text-center">
                          ✅ Aulas criadas com sucesso!
                        </div>
                      )}

                      <div className="flex justify-between gap-2 mt-2">
                        <button 
                          onClick={() => router.push(`/professor/aula/${sala.id}`)}
                          className="flex-1 text-sm bg-slate-100 text-slate-700 py-2 rounded hover:bg-slate-200 transition font-medium"
                        >
                          📊 Acessar Sala
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

        {/* View: Hub de Criação (Navega para Páginas Dedicadas) */}
        {view === "create" && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-slate-800 mb-2">Qual tipo de semestre deseja criar?</h2>
            <p className="text-slate-500 mb-8">Nossa plataforma oferece duas experiências diferentes de acordo com a sua necessidade.</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Botão A: Inteligente */}
              <div 
                className="border border-slate-200 rounded-xl p-6 hover:border-blue-400 hover:shadow-md transition-all cursor-pointer group bg-slate-50 hover:bg-blue-50/30" 
                onClick={() => router.push("/professor/criar/inteligente")}
              >
                <div className="text-4xl mb-4">✨</div>
                <h3 className="font-bold text-slate-800 text-xl mb-2 group-hover:text-blue-600">Sala Inteligente</h3>
                <p className="text-sm text-slate-600 mb-4">A IA construirá todo o semestre utilizando estritamente a ementa e a bibliografia oficial cadastrada no sistema. Rápido e padronizado.</p>
                <span className="text-blue-600 font-bold text-sm">Criar Sala Inteligente →</span>
              </div>

              {/* Botão B: Personalizado */}
              <div 
                className="border border-slate-200 rounded-xl p-6 hover:border-blue-400 hover:shadow-md transition-all cursor-pointer group bg-slate-50 hover:bg-blue-50/30" 
                onClick={() => router.push("/professor/criar/personalizado")}
              >
                <div className="text-4xl mb-4">✏️</div>
                <h3 className="font-bold text-slate-800 text-xl mb-2 group-hover:text-blue-600">Crie do Seu Jeito</h3>
                <p className="text-sm text-slate-600 mb-4">Faça upload de seus próprios PDFs, escolha a quantidade exata de aulas, modifique o tom e guie a IA bloco a bloco (ou jogue tudo pra ela).</p>
                <span className="text-blue-600 font-bold text-sm">Criar Sala Personalizada →</span>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
