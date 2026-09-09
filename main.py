"""
Main entry point for Jili Desktop Pet
"""
import sys
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from config import (PET_WINDOW_SIZE, RANDOM_CHAT_MIN, RANDOM_CHAT_MAX,
                     DEFAULT_EYE_INTERVAL, DEFAULT_WATER_INTERVAL, DEFAULT_ACTIVITY_INTERVAL,
                     RANDOM_CHAT_MESSAGES, EYE_REMINDER_MESSAGES, WATER_REMINDER_MESSAGES,
                     ACTIVITY_REMINDER_MESSAGES, SMALL_BUBBLE_DURATION)
from sprite_generator import SpriteGenerator
from pet import PetWindow
from states import PetState, StateMachine
from animations import AnimationManager
from interactions import InteractionManager
from bubble import ChatBubble


class JiliApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        print("Initializing components...")
        self._init_sprite_generator()
        self._init_pet_window()
        self._init_animation_manager()
        self._init_interaction_manager()
        self._init_state_machine()
        self._init_bubble()
        self._wire_components()
        self._start_application()

    def _init_sprite_generator(self):
        print("Creating sprite generator...")
        self.sprite_generator = SpriteGenerator()
        self.frames = self.sprite_generator.generate_all_sprites()
        print(f"Generated {len(self.frames)} state frame sets")

    def _init_pet_window(self):
        print("Creating pet window...")
        self.pet_window = PetWindow()
        print("Pet window created")

    def _init_animation_manager(self):
        print("Creating animation manager...")
        self.animation_manager = AnimationManager()
        for state, frames in self.frames.items():
            self.animation_manager.load_frames(state, frames)
        self.animation_manager.start_animation()
        print("Animation manager created and started")

    def _init_interaction_manager(self):
        print("Creating interaction manager...")
        self.interaction_manager = InteractionManager(self.pet_window)
        self.pet_window.set_interaction_manager(self.interaction_manager)
        print("Interaction manager created")

    def _init_state_machine(self):
        print("Creating state machine...")
        self.state_machine = StateMachine()

        def on_state_changed(new_state):
            self.animation_manager.set_state(new_state)
            if new_state == PetState.WALKING:
                screen = QApplication.primaryScreen()
                screen_geometry = screen.availableGeometry()
                target_x = random.randint(50, screen_geometry.width() - 250)
                self.pet_window.start_walking(target_x)
            elif new_state == PetState.IDLE:
                self.pet_window.stop_walking()
                # Update bubble position when stopping
                self.chat_bubble.position_above_pet(self.pet_window)

        self.state_machine.state_changed.connect(on_state_changed)
        print("State machine created")

    def _init_bubble(self):
        print("Creating chat bubble...")
        self.chat_bubble = ChatBubble()
        print("Chat bubble created")
        self.eye_interval = DEFAULT_EYE_INTERVAL
        self.water_interval = DEFAULT_WATER_INTERVAL
        self.activity_interval = DEFAULT_ACTIVITY_INTERVAL

    def _wire_components(self):
        # Stop everything when exit is triggered
        def on_exit():
            self.auto_timer.stop()
            self.chat_timer.stop()
            self.eye_timer.stop()
            self.water_timer.stop()
            self.activity_timer.stop()
            self.visibility_check_timer.stop()
            self.chat_bubble.hide()
            self.pet_window.hide()

        self.app.aboutToQuit.connect(on_exit)
        print("Wiring components...")
        self.animation_manager.frame_ready.connect(self.pet_window.set_sprite)
        self.interaction_manager.request_state_change.connect(self.animation_manager.set_state)
        self.interaction_manager.request_jump.connect(self.pet_window.jump)
        self.interaction_manager.open_reminder_settings.connect(self._show_reminder_settings_dialog)
        self.interaction_manager.show_about.connect(self._show_about_dialog)

        def on_drag_started():
            self.auto_timer.stop()
            self.state_machine.set_state(PetState.DRAGGING)
            self.chat_bubble.hide()

        def on_drag_ended():
            self.state_machine.set_state(PetState.IDLE)
            self.auto_timer.start(6000)
            # Update bubble position after drag ends
            self.chat_bubble.position_above_pet(self.pet_window)

        self.pet_window.drag_started.connect(on_drag_started)
        self.pet_window.drag_ended.connect(on_drag_ended)
        self.pet_window.position_changed.connect(self._update_bubble_position)
        print("Components wired")

    def _show_reminder_settings_dialog(self):
        print("Reminder settings dialog requested")
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QHBoxLayout
        from PyQt5.QtCore import Qt
        dialog = QDialog()
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        dialog.setWindowTitle("Reminder Settings")
        dialog.setFixedSize(300, 200)
        layout = QVBoxLayout()

        eye_layout = QHBoxLayout()
        eye_label = QLabel("Eye Reminder (min):")
        eye_spin = QSpinBox()
        eye_spin.setRange(1, 7200)
        eye_spin.setValue(self.eye_interval)
        eye_spin.setSuffix(" min")
        eye_layout.addWidget(eye_label)
        eye_layout.addWidget(eye_spin)
        layout.addLayout(eye_layout)

        water_layout = QHBoxLayout()
        water_label = QLabel("Water Reminder (min):")
        water_spin = QSpinBox()
        water_spin.setRange(1, 7200)
        water_spin.setValue(self.water_interval)
        water_spin.setSuffix(" min")
        water_layout.addWidget(water_label)
        water_layout.addWidget(water_spin)
        layout.addLayout(water_layout)

        activity_layout = QHBoxLayout()
        activity_label = QLabel("Activity Reminder (min):")
        activity_spin = QSpinBox()
        activity_spin.setRange(1, 7200)
        activity_spin.setValue(self.activity_interval)
        activity_spin.setSuffix(" min")
        activity_layout.addWidget(activity_label)
        activity_layout.addWidget(activity_spin)
        layout.addLayout(activity_layout)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            self.eye_interval = eye_spin.value()
            self.water_interval = water_spin.value()
            self.activity_interval = activity_spin.value()
            print(f"Settings saved: Eye={self.eye_interval}, Water={self.water_interval}, Activity={self.activity_interval}")
            self._restart_reminder_timers()

    def _show_about_dialog(self):
        print("About dialog requested")
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("About Jili")
        msg.setText("Jili Desktop Pet v1.0\n\nA cute tiger desktop pet\n\nFeatures:\n- Transparent window, always on top\n- Drag and drop interaction\n- Timed reminders\n- Cute animations\n\nMade with love by RQ")
        msg.exec_()

    def _start_application(self):
        print("Starting application...")
        print("Setting initial state...")
        self.animation_manager.set_state(PetState.IDLE)
        print("Initial state set")

        self.pet_window.show()
        print("Pet window shown")
        self.pet_window.raise_()
        self.pet_window.activateWindow()
        self.pet_window.update()
        print("Window updated")
        print("Jili Desktop Pet started successfully!")

        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self._auto_behavior)
        self.auto_timer.start(8000)

        # Add visibility check timer
        self.visibility_check_timer = QTimer()
        self.visibility_check_timer.timeout.connect(self._check_pet_visibility)
        self.visibility_check_timer.start(5000)  # Check every 5 seconds

        self._start_random_chat_timer()
        self._start_reminder_timers()

    def _start_random_chat_timer(self):
        interval = random.randint(RANDOM_CHAT_MIN, RANDOM_CHAT_MAX) * 1000
        self.chat_timer = QTimer()
        self.chat_timer.timeout.connect(self._show_random_chat)
        self.chat_timer.start(interval)
        print(f"Random chat timer started (interval: {interval/1000}s)")

    def _show_random_chat(self):
        try:
            message = random.choice(RANDOM_CHAT_MESSAGES)
            self.chat_bubble.show_message(message, SMALL_BUBBLE_DURATION)
            # Update position after showing to ensure it's above current pet position
            self.chat_bubble.position_above_pet(self.pet_window)
            print(f"Random chat shown: {message}")
        except Exception as e:
            print(f"Random chat error: {e}")
            import traceback
            traceback.print_exc()
        interval = random.randint(RANDOM_CHAT_MIN, RANDOM_CHAT_MAX) * 1000
        self.chat_timer.start(interval)

    def _start_reminder_timers(self):
        self.eye_timer = QTimer()
        self.eye_timer.timeout.connect(self._show_eye_reminder)
        self.eye_timer.start(self.eye_interval * 60 * 1000)
        print(f"Eye reminder timer started (interval: {self.eye_interval} min)")

        self.water_timer = QTimer()
        self.water_timer.timeout.connect(self._show_water_reminder)
        self.water_timer.start(self.water_interval * 60 * 1000)
        print(f"Water reminder timer started (interval: {self.water_interval} min)")

        self.activity_timer = QTimer()
        self.activity_timer.timeout.connect(self._show_activity_reminder)
        self.activity_timer.start(self.activity_interval * 60 * 1000)
        print(f"Activity reminder timer started (interval: {self.activity_interval} min)")

    def _restart_reminder_timers(self):
        self.eye_timer.stop()
        self.water_timer.stop()
        self.activity_timer.stop()
        self.eye_timer.start(self.eye_interval * 60 * 1000)
        self.water_timer.start(self.water_interval * 60 * 1000)
        self.activity_timer.start(self.activity_interval * 60 * 1000)
        print(f"Timers restarted: Eye={self.eye_interval}min, Water={self.water_interval}min, Activity={self.activity_interval}min")

    def _show_eye_reminder(self):
        try:
            message = random.choice(EYE_REMINDER_MESSAGES).format(minutes=self.eye_interval)
            self.chat_bubble.show_message(message, 10000)
            # Update position after showing to ensure it's above current pet position
            self.chat_bubble.position_above_pet(self.pet_window)
            self.animation_manager.set_state(PetState.REMINDING)
            QTimer.singleShot(5000, lambda: self.animation_manager.set_state(PetState.IDLE))
        except Exception as e:
            print(f"Eye reminder error: {e}")

    def _show_water_reminder(self):
        try:
            message = random.choice(WATER_REMINDER_MESSAGES)
            self.chat_bubble.show_message(message, 10000)
            # Update position after showing to ensure it's above current pet position
            self.chat_bubble.position_above_pet(self.pet_window)
            self.animation_manager.set_state(PetState.REMINDING)
            QTimer.singleShot(5000, lambda: self.animation_manager.set_state(PetState.IDLE))
        except Exception as e:
            print(f"Water reminder error: {e}")

    def _show_activity_reminder(self):
        try:
            message = random.choice(ACTIVITY_REMINDER_MESSAGES)
            self.chat_bubble.show_message(message, 10000)
            # Update position after showing to ensure it's above current pet position
            self.chat_bubble.position_above_pet(self.pet_window)
            self.animation_manager.set_state(PetState.REMINDING)
            QTimer.singleShot(5000, lambda: self.animation_manager.set_state(PetState.IDLE))
        except Exception as e:
            print(f"Activity reminder error: {e}")

    def _update_bubble_position(self, x, y):
        # Always update bubble position, even if not visible
        # This ensures bubble is at correct position when it becomes visible
        self.chat_bubble.position_above_pet(self.pet_window)

        # Ensure pet window stays visible
        if not self.pet_window.isVisible():
            print("Warning: Pet window became invisible, showing it again")
            self.pet_window.show()
            self.pet_window.raise_()

    def _auto_behavior(self):
        current = self.state_machine.get_current_state()
        if current == PetState.IDLE:
            if random.random() < 0.6:  
                self.state_machine.set_state(PetState.WALKING)
        elif current == PetState.WALKING:
            if random.random() < 0.3:  
                self.state_machine.set_state(PetState.IDLE)
        elif current in [PetState.REMINDING, PetState.WAVING, PetState.EATING]:
            self.state_machine.set_state(PetState.IDLE)

    def _check_pet_visibility(self):
        """Periodically check if pet window is still visible"""
        if not self.pet_window.isVisible():
            print("WARNING: Pet window became invisible! Restoring...")
            self.pet_window.show()
            self.pet_window.raise_()
            self.pet_window.activateWindow()
            print("Pet window restored")

    def run(self):
        print("Starting event loop...")
        result = self.app.exec_()
        print(f"Event loop ended with code: {result}")
        return result


def main():
    try:
        print("Creating JiliApp...")
        app = JiliApp()
        print("JiliApp created, running...")
        app.pet_window.update()
        app.app.processEvents()

        # Install global exception handler
        def handle_exception(exc_type, exc_value, exc_traceback):
            print("=== UNHANDLED EXCEPTION ===")
            import traceback
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print("==========================")

        sys.excepthook = handle_exception

        sys.exit(app.run())
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
