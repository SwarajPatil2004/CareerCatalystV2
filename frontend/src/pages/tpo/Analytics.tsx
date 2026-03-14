import React, { useEffect, useState } from 'react';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement,
  Title, 
  Tooltip, 
  Legend, 
  ArcElement 
} from 'chart.js';
import { Line, Bar, Pie } from 'react-chartjs-2';
import { Download, TrendingUp, Users, AlertTriangle } from 'lucide-react';
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Analytics = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await axios.get('/api/tpo/analytics/health', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setData(response.data);
      } catch (error) {
        console.error('Error fetching analytics:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  const handleExport = async () => {
    try {
      const response = await axios.get('/api/tpo/analytics/export', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'institution_analytics.csv');
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error('Error exporting CSV:', error);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-500">Loading analytics...</div>;
  if (!data) return <div className="p-8 text-center text-red-500">Failed to load analytics data.</div>;

  const activityData = {
    labels: data.activity_trend.map((t: any) => t.date),
    datasets: [
      {
        label: 'Student Activity',
        data: data.activity_trend.map((t: any) => t.count),
        borderColor: 'rgb(79, 70, 229)',
        backgroundColor: 'rgba(79, 70, 229, 0.5)',
        tension: 0.4,
      },
    ],
  };

  const skillsData = {
    labels: data.skills_distribution.map((s: any) => s.name),
    datasets: [
      {
        label: 'Top Skills',
        data: data.skills_distribution.map((s: any) => s.count),
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1,
      },
    ],
  };

  const funnelData = {
    labels: ['Shortlisted', 'Selected'],
    datasets: [
      {
        label: 'Placement Funnel',
        data: [data.placement_funnel.shortlisted, data.placement_funnel.selected],
        backgroundColor: ['rgba(245, 158, 11, 0.5)', 'rgba(16, 185, 129, 0.5)'],
        borderColor: ['rgb(245, 158, 11)', 'rgb(16, 185, 129)'],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Institution Analytics</h1>
          <p className="text-gray-500 mt-1">Real-time performance and placement metrics</p>
        </div>
        <button 
          onClick={handleExport}
          className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
        >
          <Download size={20} />
          Export CSV
        </button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
              <Users size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Total Students</p>
              <h2 className="text-2xl font-bold text-gray-900">{data.stats.total_students}</h2>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-50 text-green-600 rounded-lg">
              <TrendingUp size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Active (30d)</p>
              <h2 className="text-2xl font-bold text-gray-900">{data.stats.active_students}</h2>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-red-50 text-red-600 rounded-lg">
              <AlertTriangle size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">At-Risk Students</p>
              <h2 className="text-2xl font-bold text-gray-900">{data.stats.at_risk_students}</h2>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Activity Trend</h2>
          <div className="h-[300px]">
            <Line data={activityData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Skills Heatmap</h2>
          <div className="h-[300px]">
            <Bar data={skillsData} options={{ maintainAspectRatio: false, indexAxis: 'y' as const }} />
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Placement Funnel</h2>
          <div className="h-[300px] flex justify-center">
            <Pie data={funnelData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
