import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

import styles from './nav.module.css'

export default function MainNav() {
    const { isAuth } = useAuth();
    return (
        <nav className={styles.nav}>
            <ul>
                <li>{isAuth ? <Link to='/'>Home</Link> : null}</li>
                <li>
                    {isAuth ? (
                        <Link to='/logout'>Logout</Link>
                    ) : (
                        <Link to='/login'>Login</Link>
                    )}
                </li>
            </ul>
        </nav>
    );
}
