import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';

/**
 * Root App component with routing structure.
 * 
 * Routes:
 * - / : Home/Dashboard
 * - /upload : Document upload
 * - /review : Review queue
 * - /results : Extraction results
 * - /batch : Batch processing
 * - /settings : Application settings
 */
function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          {/* TODO: Add additional routes for upload, review, results, batch, settings */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
