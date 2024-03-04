import { Outlet } from 'react-router-dom';

const Layout = () => {
    return (
        <div style={{ border: 'solid 1px violet' }}>
            <Outlet />
        </div>
    );
};

export default Layout;
