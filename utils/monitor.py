"""
Performance Monitor - System Performance Monitoring
===================================================

Monitors and tracks performance metrics for the contextual engine
including response times, resource utilization, and efficiency metrics.
"""

import time
import psutil
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import deque

@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    response_time: float
    requests_processed: int
    success_rate: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class PerformanceMonitor:
    """Monitors system and application performance"""
    
    def __init__(self, max_history_size: int = 1000):
        self.max_history_size = max_history_size
        self.metrics_history = deque(maxlen=max_history_size)
        self.request_times = deque(maxlen=100)  # Last 100 requests
        
        # Counters
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        # Performance tracking
        self.start_time = time.time()
        self.last_snapshot_time = time.time()
        
    def record_request(self, processing_time: float, input_size: int, output_size: int):
        """Record a request for performance tracking"""
        self.total_requests += 1
        self.request_times.append(processing_time)
        
        # Determine success based on reasonable processing time
        if processing_time < 30.0:  # 30 second timeout
            self.successful_requests += 1
        else:
            self.failed_requests += 1
    
    def record_success(self):
        """Record a successful operation"""
        self.successful_requests += 1
    
    def record_failure(self):
        """Record a failed operation"""
        self.failed_requests += 1
    
    def take_snapshot(self, metadata: Optional[Dict[str, Any]] = None) -> PerformanceMetrics:
        """Take a performance snapshot"""
        current_time = time.time()
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        
        # Calculate response time metrics
        if self.request_times:
            avg_response_time = sum(self.request_times) / len(self.request_times)
        else:
            avg_response_time = 0.0
        
        # Calculate success rate
        if self.total_requests > 0:
            success_rate = self.successful_requests / self.total_requests
        else:
            success_rate = 1.0
        
        # Create metrics snapshot
        metrics = PerformanceMetrics(
            timestamp=current_time,
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            response_time=avg_response_time,
            requests_processed=self.total_requests,
            success_rate=success_rate,
            metadata=metadata or {}
        )
        
        # Add to history
        self.metrics_history.append(metrics)
        self.last_snapshot_time = current_time
        
        return metrics
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        snapshot = self.take_snapshot()
        
        return {
            "current_snapshot": {
                "cpu_percent": snapshot.cpu_percent,
                "memory_percent": snapshot.memory_percent,
                "avg_response_time": snapshot.response_time,
                "success_rate": snapshot.success_rate
            },
            "cumulative_stats": {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "uptime_seconds": time.time() - self.start_time
            },
            "recent_performance": self._get_recent_performance_summary()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        return self.get_current_metrics()
    
    def _get_recent_performance_summary(self) -> Dict[str, Any]:
        """Get summary of recent performance"""
        if not self.metrics_history:
            return {"no_data": True}
        
        recent_metrics = list(self.metrics_history)[-10:]  # Last 10 snapshots
        
        if not recent_metrics:
            return {"insufficient_data": True}
        
        # Calculate averages
        avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        avg_response_time = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        avg_success_rate = sum(m.success_rate for m in recent_metrics) / len(recent_metrics)
        
        return {
            "avg_cpu_percent": avg_cpu,
            "avg_memory_percent": avg_memory,
            "avg_response_time": avg_response_time,
            "avg_success_rate": avg_success_rate,
            "snapshots_analyzed": len(recent_metrics)
        }
    
    def get_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        if len(self.metrics_history) < 2:
            return {"trend_analysis": "insufficient_data"}
        
        metrics_list = list(self.metrics_history)
        
        # Compare recent vs older metrics
        recent_metrics = metrics_list[-5:] if len(metrics_list) >= 5 else metrics_list
        older_metrics = metrics_list[:-5] if len(metrics_list) >= 10 else metrics_list[:-len(recent_metrics)]
        
        if not older_metrics:
            return {"trend_analysis": "insufficient_historical_data"}
        
        # Calculate trends
        recent_avg_response = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        older_avg_response = sum(m.response_time for m in older_metrics) / len(older_metrics)
        
        recent_avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        older_avg_cpu = sum(m.cpu_percent for m in older_metrics) / len(older_metrics)
        
        recent_avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        older_avg_memory = sum(m.memory_percent for m in older_metrics) / len(older_metrics)
        
        return {
            "trend_analysis": "available",
            "response_time_trend": {
                "direction": "improving" if recent_avg_response < older_avg_response else "degrading",
                "recent_avg": recent_avg_response,
                "older_avg": older_avg_response,
                "change": recent_avg_response - older_avg_response
            },
            "cpu_usage_trend": {
                "direction": "increasing" if recent_avg_cpu > older_avg_cpu else "decreasing",
                "recent_avg": recent_avg_cpu,
                "older_avg": older_avg_cpu,
                "change": recent_avg_cpu - older_avg_cpu
            },
            "memory_usage_trend": {
                "direction": "increasing" if recent_avg_memory > older_avg_memory else "decreasing",
                "recent_avg": recent_avg_memory,
                "older_avg": older_avg_memory,
                "change": recent_avg_memory - older_avg_memory
            }
        }
    
    def get_performance_alerts(self) -> List[Dict[str, Any]]:
        """Get performance alerts based on thresholds"""
        alerts = []
        
        if not self.metrics_history:
            return alerts
        
        latest_metrics = self.metrics_history[-1]
        
        # CPU usage alert
        if latest_metrics.cpu_percent > 80:
            alerts.append({
                "type": "high_cpu_usage",
                "severity": "warning" if latest_metrics.cpu_percent < 90 else "critical",
                "value": latest_metrics.cpu_percent,
                "threshold": 80,
                "message": f"High CPU usage: {latest_metrics.cpu_percent:.1f}%"
            })
        
        # Memory usage alert
        if latest_metrics.memory_percent > 85:
            alerts.append({
                "type": "high_memory_usage",
                "severity": "warning" if latest_metrics.memory_percent < 95 else "critical",
                "value": latest_metrics.memory_percent,
                "threshold": 85,
                "message": f"High memory usage: {latest_metrics.memory_percent:.1f}%"
            })
        
        # Response time alert
        if latest_metrics.response_time > 5.0:
            alerts.append({
                "type": "slow_response_time",
                "severity": "warning" if latest_metrics.response_time < 10.0 else "critical",
                "value": latest_metrics.response_time,
                "threshold": 5.0,
                "message": f"Slow response time: {latest_metrics.response_time:.2f}s"
            })
        
        # Success rate alert
        if latest_metrics.success_rate < 0.95:
            alerts.append({
                "type": "low_success_rate",
                "severity": "warning" if latest_metrics.success_rate > 0.85 else "critical",
                "value": latest_metrics.success_rate,
                "threshold": 0.95,
                "message": f"Low success rate: {latest_metrics.success_rate:.2%}"
            })
        
        return alerts
    
    def export_metrics(
        self, 
        start_time: Optional[float] = None, 
        end_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """Export metrics within time range"""
        current_time = time.time()
        start_time = start_time or (current_time - 3600)  # Default: last hour
        end_time = end_time or current_time
        
        filtered_metrics = [
            metrics for metrics in self.metrics_history
            if start_time <= metrics.timestamp <= end_time
        ]
        
        return {
            "export_timestamp": current_time,
            "time_range": {"start": start_time, "end": end_time},
            "metrics_count": len(filtered_metrics),
            "metrics": [
                {
                    "timestamp": m.timestamp,
                    "cpu_percent": m.cpu_percent,
                    "memory_percent": m.memory_percent,
                    "response_time": m.response_time,
                    "requests_processed": m.requests_processed,
                    "success_rate": m.success_rate,
                    "metadata": m.metadata
                }
                for m in filtered_metrics
            ]
        }
    
    def reset(self):
        """Reset performance monitoring state"""
        self.metrics_history.clear()
        self.request_times.clear()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = time.time()
        self.last_snapshot_time = time.time()