import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  CheckCircle2, 
  Circle, 
  TrendingUp, 
  Award, 
  Briefcase, 
  Code 
} from 'lucide-react';
import apiClient from '../api/client';
import type { StudentProfile } from '../types';
import { cn } from '../utils/cn';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<StudentProfile | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await apiClient.get('/students/me/profile');
        setProfile(response.data);
      } catch (error) {
        console.error('Failed to fetch profile', error);
      }
    };
    fetchProfile();
  }, []);

  const stats = [
    { name: 'Profile Completion', value: '85%', icon: CheckCircle2, color: 'text-green-600' },
    { name: 'Skills Added', value: '12', icon: Code, color: 'text-blue-600' },
    { name: 'Projects', value: '4', icon: Briefcase, color: 'text-purple-600' },
    { name: 'Achievements', value: '2', icon: Award, color: 'text-orange-600' },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Hello, {user?.full_name}! 👋</h1>
        <p className="text-gray-600">Here's what's happening with your profile today.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center gap-4">
            <div className={cn("p-3 bg-gray-50 rounded-xl", stat.color)}>
              <stat.icon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">{stat.name}</p>
              <p className="text-xl font-bold text-gray-900">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <div className="p-6 border-b border-gray-100 flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-900">Recommended Steps</h2>
            <TrendingUp className="w-5 h-5 text-gray-400" />
          </div>
          <div className="p-6 space-y-4">
            {[
              { label: 'Add a professional headline', done: !!profile?.headline },
              { label: 'Link your GitHub profile', done: !!profile?.github_link },
              { label: 'Add your latest project', done: true },
              { label: 'Complete branch details', done: !!profile?.branch },
            ].map((step, i) => (
              <div key={i} className="flex items-center gap-3">
                {step.done ? (
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                ) : (
                  <Circle className="w-5 h-5 text-gray-300" />
                )}
                <span className={step.done ? "text-gray-500 line-through" : "text-gray-700"}>
                  {step.label}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-primary-600 rounded-2xl p-6 text-white flex flex-col justify-between">
          <div>
            <h3 className="text-xl font-bold mb-2">Build Your Future</h3>
            <p className="text-primary-100 text-sm">
              Complete your profile to unlock personalized career roadmaps and interview practice sessions.
            </p>
          </div>
          <button className="mt-8 bg-white text-primary-600 font-bold py-2 px-4 rounded-xl hover:bg-primary-50 transition-colors self-start">
            Build Roadmap
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
