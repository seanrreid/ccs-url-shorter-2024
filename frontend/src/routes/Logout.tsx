import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

// export async function loader() {
//     const url = 'http://localhost:8000/logout/';
//     const refresh_token = localStorage.getItem('refresh_token');
//     const access_token = localStorage.getItem('access_token');

//     const response = await fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             Authorization: `Bearer ${access_token}`,
//         },
//         body: JSON.stringify({ refresh_token }),
//     });
//     return { response };
// }

const Logout = () => {
    const { setIsAuth } = useAuth();
    const navigate = useNavigate();

    localStorage.clear();
    setIsAuth(false);
    return navigate(`/login`);
}

export default Logout