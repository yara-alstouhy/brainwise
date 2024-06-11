import Navbar from "../elements/Navbar";
import Hero from "../elements/Hero";


const navigation = [
    { name: 'Dashboard', href: '/home', current: true },
    { name: 'Company Management', href: 'company', current: false },
    { name: 'Department Management', href: 'department', current: false },
    { name: 'Employee Management', href: 'employee', current: false },
]



export default function Home() {
    return (
        <>
            <div className="min-h-full">
                <Navbar navigation={navigation}/>
                <main>
                    <div className="mx-auto max-w-7xl sm:px-6 lg:px-4 ">{
                        <Hero/>

                    }</div>
                </main>
            </div>
        </>
    )
}
