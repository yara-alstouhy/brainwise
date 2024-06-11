import React, {Component} from 'react';
import Navbar from "../elements/Navbar";
import Table from "../elements/Table";
import CreateCompany from "../elements/CreateCompany";
const navigation = [
    { name: 'Dashboard', href: '/home', current: false },
    { name: 'Company Management', href: 'company', current: true },
    { name: 'Department Management', href: 'department', current: false },
    { name: 'Employee Management', href: 'employee', current: false },
]
class ManageCompanies extends Component {
    render() {

        const apiUrl = 'http://127.0.0.1:8000/company/';
        return (
            <div className="min-h-screen">
                <Navbar navigation={navigation}/>

                <div className={'flex flex-row'}>
                    <div className={" flex  flex-col py-10 w-2/3 "}>
                        <div className="max-w-7xl py-10 sm:px-6 lg:px-8">
                            <h1 className="text-3xl font-bold tracking-tight text-gray-900">Manage Companies</h1>
                        </div>
                        <Table apiUrl={apiUrl}/>
                    </div>
                    <div className={" flex justify-end  w-1/3 "}>
                        <CreateCompany/>
                    </div>

                </div>

            </div>
        );
    }
}

export default ManageCompanies;
