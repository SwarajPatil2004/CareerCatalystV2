import React, { useState, useEffect } from 'react';
import { 
  Users, Building, Activity, 
  ShieldAlert, Settings, BarChart, 
  CheckCircle, XCircle, AlertTriangle,
  ArrowUpRight, ArrowDownRight, RefreshCw
} from 'lucide-react';
import axios from 'axios';

const AdminDashboard = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/v1/admin/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching admin stats:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (loading) return <div className="p-20 text-center text-gray-400 italic">Accessing control center...</div>;

  const cards = [
    { label: 'Total Users', value: stats?.total_users || 0, icon: <Users />, color: 'bg-blue-500' },
    { label: 'DAU (30d)', value: stats?.dau || 0, icon: <Activity />, color: 'bg-green-500' },
    { label: 'Pending Partners', value: stats?.pending_institutions || 0, icon: <Building />, color: 'bg-amber-500' },
    { label: 'Interviews Held', value: stats?.total_interviews || 0, icon: <Activity />, color: 'bg-purple-500' },
  ];

  return (
    <div className="p-8 lg:p-12 bg-gray-50 min-h-screen">
      <header className="flex items-center justify-between mb-12">
        <div>
          <h1 className="text-4xl font-black text-gray-900 tracking-tight">Enterprise Admin</h1>
          <p className="text-gray-500 mt-2 font-medium">Platform-wide visibility & control</p>
        </div>
        <button 
          onClick={fetchStats}
          className="p-4 bg-white border border-gray-200 rounded-2xl hover:bg-gray-50 transition-all shadow-sm"
        >
          <RefreshCw size={20} className="text-gray-400" />
        </button>
      </header>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
        {cards.map((card, i) => (
          <div key={i} className="bg-white p-8 rounded-[2rem] shadow-sm border border-gray-100 relative overflow-hidden group hover:shadow-xl transition-all">
             <div className={`absolute top-0 right-0 w-24 h-24 ${card.color} opacity-5 rounded-bl-full group-hover:opacity-10 transition-opacity`} />
             <div className="flex items-center gap-4 mb-4">
                <div className={`p-3 rounded-xl text-white ${card.color}`}>
                   {React.cloneElement(card.icon as React.ReactElement, { size: 20 })}
                </div>
                <span className="text-sm font-bold text-gray-400 uppercase tracking-widest">{card.label}</span>
             </div>
             <div className="flex items-end justify-between">
                <span className="text-4xl font-black text-gray-900">{card.value.toLocaleString()}</span>
                <span className="text-xs font-bold text-green-500 flex items-center gap-1 mb-1">
                   <ArrowUpRight size={14} /> 12%
                </span>
             </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Verification Queue */}
        <div className="xl:col-span-2 bg-white rounded-[2rem] border border-gray-100 shadow-sm p-8">
           <h2 className="text-2xl font-black text-gray-900 mb-8 flex items-center gap-3">
              <ShieldAlert className="text-amber-500" /> Pending Approvals
           </h2>
           <div className="space-y-4">
              {[1, 2, 3].map((item) => (
                <div key={item} className="flex items-center justify-between p-6 bg-gray-50 rounded-2xl border border-gray-100 hover:border-indigo-200 transition-all">
                   <div className="flex items-center gap-6">
                      <div className="w-12 h-12 rounded-xl bg-white border border-gray-100 flex items-center justify-center font-bold text-indigo-600 shadow-sm">
                         IN
                      </div>
                      <div>
                         <p className="font-black text-gray-900">Institute of Technology {item}</p>
                         <p className="text-xs font-bold text-gray-400 uppercase tracking-tight">Applied 2h ago • New York, NY</p>
                      </div>
                   </div>
                   <div className="flex items-center gap-2">
                      <button className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-black shadow-lg shadow-indigo-100 hover:bg-indigo-500">APPROVE</button>
                      <button className="p-2 hover:bg-red-50 text-red-400 rounded-xl transition-all"><XCircle size={18} /></button>
                   </div>
                </div>
              ))}
           </div>
        </div>

        {/* System Health */}
        <div className="bg-gray-900 rounded-[2rem] p-8 text-white relative overflow-hidden">
           <div className="absolute top-0 right-0 p-8 opacity-10">
              <Activity size={120} />
           </div>
           <h2 className="text-2xl font-black mb-8 flex items-center gap-3">
              <Activity className="text-green-400" /> System Health
           </h2>
           <div className="space-y-6 relative z-10">
              <div className="p-6 bg-white/5 border border-white/10 rounded-2xl">
                 <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-bold text-gray-400 uppercase">Latency (API)</span>
                    <span className="text-xs font-black text-green-400">OPTIMAL</span>
                 </div>
                 <p className="text-3xl font-black">124ms</p>
              </div>
              <div className="p-6 bg-white/5 border border-white/10 rounded-2xl">
                 <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-bold text-gray-400 uppercase">Error Rate</span>
                    <span className="text-xs font-black text-green-400">0.02%</span>
                 </div>
                 <p className="text-3xl font-black italic">NOMINAL</p>
              </div>
              <div className="p-6 bg-white/5 border border-white/10 rounded-2xl">
                 <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-bold text-gray-400 uppercase">Celery Workers</span>
                    <span className="text-xs font-black text-amber-400">BUSY (82%)</span>
                 </div>
                 <p className="text-3xl font-black">12 Active</p>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
