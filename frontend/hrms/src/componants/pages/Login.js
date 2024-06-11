import React, {useContext, useState} from 'react';
import { useNavigate } from 'react-router-dom';
// import { UserContext } from '../../UserContext';
function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    // const { setUser } = useContext(UserContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await fetch('http://127.0.0.1:8000/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
                credentials: 'include',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Login successful:', data);
            // setUser(data);
            document.cookie = `jwt=${data['jwt']}`
            navigate('/home');
            // const getCookie = (name) => {
            //     const value = `; ${document.cookie}`;
            //     const parts = value.split(`; ${name}=`);
            //     if (parts.length === 2) return parts.pop().split(';').shift();
            // }
            // console.log(getCookie('jwt'));
        } catch (error) {
            console.error('error:', error);
            setError('Login failed. Please check your email and password and try again.');
        }
    };

    return (
        <div className={'h-screen flex justify-center items-center bg-gradient-to-b from-purple-800 '}>
            <div className="w-100 mb-20 mx-auto p-6 border border-gray-300 rounded bg-gray-50 h-fit">
                <h1 className="text-2xl font-bold mb-6">Login</h1>
                {error && <p className="text-red-500">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block mb-1">Email:</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded"
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block mb-1">Password:</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded focus:border-none"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-500"
                    >
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Login;
