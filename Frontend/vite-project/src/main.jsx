import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';

import App from './App.jsx';
import { AuthProvider } from './usecontext/Authcontext.jsx';
import { store } from './redux/store.js';
import { BrowserRouter } from 'react-router-dom';

createRoot(document.getElementById('root')).render(

<BrowserRouter>
    <Provider store={store}>
        <AuthProvider>
            <App />
        </AuthProvider>
    </Provider>
</BrowserRouter>

);