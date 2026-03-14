import React, { useState } from 'react';
import { 
  Users, 
  Briefcase, 
  Calendar, 
  AlertTriangle,
  ArrowUpRight,
  TrendingUp,
  Clock
} from 'lucide-react';
import { cn } from '../../utils/cn';

interface DashboardStats {
  totalStudents: number;
  activeDrives: number;
  upcomingDeadlines: number;
  newApplications: number;
}

const TPODashboard: React.FC = () => {
  const [stats] = useState<DashboardStats>({
    totalStudents: 450,
    activeDrives: 12,
    upcomingDeadlines: 3,
    newApplications: 28
  });

  const [studentsAtRisk] = useState([
    { id: 1, name: 'Swaraj Patil', branch: 'CS', risk: 'Low Activity', lastActive: '5 days ago' },
    { id: 2, name: 'Rahul Sharma', branch: 'IT', risk: 'Incomplete Profile', lastActive: '2 weeks ago' },
    { id: 3, name: 'Anita Desai', branch: 'ENTC', risk: 'Low Activity', lastActive: '10 days ago' },
  ]);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
        <p className="text-gray-500">Overview of your institution's placement activity.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total Students', value: stats.totalStudents, icon: Users, color: 'text-blue-600', bg: 'bg-blue-50' },
          { label: 'Active Drives', value: stats.activeDrives, icon: Briefcase, color: 'text-purple-600', bg: 'bg-purple-50' },
          { label: 'Upcoming Deadlines', value: stats.upcomingDeadlines, icon: Calendar, color: 'text-orange-600', bg: 'bg-orange-50' },
          { label: 'New Applications', value: stats.newApplications, icon: TrendingUp, color: 'text-green-600', bg: 'bg-green-50' },
        ].map((stat, i: number) => (
          <div key={i} className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className={cn("p-2.5 rounded-xl", stat.bg)}>
                <stat.icon className={cn("w-6 h-6", stat.color)} />
              </div>
              <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded-lg">+12%</span>
            </div>
            <p className="text-sm font-medium text-gray-500">{stat.label}</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Students at Risk */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden text-black">
          <div className="px-6 py-5 border-b border-gray-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-orange-500" />
              <h2 className="text-lg font-bold">Students Needing Attention</h2>
            </div>
            <button className="text-sm font-bold text-primary-600 hover:text-primary-700 flex items-center gap-1">
              View All <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                  <th className="px-6 py-3 font-bold">Student Name</th>
                  <th className="px-6 py-3 font-bold">Branch</th>
                  <th className="px-6 py-3 font-bold">Risk Reason</th>
                  <th className="px-6 py-3 font-bold">Last Active</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 italic">
                {studentsAtRisk.map((student: any) => (
                  <tr key={student.id} className="hover:bg-gray-50/50 transition-colors">
                    <td className="px-6 py-4 font-bold text-gray-900">{student.name}</td>
                    <td className="px-6 py-4 text-gray-600">{student.branch}</td>
                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 bg-orange-50 text-orange-600 rounded-lg text-xs font-bold">
                        {student.risk}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-gray-500 text-sm flex items-center gap-1">
                      <Clock className="w-4 h-4" /> {student.lastActive}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-900 rounded-3xl p-8 text-white flex flex-col justify-between shadow-2xl shadow-gray-900/20">
          <div>
            <h3 className="text-xl font-extrabold mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full bg-white/10 hover:bg-white/20 text-white rounded-xl py-3 px-4 text-left font-medium transition-all">
                Post New Drive
              </button>
              <button className="w-full bg-white/10 hover:bg-white/20 text-white rounded-xl py-3 px-4 text-left font-medium transition-all">
                Export Student Data
              </button>
              <button className="w-full bg-white/10 hover:bg-white/20 text-white rounded-xl py-3 px-4 text-left font-medium transition-all">
                Broadcast Announcement
              </button>
            </div>
          </div>
          <div className="mt-8 p-4 bg-primary-600/20 border border-primary-600/30 rounded-2xl">
            <p className="text-sm font-medium text-primary-100">
              Institution Tier: <span className="text-white font-bold italic">Gold</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TPODashboard;
