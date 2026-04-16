# REEFSIDE — Marine Conservation Simulator PRD

## Original Problem Statement
Build REEFSIDE: A cooperative, location-based marine conservation simulator from a previous 8-bit underwater Mario clone ("Aqua Quest"). The game is a pixel-based 8-bit side-scrolling game (similar visual style to Aqua Quest/Mario) with educational environmental themes based on a detailed design specification document.

## Core Requirements
- Full-screen pixel art 8-bit game (replaces Aqua Quest entirely)
- 4 Guardian roles with unique abilities (Marine Scientist, Indigenous Ranger, Sustainable Fisher, Climate Advocate)
- 10 reef zones with dynamic health system (RGB → greyscale bleaching)
- Cooperative zone restoration mechanics tied to UN SDG 14 / 30×30 Target
- Win condition: Protect 30% of reef (3+ zones > 60% health) by year 2030
- Climate events: Heatwaves, Cyclones (1.5x more frequent near 2030)
- Full HUD: Year counter, zone minimap, support meter, oxygen bar
- Submarine entry animation
- Glass morphism UI for non-game screens
- Web Audio API dynamic soundscape tied to reef health
- Educational content (SDG facts, Biodiversity tooltips)
- Immersive Submarine Hub replacing standard menus
- New animals: crabs, seahorses, whales, sharks
- Multiple level themes: night ocean, volcanic vent, shipwreck, arctic
- Whale Boss final level (gets swallowed, whale stomach scene)
- Vignette "Tide of Memories" (sepia overlay with guardian memories on zone restore)
- Mobile touch D-Pad
- Score multiplier for kill chains

## User Personas
- Target: 12-18 year old students
- Educational focus on marine conservation
- Should run well on low-spec school computers
- Accessible design

## Architecture
- `/app/frontend/src/components/UnderwaterGame.jsx` — Main orchestrator (Title → Hub → Game → End)
- `/app/frontend/src/components/SubmarineHub.jsx` — Immersive canvas lobby (closet, nav robot, hatch)
- `/app/frontend/src/components/GameCanvas.jsx` — Full REEFSIDE game engine (canvas, zones, physics, whale boss)
- `/app/frontend/src/components/GuardianSelect.jsx` — Legacy (no longer in flow)
- `/app/frontend/src/components/GameEndScreen.jsx` — Win/lose screen with SDG facts
- `/app/frontend/src/utils/sprites.js` — All pixel art sprites (diver, shark, dolphin, coral, crab, seahorse, whale, net, submarine interior)
- `/app/frontend/src/utils/levels.js` — 7 levels + boss (reef, deep, night, shipwreck, volcanic, arctic, boss)
- `/app/frontend/src/utils/audio.js` — Reef Symphony Web Audio API engine

### Phase 3: Audio Polish + Net Enemy + Text Cleanup (Feb 2026)
- FIXED: All em dashes replaced with colons/hyphens/commas across all user-visible text
- ADDED: Fishing net enemy (type='net') - stationary mid-water, entangles player on contact, stomped to clear (+200 pts), appears in SHIPWRECK/DEEP OCEAN/ARCTIC
- ADDED: playHit() SFX on player damage, playBubble() every 22 frames while swimming up, playNetEntangle() on net contact
- UPDATED: Tutorial page 5 includes FISHING NET enemy description

### Phase 2: Hub Expansion + Settings -- COMPLETE (Feb 2026)
- ✅ WASD bug fixed in SubmarineHub (added keyup handler — keys were permanently stuck)
- ✅ Arrow key preventDefault added in hub to stop browser scroll interference
- ✅ Biodiversity Catalog panel — 9 species cards (coral, shark, dolphin, jellyfish, squid, crown-of-thorns, crab, seahorse, whale)
- ✅ Catalog detail pane: name, scientific name, role, threat, field note
- ✅ Interactive glossary tooltips (hover terms like zooxanthellae, bleaching, symbiosis, etc.)
- ✅ WCAG Colorblind modes: Deuteranopia / Protanopia / High Contrast (CSS filter on game canvas)
- ✅ Settings panel with key remapping for all 6 actions (click → PRESS KEY → remap)
- ✅ Settings persisted in localStorage under 'reefside_settings'
- ✅ Reset to Defaults button
- ✅ settings.js utility (getSettings/setSettings/resetSettings/keyCodeLabel)
- ✅ New Catalog interact zone added to submarine hub canvas at floorX=860
- ✅ C key shortcut opens catalog from anywhere in hub
- ✅ S key shortcut opens settings from hub
- ✅ Hub HUD updated to show C/S shortcuts
- ✅ Major UI polish: corner accents, blink indicator lights, panel glow upgrades

### Phase 1: Core Game — COMPLETE
- ✅ Title screen (REEFSIDE logo, animated bubbles, glass morphism buttons, How To Play modal)
- ✅ Submarine Hub (immersive canvas interior with Equipment Bay, Mission Briefing, Navigator-7, Water Hatch)
- ✅ Full-screen canvas game (1200×700 internal coords, letterbox scaling)
- ✅ Submarine entry animation (submarine slides in, hatch opens, diver emerges)
- ✅ Zone health system (10 zones, 0-100% health, degradation + restoration)
- ✅ Dynamic bleaching visual (4 health states: vibrant → faded → pale → bleached white)
- ✅ Player diver physics (AABB, gravity, swim up, wall collision)
- ✅ Guardian abilities (E key, 30s cooldown, 4 unique abilities)
- ✅ Outfit system (3 suits with stat bonuses: standard, wetsuit, hazmat)
- ✅ Enemy types: Shark (bounce), Dolphin (launch/bounce), Jellyfish, Blooper, Crown of Thorns, Crab (floor walker), Seahorse (collectible)
- ✅ Whale Boss: tracks player, opens mouth, swallows, whale stomach cinematic scene
- ✅ Climate events: Heatwave (zone damage), Cyclone (debris + player push)
- ✅ Full HUD: Year (2025→2030), zone minimap, support meter, oxygen bar, pearls, kill chain
- ✅ Pearl collection (+zone health, +support)
- ✅ Power-ups: Oxygen Tank, Guardian Power
- ✅ Win/loss condition at year 2030 (3+ zones > 60%)
- ✅ Bloom event (particle burst when zone > 80%)
- ✅ Game End Screen (SDG facts, score, leaderboard submission)
- ✅ Tutorial tip (5s display at game start)
- ✅ Pause screen (P key)
- ✅ Flashlight in dark zones (health < 40%)
- ✅ Web Audio API dynamic soundscape (healthy → sparse → dissonant based on reef health)
- ✅ CRT overlay effect
- ✅ Score popups
- ✅ Vignette "Tide of Memories" (sepia overlay with guardian lore text on zone restore)
- ✅ Mobile Touch D-Pad (visible on touch/mobile devices)
- ✅ Kill chain multiplier (up to 4x)
- ✅ Level themes: reef, deep ocean, night, shipwreck, volcanic vent, arctic waters, boss
- ✅ Multiple level select via Navigator-7 in submarine hub
- ✅ Outfit select and guardian select via Equipment Bay in submarine hub
- ✅ Mission Briefing (6-page tutorial) in submarine hub
- ✅ Press Start 2P font throughout

## Key Technical Details
- Canvas: 1200×700 base coords, scaled to fill screen maintaining aspect ratio
- FLOOR_Y = 600, CEIL_Y = 82, HUD_TOP = 60, HUD_BOT = 50
- Zones: 10 × 1200px = 12000px total level width
- Year system: 1 year = 3000 frames (50s at 60fps), 5 years = 250s total game
- Zone protection threshold: health > 60% = "protected"
- Win: 3+ zones protected at year 2030 (30% = 30×30 SDG target)
- Climate events: every 40s (early game), every 20s (late game 2028+)
- Guardian abilities: 30s cooldown each

## Game Flow
Title Screen → BEGIN MISSION → Submarine Hub (canvas lobby) → Walk to WATER HATCH → [E] DIVE IN → Game → Game End Screen

## Prioritized Backlog

### P1 (High Priority)
- Archive/Biodiversity Catalog screen (species info, tooltips for zooxanthellae, symbiosis etc.)
- Colorblind mode toggle (WCAG compliant)

### P2 (Nice to Have)
- WASD key remapping settings screen
- More enemy variety (illegal fishing net enemy — sprites already done)
- Audio polish (specific SFX for swim bubble, coin, hit)

### P3 (Future)
- Real-time multiplayer presence channels (multiple roles in same session)

## Known Constraints
- Single-player only (cooperative mechanics simulated via 4 Guardian roles accessible to 1 player)
- Audio disabled by default (user must press M to enable)
- No authentication required

## API Endpoints Used
- `POST /api/leaderboard` — Submit score at game end
- `GET /api/leaderboard` — Fetch top scores
