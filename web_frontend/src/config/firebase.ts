import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { logger } from '../utils/logger';
import { connectDataConnectEmulator, getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@firebasegen/news-connector';
import { getAuth } from 'firebase/auth';

function validateConfig() {
  const requiredEnvVars = [
    'VITE_FIREBASE_API_KEY',
    'VITE_FIREBASE_AUTH_DOMAIN',
    'VITE_FIREBASE_PROJECT_ID',
    'VITE_FIREBASE_STORAGE_BUCKET',
    'VITE_FIREBASE_MESSAGING_SENDER_ID',
    'VITE_FIREBASE_APP_ID',
  ];

  const missingVars = requiredEnvVars.filter(
    (varName) => !import.meta.env[varName]
  );

  if (missingVars.length > 0) {
    throw new Error(
      `Missing required Firebase configuration: ${missingVars.join(', ')}`
    );
  }
}

function initializeFirebase() {
  try {
    validateConfig();

    const projectId = import.meta.env.VITE_FIREBASE_PROJECT_ID;

    logger.debug('Initializing Firebase with configuration', {
      projectId,
      authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
    });

    const firebaseConfig = {
      apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
      authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
      projectId: projectId,
      storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
      messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
      appId: import.meta.env.VITE_FIREBASE_APP_ID,
    };

    const app = initializeApp(firebaseConfig);
    logger.info(app.name);
    logger.info('Firebase initialized successfully');

    return app;
  } catch (error) {
    logger.error('Failed to initialize Firebase:', error);
    throw error;
  }
}

let db: ReturnType<typeof getFirestore>;
let dataconnect: ReturnType<typeof getDataConnect>;
try {
  let app = initializeFirebase();
  db = getFirestore(app)
  dataconnect = getDataConnect(app, connectorConfig)
} catch (error) {
  logger.error('Failed to initialize Firebase at module level:', error);
  // Instead of throwing, we might want to provide a fallback or handle gracefully
  db = null as any; // or some fallback/mock implementation
}

export { db, dataconnect };
