import { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Stats {
  total_deliveries: number;
  pending_deliveries: number;
  completed_deliveries: number;
  failed_deliveries: number;
  available_drivers: number;
  available_vehicles: number;
}

function App() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [chartData, setChartData] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      fetch('http://127.0.0.1:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin1', password: 'secret123' })
      })
      .then(res => res.json())
      .then(data => {
        localStorage.setItem('token', data.data.access_token);
        window.location.reload();
      });
      return;
    }

    const headers = { Authorization: `Bearer ${token}` };
    
    fetch('http://127.0.0.1:5000/api/analytics/overview', { headers })
      .then(res => res.json())
      .then(data => setStats(data.data));

    fetch('http://127.0.0.1:5000/api/analytics/deliveries', { headers })
      .then(res => res.json())
      .then(data => {
        setChartData({
          labels: data.data.map((d: any) => d.status),
          datasets: [{
            label: 'Deliveries',
            data: data.data.map((d: any) => d.count),
            backgroundColor: '#3b82f6',
            borderRadius: 6
          }]
        });
      });
  }, []);

  return (
    <div className="app-container">
      <div className="sidebar">
        <div className="sidebar-logo">FLEETNEX (React)</div>
      </div>
      <div className="main-content">
        <h2>Live Operations Overview</h2>
        
        {stats ? (
          <div className="stats-grid">
            <div className="stat-card"><h3>Total</h3><div className="value primary">{stats.total_deliveries}</div></div>
            <div className="stat-card"><h3>Pending</h3><div className="value">{stats.pending_deliveries}</div></div>
            <div className="stat-card"><h3>Completed</h3><div className="value success">{stats.completed_deliveries}</div></div>
            <div className="stat-card"><h3>Drivers</h3><div className="value primary">{stats.available_drivers}</div></div>
          </div>
        ) : <p>Loading stats...</p>}

        {chartData && (
          <div className="stat-card" style={{ marginTop: '20px' }}>
            <Bar data={chartData} options={{ responsive: true }} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
