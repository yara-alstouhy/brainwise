import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './componants/pages/Home'
import Landing from "./componants/pages/Landing";
import Login from "./componants/pages/Login";
import ManageEmployee from "./componants/pages/ManageEmployee";
import ManageCompanies from "./componants/pages/ManageCompanies";
import ManageDepartments from "./componants/pages/ManageDepartments";
function App() {

  return (
      <>
          <Router>
              <Routes>
                  <Route path="/login" element={<Login />} />
                  <Route path="/home" element={<Home />}/>
                  <Route path="/company" element={<ManageCompanies/>} />
                  <Route path="/department" element={<ManageDepartments/>} />
                  <Route path="/employee" element={<ManageEmployee/>} />
                  {/*</Route>*/}
                  <Route path="/" element={<Landing/>} />
              </Routes>
          </Router>
      </>

  );
}
export default App;
