import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import Layout from '../pages/Layout';
import ProtectedRouteLayout from '../pages/ProtectedRouteLayout';
import Error from '../pages/Error';
import Home from './Home';
import Login, { action as loginAction } from './Login';
import AddLink from './AddLink';

const Routes = () => {
    const { isAuth } = useAuth();

    const publicRoutes = [
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
                    action: loginAction,
                },
            ],
        },
    ];

    const protectedRoutes = [
        {
            element: <ProtectedRouteLayout />,
            children: [
                {
                    path: '/links/add',
                    element: <AddLink />,
                },
            ],
        },
    ];

    const router = createBrowserRouter([
        ...publicRoutes,
        ...(!isAuth ? protectedRoutes : []),
        ...protectedRoutes,
    ]);

    return <RouterProvider router={router} />;
};

export default Routes;
