import pytest
from unittest.mock import patch, AsyncMock
from app.core.edge.failover.manager import failover_manager

@pytest.mark.asyncio
async def test_failover_manager():
    with patch("app.core.edge.failover.manager.leader_election.acquire_leadership", new_callable=AsyncMock) as mock_acquire:
        # Simulate successful acquisition
        mock_acquire.return_value = (True, 42)
        await failover_manager.handle_node_failure("node_1", "US-EAST", "node_2")
        mock_acquire.assert_called_once_with("US-EAST", "node_2")

    with patch("app.core.edge.failover.manager.leader_election.acquire_leadership", new_callable=AsyncMock) as mock_acquire:
        with patch("app.core.edge.failover.manager.degraded_engine.activate_degraded_mode") as mock_degraded:
            # Simulate failed acquisition (split-brain prevention)
            mock_acquire.return_value = (False, None)
            await failover_manager.handle_node_failure("node_1", "US-EAST", "node_3")
            mock_degraded.assert_called_once_with("node_3")
