import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { SupplementList } from "./pages/SupplementList";
import { SupplementDetail } from "./pages/SupplementDetail";
import { SymptomList } from "./pages/SymptomList";
import { SymptomDetail } from "./pages/SymptomDetail";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Navigate to="/supplements" replace />} />
          <Route path="/supplements" element={<SupplementList />} />
          <Route path="/supplements/:id" element={<SupplementDetail />} />
          <Route path="/symptoms" element={<SymptomList />} />
          <Route path="/symptoms/:slug" element={<SymptomDetail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
