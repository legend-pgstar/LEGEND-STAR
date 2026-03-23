import React, { useEffect, useMemo, useState, useRef } from 'react';
import { Link, Route, Routes, useLocation } from 'react-router-dom';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
const API_KEY = import.meta.env.VITE_API_KEY || 'changeme';
const headers = { 'x-api-key': API_KEY };

function StatsCard({ title, value }) {
  return (
    <div className="card border-l-4 border-l-neonblue/70 p-4 m-2">
      <h3 className="text-sm uppercase tracking-wider text-neonblue">{title}</h3>
      <p className="text-3xl font-semibold text-white">{value}</p>
    </div>
  );
}

function Loading() {
  return (
    <div className="flex justify-center items-center py-10">
      <div className="spinner" />
    </div>
  );
}

function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [chartData, setChartData] = useState({ labels: [], datasets: [] });
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const [aRes, lRes] = await Promise.all([
        axios.get(`${API_BASE}/analytics`, { headers }),
        axios.get(`${API_BASE}/logs?limit=100`, { headers }),
      ]);
      setAnalytics(aRes.data);
      setLogs(lRes.data);
    };
    fetchData().catch(console.error);
  }, []);

  useEffect(() => {
    const byTime = logs
      .slice(0, 100)
      .reverse()
      .reduce((acc, log) => {
        const key = new Date(log.time).toLocaleString();
        acc[key] = (acc[key] || 0) + 1;
        return acc;
      }, {});

    setChartData({
      labels: Object.keys(byTime),
      datasets: [
        {
          label: 'Logs over time',
          data: Object.values(byTime),
          borderColor: '#6EE7FF',
          backgroundColor: 'rgba(110, 231, 255, 0.25)',
          tension: 0.3,
          fill: true,
        },
      ],
    });
  }, [logs]);

  if (!analytics) return <Loading />;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatsCard title="Active Users" value={analytics.active_users} />
        <StatsCard title="Messages" value={analytics.total_messages} />
        <StatsCard title="Commands" value={analytics.total_commands} />
        <StatsCard title="Errors" value={analytics.total_errors} />
      </div>
      <div className="card h-96">
        <Line
          data={chartData}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: true } },
          }}
        />
      </div>
    </div>
  );
}

function LogRow({ item }) {
  const colors = {
    message: 'border-green-400',
    command: 'border-blue-400',
    error: 'border-red-500',
    system: 'border-yellow-300',
  };

  return (
    <div className={`card border-l-4 ${colors[item.type] || 'border-gray-300'}`}>
      <div className="flex justify-between gap-2 mb-1">
        <span className="font-semibold uppercase tracking-wide text-xs">{item.type}</span>
        <span className="text-xs text-gray-400">{new Date(item.time).toLocaleString()}</span>
      </div>
      <div className="text-sm">{item.content || item.error || item.command || 'No content'}</div>
      <div className="text-xs text-gray-400 mt-2">
        {item.user || 'unknown'} • ID {item.user_id || 'n/a'} • {item.guild || 'no guild'}
      </div>
      <details className="mt-2">
        <summary className="text-xs text-neonpurple">JSON</summary>
        <pre className="text-xs bg-[#07101F] p-2 rounded overflow-x-auto">{JSON.stringify(item, null, 2)}</pre>
      </details>
    </div>
  );
}

function LiveLogs() {
  const [logs, setLogs] = useState([]);
  const [filterUser, setFilterUser] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [status, setStatus] = useState('Connecting...');
  const wsRef = useRef(null);

  useEffect(() => {
    const fetchLogs = async () => {
      const res = await axios.get(`${API_BASE}/logs?limit=100`, { headers });
      setLogs(res.data);
    };

    fetchLogs().catch(console.error);

    const ws = new WebSocket(`${API_BASE.replace(/^http/, 'ws')}/ws`);
    wsRef.current = ws;

    ws.onopen = () => setStatus('Connected');
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLogs((prev) => [data, ...prev].slice(0, 100));
      } catch (error) {
        console.warn(error);
      }
    };
    ws.onclose = () => setStatus('Disconnected');
    ws.onerror = () => setStatus('Error');

    return () => ws.close();
  }, []);

  const filtered = useMemo(
    () =>
      logs.filter((l) => {
        const matchesUser = filterUser ? (l.user || '').toLowerCase().includes(filterUser.toLowerCase()) : true;
        const matchesType = typeFilter === 'all' ? true : l.type === typeFilter;
        return matchesUser && matchesType;
      }),
    [logs, filterUser, typeFilter]
  );

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center gap-3">
        <div className="text-sm text-gray-300">WebSocket status: {status}</div>
        <div className="flex gap-2">
          <input
            className="rounded px-3 py-2 bg-[#0D1330]"
            placeholder="Search by user"
            value={filterUser}
            onChange={(e) => setFilterUser(e.target.value)}
          />
          <select className="rounded px-3 py-2 bg-[#0D1330]" value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
            <option value="all">All</option>
            <option value="message">Message</option>
            <option value="command">Command</option>
            <option value="error">Error</option>
            <option value="system">System</option>
          </select>
        </div>
      </div>
      {filtered.length === 0 ? <div className="text-center text-gray-400">No logs found</div> : filtered.map((item) => <LogRow key={item.id} item={item} />)}
    </div>
  );
}

function ControlPanel() {
  const [channelId, setChannelId] = useState('');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState('Unknown');
  const [isSending, setIsSending] = useState(false);

  const checkStatus = async () => {
    try {
      const res = await axios.post(`${API_BASE}/control`, { action: 'get_status' }, { headers });
      setStatus(res.data.bot_online ? 'Online' : 'Offline');
    } catch (e) {
      setStatus('Unavailable');
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const send = async () => {
    if (!channelId || !message) return;
    setIsSending(true);
    try {
      await axios.post(`${API_BASE}/control`, { action: 'send_message', channel_id: Number(channelId), message }, { headers });
      setMessage('');
    } catch (e) {
      console.error(e);
      alert('Failed to queue message');
    }
    setIsSending(false);
  };

  return (
    <div className="space-y-4">
      <div className="card">
        <h2 className="text-xl mb-2">Control Panel</h2>
        <p>Bot status: <span className="font-bold">{status}</span></p>
      </div>

      <div className="card space-y-3">
        <input
          value={channelId}
          onChange={(e) => setChannelId(e.target.value)}
          placeholder="Channel ID"
          className="w-full rounded bg-[#0D1330] px-3 py-2"
        />
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Message"
          rows={4}
          className="w-full rounded bg-[#0D1330] px-3 py-2"
        />
        <button onClick={send} disabled={isSending} className="px-4 py-2 bg-neonblue text-black font-semibold rounded hover:opacity-90">
          {isSending ? 'Sending...' : 'Send Message'}
        </button>
      </div>
    </div>
  );
}

function ErrorViewer() {
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    const load = async () => {
      const res = await axios.get(`${API_BASE}/errors?limit=100`, { headers });
      setErrors(res.data);
    };
    load().catch(console.error);
  }, []);

  return (
    <div className="space-y-3">
      <h2 className="text-xl">Error Viewer</h2>
      {errors.map((e) => (
        <details className="card" key={e.id}>
          <summary className="cursor-pointer">{new Date(e.time).toLocaleString()} - {e.error?.slice(0, 100) || 'Error'}</summary>
          <pre className="text-xs bg-[#07101F] p-2 rounded mt-2 overflow-x-auto">{JSON.stringify(e, null, 2)}</pre>
        </details>
      ))}
    </div>
  );
}

function UserActivity() {
  const [users, setUsers] = useState([]);
  const [query, setQuery] = useState('');

  useEffect(() => {
    axios.get(`${API_BASE}/users?limit=200`, { headers }).then((res) => setUsers(res.data)).catch(console.error);
  }, []);

  const filtered = users.filter((u) => (u.user || '').toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="space-y-3">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search users"
        className="w-full rounded bg-[#0D1330] px-3 py-2"
      />
      <div className="grid md:grid-cols-2 gap-3">
        {filtered.map((u) => (
          <div key={`${u.user_id}-${u.user}`} className="card">
            <div className="flex justify-between">
              <strong>{u.user || 'Unknown'}</strong>
              <span className="text-gray-400">{u.actions} actions</span>
            </div>
            <p className="text-xs text-gray-500">ID: {u.user_id}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  const location = useLocation();
  const menu = [
    { path: '/', name: 'Dashboard' },
    { path: '/logs', name: 'Live Logs' },
    { path: '/control', name: 'Control Panel' },
    { path: '/errors', name: 'Errors' },
    { path: '/users', name: 'Users' },
  ];

  return (
    <div className="min-h-screen flex bg-bg text-white">
      <aside className="w-64 p-4 border-r border-neonblue/20 bg-[#070B1A]">
        <h1 className="text-2xl font-bold mb-4 text-neonpurple">Legend Star</h1>
        <nav className="space-y-2">
          {menu.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`block px-3 py-2 rounded ${location.pathname === item.path ? 'bg-neonblue text-black' : 'text-white hover:bg-[#151d45]'}`}
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </aside>

      <div className="flex-1 p-4 md:p-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/logs" element={<LiveLogs />} />
          <Route path="/control" element={<ControlPanel />} />
          <Route path="/errors" element={<ErrorViewer />} />
          <Route path="/users" element={<UserActivity />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;

