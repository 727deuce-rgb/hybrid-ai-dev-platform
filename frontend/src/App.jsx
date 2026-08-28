import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSystemStatus();
    const interval = setInterval(fetchSystemStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchSystemStatus = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/system/status');
      setSystemStatus(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">
          <h1>● DRACO-4</h1>
          <p>Distributed Reasoning and Collaborative Orchestration</p>
        </div>
        <nav className="app-nav">
          <button
            className={activeTab === 'dashboard' ? 'active' : ''}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={activeTab === 'agents' ? 'active' : ''}
            onClick={() => setActiveTab('agents')}
          >
            Agents
          </button>
          <button
            className={activeTab === 'apps' ? 'active' : ''}
            onClick={() => setActiveTab('apps')}
          >
            Mini-Stacks
          </button>
          <button
            className={activeTab === 'monitor' ? 'active' : ''}
            onClick={() => setActiveTab('monitor')}
          >
            Monitor
          </button>
        </nav>
      </header>

      <main className="app-main">
        {loading && <div className="spinner">Loading...</div>}
        {error && <div className="error-banner">{error}</div>}

        {activeTab === 'dashboard' && (
          <DashboardView systemStatus={systemStatus} />
        )}
        {activeTab === 'agents' && (
          <AgentsView systemStatus={systemStatus} />
        )}
        {activeTab === 'apps' && <AppsView />}
        {activeTab === 'monitor' && <MonitorView />}
      </main>
    </div>
  );
};

const DashboardView = ({ systemStatus }) => (
  <div className="dashboard-view">
    <h2>System Overview</h2>
    {systemStatus && (
      <div className="status-grid">
        <div className="status-card">
          <h3>Status</h3>
          <p className={systemStatus.initialized ? 'status-ok' : 'status-err'}>
            {systemStatus.initialized ? '✓ Initialized' : '✗ Not Ready'}
          </p>
        </div>
        <div className="status-card">
          <h3>Total Agents</h3>
          <p className="metric">{systemStatus.total_agents || 0}</p>
        </div>
        <div className="status-card">
          <h3>Last Update</h3>
          <p className="timestamp">{systemStatus.timestamp}</p>
        </div>
      </div>
    )}
  </div>
);

const AgentsView = ({ systemStatus }) => (
  <div className="agents-view">
    <h2>Pillar Agents</h2>
    {systemStatus?.agents && (
      <div className="agents-grid">
        {Object.entries(systemStatus.agents).map(([id, agent]) => (
          <AgentCard key={id} agentId={id} agent={agent} />
        ))}
      </div>
    )}
  </div>
);

const AgentCard = ({ agentId, agent }) => (
  <div className="agent-card">
    <h3>{agentId}</h3>
    <div className="agent-details">
      <p><strong>Role:</strong> {agent.role}</p>
      <p><strong>Pattern:</strong> {agent.pattern}</p>
      <p><strong>Tasks:</strong> {agent.metrics?.tasks_processed || 0}</p>
      <p><strong>Avg Response:</strong> {agent.metrics?.avg_response_time_ms?.toFixed(2) || 0}ms</p>
    </div>
  </div>
);

const AppsView = () => (
  <div className="apps-view">
    <h2>Mini-Stack Applications</h2>
    <div className="apps-grid">
      <AppCard
        title="App 1: Perceptron"
        pattern="Monad"
        nodes={1}
        params={12}
        purpose="Binary classification"
      />
      <AppCard
        title="App 2: Comparator"
        pattern="Dyad"
        nodes={2}
        params={256}
        purpose="A/B comparison"
      />
      <AppCard
        title="App 3: Validator"
        pattern="Triad"
        nodes={3}
        params={1024}
        purpose="Triangulated decisions"
      />
      <AppCard
        title="App 4: DRACO Hub"
        pattern="Tetrad"
        nodes={4}
        params={4096}
        purpose="Multi-agent coordination"
      />
      <AppCard
        title="App 5: Expander"
        pattern="Pentad"
        nodes={5}
        params={8192}
        purpose="Distributed inference"
      />
    </div>
  </div>
);

const AppCard = ({ title, pattern, nodes, params, purpose }) => (
  <div className="app-card">
    <h3>{title}</h3>
    <div className="app-info">
      <p><strong>Pattern:</strong> {pattern}</p>
      <p><strong>Nodes:</strong> {nodes}</p>
      <p><strong>Params:</strong> {params}</p>
      <p className="purpose">{purpose}</p>
    </div>
  </div>
);

const MonitorView = () => (
  <div className="monitor-view">
    <h2>System Monitor</h2>
    <div className="monitor-grid">
      <MetricCard label="CPU Usage" value="42%" status="ok" />
      <MetricCard label="Memory" value="512MB / 1280MB" status="ok" />
      <MetricCard label="Network" value="2.3 Mbps" status="ok" />
      <MetricCard label="Tasks/min" value="847" status="ok" />
    </div>
  </div>
);

const MetricCard = ({ label, value, status }) => (
  <div className={`metric-card status-${status}`}>
    <p className="label">{label}</p>
    <p className="value">{value}</p>
  </div>
);

export default App;
