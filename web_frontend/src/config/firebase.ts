import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

class FirebaseClient {
  private static instance: FirebaseClient;
  private app: ReturnType<typeof initializeApp>;
  private firestore: ReturnType<typeof getFirestore>;

  private constructor() {
    this.validateConfig();
    const firebaseConfig = {
      apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
      authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
      projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
      storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
      messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
      appId: import.meta.env.VITE_FIREBASE_APP_ID
    };

    this.app = initializeApp(firebaseConfig);
    this.firestore = getFirestore(this.app);
  }

  private validateConfig() {
    const requiredEnvVars = [
      'VITE_FIREBASE_API_KEY',
      'VITE_FIREBASE_AUTH_DOMAIN',
      'VITE_FIREBASE_PROJECT_ID',
      'VITE_FIREBASE_STORAGE_BUCKET',
      'VITE_FIREBASE_MESSAGING_SENDER_ID',
      'VITE_FIREBASE_APP_ID'
    ];

    const missingVars = requiredEnvVars.filter(varName => !import.meta.env[varName]);
    
    if (missingVars.length > 0) {
      throw new Error(`Missing required Firebase configuration: ${missingVars.join(', ')}`);
    }
  }

  public static getInstance(): FirebaseClient {
    if (!FirebaseClient.instance) {
      FirebaseClient.instance = new FirebaseClient();
    }
    return FirebaseClient.instance;
  }

  public getFirestore() {
    return this.firestore;
  }
}

export const db = FirebaseClient.getInstance().getFirestore();