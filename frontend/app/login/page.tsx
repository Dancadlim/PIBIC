"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { auth, db } from "@/lib/firebase";
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from "firebase/auth";
import { doc, setDoc, getDoc } from "firebase/firestore";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [role, setRole] = useState<"aluno" | "professor">("aluno");
  
  // Novos campos para cadastro
  const [nome, setNome] = useState("");
  const [curso, setCurso] = useState("Estatística");
  const [departamento, setDepartamento] = useState("Departamento de Estatística");
  
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isLogin) {
        // Fluxo de Login
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const userDoc = await getDoc(doc(db, "users", userCredential.user.uid));
        
        if (userDoc.exists()) {
          const userData = userDoc.data();
          if (userData.role === "professor") {
            router.push("/professor/dashboard");
          } else {
            router.push("/aluno/dashboard");
          }
        } else {
          // Fallback se não tiver documento (ex: usuários antigos do MVP)
          if (email.includes("@ufba.br") || email.includes("professor")) {
            router.push("/professor/dashboard");
          } else {
            router.push("/aluno/dashboard");
          }
        }

      } else {
        // Fluxo de Criação de Conta
        if (!nome.trim()) throw new Error("O nome é obrigatório.");

        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const uid = userCredential.user.uid;

        const userData = {
          nome,
          email,
          role,
          ...(role === "aluno" ? { curso } : { departamento })
        };

        // Salvar dados estendidos no Firestore
        await setDoc(doc(db, "users", uid), userData);

        if (role === "professor") {
          router.push("/professor/dashboard");
        } else {
          router.push("/aluno/dashboard");
        }
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Erro na autenticação.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full p-8 bg-white rounded-xl shadow-lg border border-slate-200">
        <h2 className="text-3xl font-extrabold text-blue-900 text-center mb-6">
          Plataforma UFBA
        </h2>
        <p className="text-slate-500 text-center mb-8">
          {isLogin ? "Acesse sua conta para continuar." : "Crie sua conta para acessar o sistema."}
        </p>

        {error && <div className="bg-red-50 text-red-500 p-3 rounded-md text-sm text-center mb-4">{error}</div>}

        {!isLogin && (
          <div className="flex bg-slate-100 rounded-lg p-1 mb-6">
            <button
              type="button"
              onClick={() => setRole("aluno")}
              className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${role === "aluno" ? "bg-white text-blue-800 shadow" : "text-slate-500 hover:text-slate-700"}`}
            >
              Sou Aluno
            </button>
            <button
              type="button"
              onClick={() => setRole("professor")}
              className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${role === "professor" ? "bg-white text-blue-800 shadow" : "text-slate-500 hover:text-slate-700"}`}
            >
              Sou Professor
            </button>
          </div>
        )}

        <form onSubmit={handleAuth} className="space-y-4">
          {!isLogin && (
            <>
              <div>
                <label className="block text-sm font-medium text-slate-700">Nome Completo</label>
                <input
                  type="text"
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 text-black"
                  required
                />
              </div>
              
              {role === "aluno" ? (
                <div>
                  <label className="block text-sm font-medium text-slate-700">Curso na UFBA</label>
                  <select 
                    value={curso} 
                    onChange={(e) => setCurso(e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 text-black"
                  >
                    <option value="Estatística">Estatística</option>
                    <option value="Ciência da Computação">Ciência da Computação</option>
                    <option value="Sistemas de Informação">Sistemas de Informação</option>
                    <option value="Engenharia Civil">Engenharia Civil</option>
                    <option value="Matemática">Matemática</option>
                  </select>
                </div>
              ) : (
                <div>
                  <label className="block text-sm font-medium text-slate-700">Unidade / Departamento</label>
                  <select 
                    value={departamento} 
                    onChange={(e) => setDepartamento(e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 text-black"
                  >
                    <option value="Departamento de Estatística">Departamento de Estatística</option>
                    <option value="Departamento de Ciência da Computação (DCC)">Departamento de Ciência da Computação (DCC)</option>
                    <option value="Instituto de Matemática e Estatística (IME)">Instituto de Matemática e Estatística (IME)</option>
                  </select>
                </div>
              )}
            </>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700">Email Institucional (@ufba.br)</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 text-black"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700">Senha</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 text-black"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-800 hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
          >
            {loading ? "Aguarde..." : isLogin ? "Entrar no Sistema" : "Criar Minha Conta"}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button
            onClick={() => {
              setIsLogin(!isLogin);
              setError("");
            }}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            {isLogin ? "Primeiro acesso? Crie sua conta UFBA" : "Já possui cadastro? Faça o Login"}
          </button>
        </div>
      </div>
    </div>
  );
}
