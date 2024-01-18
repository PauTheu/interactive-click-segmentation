// eslint-disable-next-line
export const backendPrefix = 'http://127.0.0.1:5000';

// eslint-disable-next-line
export const oneshotBackendPrefix = process.env.NODE_ENV === 'development' ? 'http://localhost:5001' : `http://${location.hostname}:5001`;
