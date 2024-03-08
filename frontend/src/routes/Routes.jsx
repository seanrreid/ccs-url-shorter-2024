import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import Layout from '../pages/Layout';
import ProtectedRouteLayout from '../pages/ProtectedRouteLayout';
import Error from '../pages/Error';
import Home from './Home';
import Login, { action as loginAction } from './Login';
import Links, { loader as linksLoader } from './Links';
import AddLink, {
    loader as addLinkLoader,
    action as addLinkAction,
} from './AddLink';
import Logout from './Logout';

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
                    path: '/links/',
                    element: <Links />,
                    loader: linksLoader,
                },
                {
                    path: '/links/add',
                    element: <AddLink />,
                    loader: addLinkLoader,
                    action: addLinkAction,
                },
                {
                    path: '/logout',
                    element: <Logout />,
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
