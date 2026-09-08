\---

name: desktop-pet-development

description: Build PyQt5 desktop pet applications with transparent windows, drag interaction, chat bubbles, and timed reminders

tags: \[pyqt5, desktop-pet, python, animation, windows]

\---



\# Desktop Pet Development Skill



\## Overview

A complete desktop pet application using PyQt5, featuring a cute tiger character drawn entirely with QPainter (no external images).



\## Architecture



main.py              - Main entry, wires all components

config.py            - All constants (colors, sizes, timings, messages)

sprite\_generator.py  - Generate animation frames with QPainter

pet.py               - Transparent window with drag/drop physics

animations.py        - Frame sequencing and state-based animation

states.py            - PetState enum + StateMachine for state transitions

interactions.py      - Right-click menu, click/double-click handlers

bubble.py            - Chat bubble with fade animation

reminders.py         - Reminder manager with message pools



\## Key Techniques



\### Transparent Window

\- Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool

\- Qt.WA\_TranslucentBackground

\- Never set WA\_TransparentForMouseEvents(True) in \_\_init\_\_



\### Animation System

\- QTimer drives frame cycling

\- AnimationManager emits pyqtSignal(QPixmap) for each frame

\- current\_state must init as None, not PetState.IDLE, otherwise set\_state() skips initialization



\### Drag and Physics

\- mousePressEvent starts drag, stops walking and physics first

\- mouseReleaseEvent triggers falling with gravity + bounce

\- Stop auto\_timer during drag, restart after drop



\### Chat Bubble

\- Separate QWidget with WA\_TranslucentBackground

\- QPropertyAnimation for fade in/out

\- bubble.hide() must disconnect fade\_animation.finished to prevent crash

\- Position above pet, clamp to screen bounds



\### Entry Animation

\- Skip entry animation (fall from top), directly show at bottom position

\- \_start\_entry\_animation should just call \_initialize\_position()



\### Event Handlers

\- \_set\_click\_through, enterEvent, leaveEvent should be pass (no-op)

\- Right-click shows context menu via interaction\_manager.show\_context\_menu(event.globalPos())



\## Known Pitfalls (IMPORTANT)



1\. AnimationManager.\_\_init\_\_: self.current\_state = None (NOT PetState.IDLE)

2\. Never enable WA\_TransparentForMouseEvents in PetWindow.\_\_init\_\_

3\. bubble.hide() must try: self.fade\_animation.finished.disconnect() before starting fade

4\. Dialog windows need Qt.WindowStaysOnTopHint or they hide behind the pet

5\. Walking state must stop physics\_timer and walking\_target before drag starts

6\. \_show\_random\_chat should have try-except to prevent crash

7\. Timer intervals: use minutes \* 60 \* 1000 for milliseconds conversion

8\. On company Windows PCs, use python -m pip instead of pip directly

9\. PowerShell may need Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned for venv



\## QPainter Character Drawing Tips



\- Use SPRITE\_SIZE=256 for good detail

\- Big head (60%) + small body (40%) ratio for cute Q-style

\- Round shapes only (ellipses, rounded rects), no sharp corners

\- Tiger features: wang character on forehead with RoundCap strokes, cheek stripes, body stripes

\- All line strokes use Qt.RoundCap for soft look

\- Use deep brown (#8B4513) not black for stripes and details

\- Draw order: tail, body, legs, arms, head, face, effects (hearts/Zzz)

\- Wang character: three horizontal lines + one vertical, use QPen with RoundCap, deep brown color



\## States



IDLE, WALKING, DRAGGING, FALLING, SLEEPING, EATING, WAVING, REMINDING



\## Auto Behavior System



\- QTimer every 8 seconds checks whether to switch between IDLE and WALKING

\- 50% probability to start walking when idle

\- Random target\_x position across screen width

\- Stop auto\_timer during drag, restart after drop



\## Reminder System



\- Three independent QTimers for eye, water, activity reminders

\- Configurable intervals via right-click menu dialog

\- Random messages from config.py message pools

\- Chat bubble displays reminder text above pet



\## Dependencies



\- PyQt5 >= 5.15.0

\- Python >= 3.8

\- Windows OS (optimized for Windows)

