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
import { Bar } from 'react-chartjs-2';
import { DollarSign, ShieldAlert, CreditCard, Activity } from 'lucide-react';
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

const FounderDashboard = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCosts = async () => {
      try {
        const response = await axios.get('/api/admin/costs', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setData(response.data);
      } catch (error) {
        console.error('Error fetching costs:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchCosts();
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading cost data...</div>;
  if (!data) return <div className="p-8 text-center text-red-500">Failed to load cost data.</div>;

  const chartData = {
    labels: data.institutions.map((i: any) => i.name),
    datasets: [
      {
        label: 'Spend ($)',
        data: data.institutions.map((i: any) => i.spend),
        backgroundColor: 'rgba(79, 70, 229, 0.5)',
        borderColor: 'rgb(79, 70, 229)',
        borderWidth: 1,
      },
      {
        label: 'Budget Cap ($)',
        data: data.institutions.map((i: any) => i.cap),
        backgroundColor: 'rgba(239, 68, 68, 0.2)',
        borderColor: 'rgb(239, 68, 68)',
        borderWidth: 1,
        borderDash: [5, 5],
      },
    ],
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Founder Dashboard</h1>
        <p className="text-gray-500 mt-1">AI Usage Costs & Budget Monitoring</p>
      </div>

      {/* Global Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
              <DollarSign size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Total Spend (Mister)</p>
              <h2 className="text-2xl font-bold text-gray-900">${data.total_spend.toFixed(4)}</h2>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-50 text-green-600 rounded-lg">
              <Activity size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Today's Spend</p>
              <h2 className="text-2xl font-bold text-gray-900">${data.daily_spend.toFixed(4)}</h2>
            </div>
          </div>
        </div>
      </div>

      {/* Institution List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-900">Institution Budgets</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50 text-gray-500 text-sm uppercase font-semibold">
              <tr>
                <th className="px-6 py-4">Institution</th>
                <th className="px-6 py-4">Current Spend</th>
                <th className="px-6 py-4">Monthly Cap</th>
                <th className="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {data.institutions.map((inst: any) => (
                <tr key={inst.name} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">{inst.name}</td>
                  <td className="px-6 py-4">${inst.spend.toFixed(4)}</td>
                  <td className="px-6 py-4">${inst.cap.toFixed(2)}</td>
                  <td className="px-6 py-4">
                    {inst.spend >= inst.cap ? (
                      <span className="flex items-center gap-1 text-red-600 font-semibold text-sm">
                        <ShieldAlert size={16} /> EXCEEDED
                      </span>
                    ) : (
                      <span className="text-green-600 font-semibold text-sm">NORMAL</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Spend vs Budget by Institution</h2>
        <div className="h-[400px]">
          <Bar data={chartData} options={{ maintainAspectRatio: false }} />
        </div>
      </div>
    </div>
  );
};

export default FounderDashboard;
