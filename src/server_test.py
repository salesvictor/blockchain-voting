from api import *
import election_coordinator

coordinator = election_coordinator.ElectionCoordinator(RPC_SERVER_ADDR)
coordinator.start()
