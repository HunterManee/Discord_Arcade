SYSTEM ARCHITECTURE OVERVIEW
----------------------------
Discord Arcade is a modular multiplayer platform built on Discord that explores
real-time system design through a distributed client/server architecture.

Core Responsiblities
- Client Bot      -> interaction handling + interface layer
- Host Server     -> game orchestration and authoritative state
- WebSocket layer -> real-time synchronization

Component                    |System Design
-----------------------------|---------------------
Client_Bot                   |Interface Layer / Client Node
Server_Bot                   |Authoritative Backend Service
WebSocket package            |Communication Protocol
Game.py base class           |Plugin Architecute / Extensible Module System
Channel Commands             |Routing Layer

DESIGN DECISIONS
----------------
Cient/Server Separation
The project separates client interaction from server-side logic to:
- Maintain clean responsibility boundaries
- Allow scalable game management
- Mirror patterns commonly used in real-world backend systems

Modular Game Architecture
Games inherit from a base structure to:
- Enforce consistent interfaces across game implementations
- Reduce duplication
- Allow easy extension

Channel-Based Command Routing
Different channel contexts allow tailored interation flows without 
tightly coupling logic to Discord event handlers.

MESSAGE FLOW
------------
1. User issues command through Discord.
2. Client Bot transforms user input into structured events and
   forwards them to the Host Server.
4. WebSocket layer transmits event to Host Server.
5. Host Server updates game state.
6. Server broadcasts update to connected clients.
7. Client Bots render updated game state.

ENGINEERING CHALLENGES
----------------------
Real-Time State Synchronization
Maintaining consistent game state across multiple users required implementing event-
based updates via WebSockets.

Session Management
Mapping users and channels to active game instances introduced lifecycle and
synchronization challenges

Command Routing
Different Discord contexts required a structured command hierachy to prevent tightly
coupled logic

SYSTEM DESIGN PERSPECTIVE
-------------------------
Discord Arcade conceptually models a simplified distributed system:
- Clients act as interactionnodes handling user input.
- The Host Server maintains authoritative game states.
- WebSocket messaging enables real-time propagation.
- Game modules operate as pluggable services within the system.

This design mirrors patterns used in:
- Multiplayer game servers
- Event-driven backend systems.
- Real-time collaboration platforms.
