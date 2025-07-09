import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MenuApp from "./components/MenuApp";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MenuApp />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
