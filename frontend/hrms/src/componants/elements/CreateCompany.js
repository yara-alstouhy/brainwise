import React from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

const schema = yup.object().shape({
    username: yup.string().required('Username is required'),
    email: yup.string().email('Invalid email').required('Email is required'),
    password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
    company_name: yup.string().required('Company name is required'),
   });

const CreateCompany = () => {
    const { register, handleSubmit, formState: { errors } } = useForm({
        resolver: yupResolver(schema),
    });

    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    const jwt = getCookie('jwt');

    const onSubmit = async (data) => {

        const company_data={
            "user": {
                "username": data['username'],
                "email": data['email'],
                "password":data['password'],
            },
            "company_name": data['company_name'],
        }
        try {
            const response = await fetch(`http://127.0.0.1:8000/company/?jwt=${jwt}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(company_data),
            });

            if (!response.ok) {
                const error = response;
                alert(`Error: ${error}`);
                throw new Error(`Error: ${error}`);
            }

            alert('Form submitted successfully');
            window.location.reload();
        } catch (error) {
            console.error('There was an error!', error);
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="py-20 px-10 w-fit flex justify-end flex-col bg-gray-50">
            <div className="space-y-12">
                <div className="pb-12">
                    <h2 className="text-base font-semibold leading-7 text-gray-900">Add new company</h2>
                    <div className="mt-10 grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-5">

                        <div className="sm:col-span-4">
                            <label htmlFor="company_name" className="block text-sm font-medium leading-6 text-gray-900">
                                Company name
                            </label>
                            <div className="mt-2">
                                <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                                    <input
                                        type="text"
                                        name="company_name"
                                        id="company_name"
                                        {...register('company_name')}
                                        className="px-6 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                    />
                                </div>
                                {errors.company_name && <p className="text-red-500 text-xs italic">{errors.company_name.message}</p>}
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label htmlFor="username" className="block text-sm font-medium leading-6 text-gray-900">
                                Username
                            </label>
                            <div className="mt-2">
                                <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                                    <input
                                        type="text"
                                        name="username"
                                        id="username"
                                        {...register('username')}
                                        className="px-6 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                    />
                                </div>
                                {errors.username && <p className="text-red-500 text-xs italic">{errors.username.message}</p>}
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    {...register('email')}
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                />
                                {errors.email && <p className="text-red-500 text-xs italic">{errors.email.message}</p>}
                            </div>
                        </div>

                        <div className="sm:col-span-4">
                            <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                                Password
                            </label>
                            <div className="mt-2">
                                <div className="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                                    <input
                                        type="password"
                                        name="password"
                                        id="password"
                                        {...register('password')}
                                        className="px-6 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                    />
                                </div>
                                {errors.password && <p className="text-red-500 text-xs italic">{errors.password.message}</p>}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-6 flex items-center justify-end gap-x-6">
                <button
                    type="submit"
                    className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                    Save
                </button>
            </div>
        </form>
    );
};

export default CreateCompany;
