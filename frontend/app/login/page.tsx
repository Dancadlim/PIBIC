"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { auth, db } from "@/lib/firebase";
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";
import { doc, setDoc, getDoc } from "firebase/firestore";

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    const autoLogin = async () => {
      try {
        await signInWithEmailAndPassword(auth, "professor@teste.com", "teste123");
        // Login com sucesso, vai redirecionar pelo onAuthStateChanged abaixo
      } catch (err: any) {
        // Se a conta não existir, vamos criar na hora
        if (err.code === "auth/user-not-found" || err.code === "auth/invalid-credential" || err.code === "auth/invalid-login-credentials") {
          try {
            const userCred = await createUserWithEmailAndPassword(auth, "professor@teste.com", "teste123");
            await setDoc(doc(db, "users", userCred.user.uid), {
              nome: "Professor Teste",
              email: "professor@teste.com",
              role: "professor",
              departamento: "Departamento de Estatística"
            });
          } catch (createErr) {
            console.error("Erro ao criar conta de teste:", createErr);
          }
        } else {
          console.error("Erro no auto-login:", err);
        }
      }
    };

    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        // Se já está logado ou acabou de logar
        const userDoc = await getDoc(doc(db, "users", user.uid));
        if (userDoc.exists() && userDoc.data().role === "aluno") {
          router.push("/aluno/dashboard");
        } else {
          router.push("/professor/dashboard");
        }
      } else {
        // Se não tiver logado, dispara a rotina de auto-login
        autoLogin();
      }
    });

    return () => unsubscribe();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full p-8 bg-white rounded-xl shadow-lg border border-slate-200 text-center">
        <h2 className="text-3xl font-extrabold text-blue-900 mb-6">
          Plataforma UFBA
        </h2>
        <div className="animate-pulse flex flex-col items-center">
          <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-slate-500 font-bold">
            Entrando automaticamente como Professor Teste...
          </p>
        </div>
      </div>
    </div>
  );
}
