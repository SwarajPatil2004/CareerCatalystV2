import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { MainLayout } from './components/Layout';
import AdminLayout from './components/AdminLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import CareerGrind from './pages/CareerGrind';
import TPOLogin from './pages/tpo/Login';
import TPODashboard from './pages/tpo/Dashboard';
import TPOStudents from './pages/tpo/Students';
import TPODrives from './pages/tpo/Drives';
import TPOAnalytics from './pages/tpo/Analytics';
import FounderDashboard from './pages/admin/FounderDashboard';
import InterviewRoom from './pages/student/InterviewRoom';
import InterviewReport from './pages/student/InterviewReport';
import Leaderboard from './pages/student/Leaderboard';
import ProjectHub from './pages/student/ProjectHub';
import RecruiterDashboard from './pages/recruiter/RecruiterDashboard';
import PublicPortfolio from './pages/portfolio/PublicPortfolio';
import AdminDashboard from './pages/admin/AdminDashboard';

const ProtectedRoute = ({ 
  children, 
  allowedRole, 
  layout 
}: { 
  children: React.ReactNode; 
  allowedRole?: 'student' | 'tpo'; 
  layout: 'student' | 'tpo' 
}) => {
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

  return (
    <>
      {layout === 'tpo' ? (
        <AdminLayout>{children}</AdminLayout>
      ) : (
        <MainLayout>{children}</MainLayout>
      )}
    </>
  );
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
          
          <Route path="/roadmaps" element={
            <ProtectedRoute allowedRole="student" layout="student">
              <CareerGrind />
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
          <Route path="/tpo/analytics" element={
            <ProtectedRoute allowedRole="tpo" layout="tpo">
              <TPOAnalytics />
            </ProtectedRoute>
          } />
          <Route path="/admin/dashboard" element={
            <ProtectedRoute layout="tpo">
              <FounderDashboard />
            </ProtectedRoute>
          } />
          
          {/* Student Interview Routes */}
          <Route path="/interviews/:sessionId" element={
            <ProtectedRoute allowedRole="student" layout="student">
              <InterviewRoom />
            </ProtectedRoute>
          } />
          <Route path="/interviews/:sessionId/report" element={
            <ProtectedRoute allowedRole="student" layout="student">
              <InterviewReport />
            </ProtectedRoute>
          } />
          <Route path="/leaderboard" element={
            <ProtectedRoute allowedRole="student" layout="student">
              <Leaderboard />
            </ProtectedRoute>
          } />
          <Route path="/p2p" element={
            <ProtectedRoute allowedRole="student" layout="student">
              <ProjectHub />
            </ProtectedRoute>
          } />
          
          <Route path="/recruiter" element={
            <RecruiterDashboard />
          } />

          <Route path="/admin" element={
            <AdminDashboard />
          } />

          <Route path="/p/:slug" element={
            <PublicPortfolio />
          } />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
