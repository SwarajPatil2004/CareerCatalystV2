import React, { useState, useEffect } from 'react';
import { 
  Trophy, Medal, Users, 
  ChevronUp, Crown, Star,
  Search, Filter, BookOpen
} from 'lucide-react';
import axios from 'axios';

const Leaderboard = () => {
  const [activeTab, setActiveTab] = useState<'individual' | 'squad' | 'institution'>('individual');
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`/api/p2p/leaderboard?type=${activeTab}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setLeaderboard(response.data);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchLeaderboard();
  }, [activeTab]);

  const getRankColor = (rank: number) => {
    if (rank === 0) return 'text-yellow-500 bg-yellow-50 border-yellow-200';
    if (rank === 1) return 'text-gray-400 bg-gray-50 border-gray-200';
    if (rank === 2) return 'text-amber-600 bg-amber-50 border-amber-200';
    return 'text-gray-500 bg-gray-50 border-gray-100';
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Career Seasons</h1>
          <p className="text-gray-500 mt-2 text-lg">Compete, learn, and grow with your squad</p>
        </div>
        
        <div className="flex bg-gray-100 p-1.5 rounded-2xl border border-gray-200">
          <button 
            onClick={() => setActiveTab('individual')}
            className={`px-6 py-2.5 rounded-xl font-bold transition-all flex items-center gap-2 ${activeTab === 'individual' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <Star size={18} /> Individuals
          </button>
          <button 
            onClick={() => setActiveTab('squad')}
            className={`px-6 py-2.5 rounded-xl font-bold transition-all flex items-center gap-2 ${activeTab === 'squad' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <Users size={18} /> Squads
          </button>
          <button 
            onClick={() => setActiveTab('institution')}
            className={`px-6 py-2.5 rounded-xl font-bold transition-all flex items-center gap-2 ${activeTab === 'institution' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <BookOpen size={18} /> Institutions
          </button>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-gray-400">Loading rankings...</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Top 3 Podium */}
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-white rounded-3xl border border-gray-100 shadow-xl shadow-gray-100 overflow-hidden">
               <div className="p-4 bg-indigo-600/5 border-b border-indigo-100 flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Season 4 Rankings</span>
                  <div className="flex items-center gap-2 text-indigo-600 text-xs font-bold">
                    <Trophy size={14} /> LIVE UPDATE
                  </div>
               </div>
               
               <div className="divide-y divide-gray-50">
                  {leaderboard.length > 0 ? leaderboard.map((item, idx) => (
                    <div key={idx} className="p-6 flex items-center justify-between hover:bg-gray-50 transition-colors group">
                       <div className="flex items-center gap-6">
                          <div className={`w-12 h-12 flex items-center justify-center rounded-2xl border-2 font-black text-lg ${getRankColor(idx)}`}>
                             {idx + 1}
                          </div>
                          <div>
                             <h4 className="font-bold text-gray-900 group-hover:text-indigo-600 transition-colors">
                               {item.name || `User ${item.user_id}`}
                             </h4>
                             <p className="text-xs text-gray-400 font-medium uppercase tracking-tighter">
                               {activeTab === 'individual' ? 'Senior Fullstack Squad' : 'Stanford University'}
                             </p>
                          </div>
                       </div>
                       
                       <div className="flex items-center gap-8">
                          <div className="text-right">
                             <div className="text-lg font-black text-gray-900">{item.total_xp || item.current_xp || 0} XP</div>
                             <div className="text-[10px] font-bold text-green-500 flex items-center justify-end gap-1">
                                <ChevronUp size={10} /> +12%
                             </div>
                          </div>
                          <div className="p-2 bg-gray-50 rounded-lg text-gray-300 group-hover:text-indigo-400 group-hover:bg-indigo-50 transition-all">
                             <Medal size={20} />
                          </div>
                       </div>
                    </div>
                  )) : (
                    <div className="p-12 text-center text-gray-400">No data for this season yet.</div>
                  )}
               </div>
            </div>
          </div>

          {/* Sidebar Info */}
          <div className="space-y-6">
             <div className="bg-indigo-600 rounded-3xl p-8 text-white shadow-xl shadow-indigo-100 relative overflow-hidden">
                <Crown size={80} className="absolute -bottom-4 -right-4 opacity-10 rotate-12" />
                <h3 className="text-xl font-bold mb-2">My Squad Status</h3>
                <p className="text-indigo-100 text-sm mb-6 leading-relaxed">Your squad is currently in the top 5% of this institution.</p>
                <div className="bg-white/10 rounded-2xl p-4 backdrop-blur-md border border-white/20">
                   <div className="flex justify-between text-xs font-bold mb-2 uppercase tracking-widest text-indigo-200">
                      <span>Squad Goal</span>
                      <span>{Math.round((3400/5000)*100)}%</span>
                   </div>
                   <div className="h-3 bg-white/20 rounded-full overflow-hidden">
                      <div className="h-full bg-white rounded-full" style={{width: '68%'}} />
                   </div>
                   <div className="mt-2 text-[10px] text-indigo-300 font-medium italic">
                     Need 1,600 XP to reach Tier 1 rewards!
                   </div>
                </div>
             </div>

             <div className="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
                <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
                   <Filter size={18} className="text-indigo-600" /> Season Perks
                </h3>
                <div className="space-y-4">
                   {[
                     { name: "Top 100", perk: "Early Access to 24/7 AI Mock", icon: "🚀" },
                     { name: "Top 10 Squads", perk: "1.5x Multiplier for 7 days", icon: "🔥" },
                     { name: "All Completers", perk: "Season 4 Badge & Certificate", icon: "💎" }
                   ].map((p, i) => (
                     <div key={i} className="flex gap-4 p-4 rounded-2xl hover:bg-gray-50 transition-all border border-transparent hover:border-gray-100">
                        <span className="text-2xl">{p.icon}</span>
                        <div>
                           <p className="text-xs font-bold text-indigo-600">{p.name}</p>
                           <p className="text-sm font-medium text-gray-600">{p.perk}</p>
                        </div>
                     </div>
                   ))}
                </div>
             </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;
