import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Layout from './pages/Layout';
import Error from './pages/Error'
import Home from './routes/Home';
import Login, { action as loginAction } from './routes/Login';

import './global.css'

const router = createBrowserRouter([
    {
        element: <Layout />,
        errorElement: <Error />,
        children: [
            {
                path: '/',
                element: <Home />,
            },
            {
                path: '/login',
                element: <Login />,
                action: loginAction
            }
        ],
    },
]);

function App() {
    return <RouterProvider router={router} />;
}

export default App;
