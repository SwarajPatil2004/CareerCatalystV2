import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { MainLayout } from './components/Layout';
import AdminLayout from './components/AdminLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import TPOLogin from './pages/tpo/Login';
import TPODashboard from './pages/tpo/Dashboard';
import TPOStudents from './pages/tpo/Students';
import TPODrives from './pages/tpo/Drives';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRole?: 'student' | 'tpo';
  layout: 'student' | 'tpo';
}

const ProtectedRoute = ({ 
  children, 
  allowedRole, 
  layout 
}: ProtectedRouteProps) => {
  const { user, loading } = useAuth();

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
  );
  
  if (!user) {
    return <Navigate to={layout === 'tpo' ? "/tpo/login" : "/login"} replace />;
  }

  if (allowedRole && user.role !== allowedRole) {
    return <Navigate to={user.role === 'tpo' ? "/tpo" : "/"} replace />;
  }

  return layout === 'tpo' ? <AdminLayout>{children}</AdminLayout> : <MainLayout>{children}</MainLayout>;
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/tpo/login" element={<TPOLogin />} />
          
          {/* Student Routes */}
          <Route path="/" element={
            <ProtectedRoute allowedRole="student" layout="student">
              <Dashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/profile" element={
            <ProtectedRoute allowedRole="student" layout="student">
              <Profile />
            </ProtectedRoute>
          } />
          
          {/* TPO Routes */}
          <Route path="/tpo" element={
            <ProtectedRoute allowedRole="tpo" layout="tpo">
              <TPODashboard />
            </ProtectedRoute>
          } />
          <Route path="/tpo/students" element={
            <ProtectedRoute allowedRole="tpo" layout="tpo">
              <TPOStudents />
            </ProtectedRoute>
          } />
          <Route path="/tpo/drives" element={
            <ProtectedRoute allowedRole="tpo" layout="tpo">
              <TPODrives />
            </ProtectedRoute>
          } />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
