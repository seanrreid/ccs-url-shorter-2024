import { Form, redirect } from 'react-router-dom';

export async function action({ request }) {
    const formData = await request.formData();
    const email = formData.get('email');
    const password = formData.get('password');

    const loginData = { email, password };

    const url = 'http://localhost:8000/login';

    const loginResponse = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
    })
        .then(async (response) => {
            const data = await response.json();
            return { status: response.status, data };
        })
        .catch((error) => {
            // Handle any errors that occurred during the fetch
            console.error('ERROR:', error.message);
        });

    const { status, data } = loginResponse;

    if (status !== 200) {
        alert(`ERROR CODE: ${status}`);
        return;
    }
    if (status === 200) {
        // We'll do something with the token once we log in
        console.log(data.access_token);
        return redirect('/');
    }
}

const Login = () => {
    return (
        <Form method='post'>
            <label>
                Email Address
                <input type='email' name='email' />
            </label>
            <label>
                Password
                <input type='password' name='password' />
            </label>
            <button type='submit'>Login</button>
        </Form>
    );
};

export default Login;
