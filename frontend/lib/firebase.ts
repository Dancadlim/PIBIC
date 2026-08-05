import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyBKt99lfFfW1MeSNwqxtU66x8eqV0nGI88",
  authDomain: "plataforma-aulas-ufba.firebaseapp.com",
  projectId: "plataforma-aulas-ufba",
  storageBucket: "plataforma-aulas-ufba.firebasestorage.app",
  messagingSenderId: "838145348800",
  appId: "1:838145348800:web:a76e45f35d62657bc7c925",
  measurementId: "G-NSBFDC8E38"
};

// Initialize Firebase (Singleton pattern para Next.js)
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
