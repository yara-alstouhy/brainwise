import React, { useEffect, useState } from 'react';
import axios from 'axios';
import EditModal from "./EditModel";

function Table({ apiUrl }) {
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [selectedRowId, setSelectedRowId] = useState(null); // State to track the selected row id
    const [isEditModalOpen, setIsEditModalOpen] = useState(false); // State to control the visibility of the edit modal

    useEffect(() => {
        fetchData();
    }, []);

    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    };

    const jwt = getCookie('jwt');

    const fetchData = async () => {
        try {
            const response = await axios.get(`${apiUrl}?jwt=${jwt}`);
            setData(response.data);
            if (response.data.length > 0) {
                setColumns(Object.keys(response.data[0]));
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const handleEdit = (id) => {
        setSelectedRowId(id);
        setIsEditModalOpen(true);
    };

    const handleDelete = async (id) => {
        try {
            const response = await axios.delete(`${apiUrl}${id}/?jwt=${jwt}`);
            console.log('Delete response:', response.data);

            fetchData();
        } catch (error) {
            console.error('Error deleting data:', error);
        }
    };

    const handleCloseEditModal = () => {
        setIsEditModalOpen(false);
        setSelectedRowId(null);
    };

    const handleSaveEditModal = async (newData) => {
        try {
            setIsEditModalOpen(false);
            setSelectedRowId(null);
            await fetchData(); // Update the table data
        } catch (error) {
            console.error('Error editing data:', error);
        }
    };


    return (
        <div className="container mx-auto p-4">
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-200">
                    <thead>
                    <tr>
                        {columns.map((column) => (
                            <th
                                key={column}
                                className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                {column}
                            </th>
                        ))}
                        <th className="px-6 py-3 bg-gray-50 text-xs font-medium text-gray-500 uppercase tracking-wider text-center">
                            Actions
                        </th>
                    </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                    {data.map((row) => (
                        <tr key={row.id}>
                            {columns.map((column) => (
                                <td key={column} className="px-6 py-4 whitespace-nowrap">
                                    {column === 'user' ? row.user.email : row[column]}
                                </td>
                            ))}
                            <td className="px-4 py-2 flex flex-row items-center justify-center">
                                <button
                                    onClick={() => handleEdit(row.id,data)}
                                    className="text-blue-600 hover:text-blue-900 w-1/2 flex items-center justify-center"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" id="edit" className="w-6 hover:text-purple-800">
                                        <path fill="none" d="M0 0h24v24H0V0z"></path>
                                        <path
                                            d="M3 17.46v3.04c0 .28.22.5.5.5h3.04c.13 0 .26-.05.35-.15L17.81 9.94l-3.75-3.75L3.15 17.1c-.1.1-.15.22-.15.36zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"
                                            fill="#9b21e1"
                                            className="color000000 svgShape"
                                        ></path>
                                    </svg>
                                </button>
                                {isEditModalOpen && (
                                    <EditModal
                                        companyName={data.find(row => row.id === selectedRowId)?.company_name} // Get the company name of the selected row
                                        onClose={handleCloseEditModal} // Pass onClose function
                                        onSave={handleSaveEditModal} // Pass onSave function
                                        apiUrl={`${apiUrl}${row.id}/?jwt=${jwt}`}
                                    />
                                )}
                                <button
                                    onClick={() => handleDelete(row.id)}
                                    className="text-red-600 hover:text-red-900 w-1/2 flex items-center justify-center"
                                >
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                                    </svg>
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default Table;
