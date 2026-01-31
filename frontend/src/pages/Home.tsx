import React from 'react';

/**
 * Home page / Dashboard component.
 * 
 * Shows overview of system status, recent uploads, pending reviews, etc.
 */
export const Home: React.FC = () => {
  return (
    <div className="home-page">
      <h1>Document Extraction System Dashboard</h1>
      <div className="dashboard-grid">
        <section className="card">
          <h2>Recent Uploads</h2>
          <p>No documents uploaded yet</p>
        </section>
        
        <section className="card">
          <h2>Pending Reviews</h2>
          <p>No pending reviews</p>
        </section>
        
        <section className="card">
          <h2>System Status</h2>
          <p>System is healthy</p>
        </section>
      </div>
    </div>
  );
};

export default Home;
