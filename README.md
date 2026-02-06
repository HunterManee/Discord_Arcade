SYSTEM ARCHITECTURE OVERVIEW
----------------------------
Discord Arcade uses a distrubuted bot architecture consisting of a Host Server and
Game Client componetns communicating through a WEbSocket-based messaging layer.

High-level flow:\n
Discord Users
     |
     V
Websocket Communication Layer
     |
     V
Host Server Bot
     |
     V
Game Logic + Session Management

Responsiblities
- Client Bot      -> interaction handling + UI ayer
- Host SErver     -> game orchestration and authoritative state
- WebSocket layer -> real-time synchronization

Component                    |System Design
-----------------------------|---------------------
Client_Bot                   |Interface Layer / Client Node
Server_Bot                   |Authoritative Backend Service
WebSocket package            |Communication Protocol
Game.py base class           |Plugin Architecute
Channel Commands             |Routing Layer

DESIGN DECISIONS
----------------
Cient/Server Separation
The project separates client interaction from server-side logic to:
- maintain clean responsibility boundaries
- allow scalable game management
- simulate real backend service patterns

Modular Game Architecture
Games inherit from a base structure to:
- ensure consistent intergaces
- reduce duplication
- allow easy extension

Channel-Based Command Routing
Different channel contexts allow tailored interation flows without tightly coupling logic
to Discord event handlers.

MESSAGE FLOW
------------
1. User issues command through Discord.
2. Client Bot processes input and forwards structed message.
3. WebSocket layer transmits event to Host Server.
4. Host Server updates game state.
5. Server broadcasts update to connected clients.
6. Client Bots render updated game state.

ENGINEERING CHALLENGES
----------------------
Real-Time State Synchronization
Maintaining consistent game state acroos multiple users required implimenting event-
basewd updates via WebSockets.

Session Management
Mapping users and channels to active game instances introduced complexity around
lifecycle managment and clearnup logic.

Command Routing
Digerent Discord contexts required a structured command hierachy to prevvent tightly
coupled logic

SYSTEM DESIGN PERSPECTIVE
-------------------------
Discord Arcade Models a simplifed distributed system:
- Clients act as interactionnodes handling user input.
- The Host Server maintains authoritative game states.
- WebSocket messaging enables real-time propagation.
- Game modules operate as pluggable services within the system.

This design mirrors patterns used in:
- multiplayer game servers
- event-driven backend systems.
- real-time collaboration platforms.
