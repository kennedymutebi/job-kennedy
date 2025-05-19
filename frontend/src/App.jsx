import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Welcome from "./Pages/Welcome/Welcome";
Welcome

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
      </Routes>
    </Router>
  );
};

export default App;
