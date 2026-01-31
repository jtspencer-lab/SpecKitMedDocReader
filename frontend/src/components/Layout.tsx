import React from 'react';
import { Outlet } from 'react-router-dom';

interface LayoutProps {
  children?: React.ReactNode;
}

/**
 * Main layout component with header, navigation, and footer.
 */
export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="layout">
      {/* Header */}
      <header className="header">
        <div className="header-container">
          <h1 className="logo">Document Extraction System</h1>
          <nav className="nav">
            <ul>
              <li><a href="/">Dashboard</a></li>
              <li><a href="/upload">Upload</a></li>
              <li><a href="/review">Review Queue</a></li>
              <li><a href="/batch">Batch</a></li>
              <li><a href="/settings">Settings</a></li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {children || <Outlet />}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>&copy; 2026 Document Extraction & Analysis System. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;
