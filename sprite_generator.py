"""
Sprite generator for 吉布丁 Desktop Pet
Creates all character animation frames using QPainter
"""

from PyQt5.QtCore import Qt, QSize, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPixmap, QColor, QPen, QBrush, QPainterPath, QFont
from config import (
    COLOR_TIGER_ORANGE, COLOR_TIGER_WHITE, COLOR_TIGER_STRIPE, COLOR_TIGER_NOSE,
    COLOR_TIGER_EAR_INNER, COLOR_TIGER_EYE, COLOR_TIGER_EYE_HIGHLIGHT,
    COLOR_TIGER_WHISKER, COLOR_TIGER_BLUSH, COLOR_STAR_YELLOW,
    COLOR_WHITE, COLOR_TIGER_STRIPE, COLOR_LIGHT_ORANGE, COLOR_DARK_STRIPE,
    SPRITE_SIZE, FRAME_COUNT_IDLE, FRAME_COUNT_WALKING, FRAME_COUNT_DRAGGING,
    FRAME_COUNT_FALLING, FRAME_COUNT_SLEEPING, FRAME_COUNT_EATING,
    FRAME_COUNT_WAVING, FRAME_COUNT_REMINDING
)
from states import PetState

class SpriteGenerator:
    """
    Generates sprite frames for all pet states using QPainter
    """
    
    def __init__(self):
        self.sprite_cache = {}  # Cache for generated sprites
        self.current_size = SPRITE_SIZE
    
    def generate_all_sprites(self):
        """Generate all sprite frames for all states"""
        print("Generating sprite frames...")
        
        # Generate frames for each state
        self.sprite_cache[PetState.IDLE] = self._generate_idle_frames()
        self.sprite_cache[PetState.WALKING] = self._generate_walking_frames()
        self.sprite_cache[PetState.DRAGGING] = self._generate_dragging_frames()
        self.sprite_cache[PetState.FALLING] = self._generate_falling_frames()
        self.sprite_cache[PetState.SLEEPING] = self._generate_sleeping_frames()
        self.sprite_cache[PetState.EATING] = self._generate_eating_frames()
        self.sprite_cache[PetState.WAVING] = self._generate_waving_frames()
        self.sprite_cache[PetState.REMINDING] = self._generate_reminding_frames()
        
        print("Sprite generation complete!")
        return self.sprite_cache
    
    def get_frames(self, state):
        """Get cached frames for a state"""
        return self.sprite_cache.get(state, [])
    
    def _create_base_pixmap(self):
        """Create a base transparent pixmap"""
        pixmap = QPixmap(self.current_size, self.current_size)
        pixmap.fill(Qt.transparent)
        return pixmap
    
    def _generate_idle_frames(self):
        """Generate idle animation frames (body bobbing, star blinking)"""
        frames = []
        for i in range(FRAME_COUNT_IDLE):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Calculate bob offset (2px up and down)
            bob_offset = 2 if i % 2 == 0 else -2
            
            # Draw character with bob offset
            self._draw_character(painter, bob_offset=bob_offset, star_visible=i % 3 != 0)
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _generate_walking_frames(self):
        """Generate walking animation frames (leg alternation, body sway)"""
        frames = []
        for i in range(FRAME_COUNT_WALKING):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Calculate leg phase and body sway (increased sway for more visible movement)
            leg_phase = i % 4
            sway_offset = 3 if leg_phase < 2 else -3  # Increased from 1 to 3
            
            # Draw character with walking pose
            self._draw_character(painter, sway_offset=sway_offset, walking_phase=leg_phase)
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _generate_dragging_frames(self):
        """Generate dragging animation frames (surprised expression)"""
        frames = []
        for i in range(FRAME_COUNT_DRAGGING):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw character with surprised expression
            self._draw_character(painter, surprised=True, limb_spread=0.3 + (i * 0.1))
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _generate_falling_frames(self):
        """Generate falling animation frames (limbs spread, surprised expression)"""
        frames = []
        for i in range(FRAME_COUNT_FALLING):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw character with limbs spread and surprised expression
            self._draw_character(painter, limb_spread=0.5 + (i * 0.1), surprised=True)
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _generate_sleeping_frames(self):
        """Generate sleeping animation frames (closed eyes, Zzz, gentle breathing)"""
        frames = []
        for i in range(FRAME_COUNT_SLEEPING):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Very gentle breathing effect (1px every few frames, not jumping)
            bob_offset = 0.5 if i % 3 == 0 else 0
            
            # Draw sleeping character with gentle breathing
            self._draw_character(painter, eyes_closed=True, bob_offset=bob_offset)
            
            # Draw Zzz effect (rising and fading) - after character so it's on top
            zzz_offset = i * 4
            self._draw_zzz(painter, zzz_offset)
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _generate_eating_frames(self):
        """Generate eating animation frames (mouth open/close, hearts)"""
        frames = []
        for i in range(FRAME_COUNT_EATING):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Calculate mouth openness
            mouth_open = i % 2 == 0
            
            # Draw character
            self._draw_character(painter, mouth_open=mouth_open)
            
            # Draw heart particles - floating upward above head
            if i % 2 == 0:
                scale = self.current_size / SPRITE_SIZE
                heart_x = self.current_size // 2
                heart_y = (self.current_size // 2) - 50 * scale + (i * 5)  # Above head, floating upward
                self._draw_heart(painter, heart_x, heart_y)
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _generate_waving_frames(self):
        """Generate waving animation frames (arm waving with rotation, happy eyes, stars)"""
        frames = []
        for i in range(FRAME_COUNT_WAVING):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Calculate arm wave angle (increased range for more visible waving)
            wave_angle = -30 + (i * 15) if i < 4 else -30 + ((7 - i) * 15)
            
            # Draw character with waving arm and happy eyes
            self._draw_character(painter, waving_arm=True, wave_angle=wave_angle, happy_eyes=True)
            
            # Draw stars on head (happy reaction)
            if i < 3:
                star_x = self.current_size // 2 + 15
                star_y = 30 - (i * 5)
                self._draw_star(painter, star_x, star_y, 4)
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _generate_reminding_frames(self):
        """Generate reminding animation frames (arms raised)"""
        frames = []
        for i in range(FRAME_COUNT_REMINDING):
            pixmap = self._create_base_pixmap()
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Calculate arm raise angle
            raise_angle = 10 + (i * 5) if i < 3 else 25 - ((i - 3) * 5)
            
            # Draw character with arms raised
            self._draw_character(painter, arms_raised=True, raise_angle=raise_angle, serious=True)
            
            painter.end()
            frames.append(pixmap)
        
        return frames
    
    def _draw_character(self, painter, bob_offset=0, sway_offset=0, star_visible=True,
                       surprised=False, limb_spread=0, eyes_closed=False, mouth_open=False,
                       walking_phase=0, waving_arm=False, wave_angle=0, arms_raised=False,
                       raise_angle=0, serious=False, happy_eyes=False):
        """
        Draw the cute tiger character with big head and small body
        
        Args:
            painter: QPainter instance
            bob_offset: Vertical bobbing offset
            sway_offset: Horizontal sway offset
            star_visible: Whether the star is visible
            surprised: Whether expression is surprised
            limb_spread: How much limbs are spread (0-1)
            eyes_closed: Whether eyes are closed
            mouth_open: Whether mouth is open
            walking_phase: Walking leg phase (0-3)
            waving_arm: Whether arm is waving
            wave_angle: Wave arm angle
            arms_raised: Whether arms are raised
            raise_angle: Arm raise angle
            serious: Whether expression is serious
        """
        center_x = self.current_size // 2 + sway_offset
        center_y = self.current_size // 2 + bob_offset
        scale = self.current_size / SPRITE_SIZE
        
        # Draw small body first
        self._draw_tiger_body(painter, center_x, center_y + 15 * scale, scale)
        
        # Draw big head
        self._draw_tiger_head(painter, center_x, center_y - 10 * scale, scale)
        
        # Draw cute face
        self._draw_tiger_face(painter, center_x, center_y - 8 * scale, scale, 
                             surprised, eyes_closed, mouth_open, serious)
        
        # Draw small arms (connected to body, not face)
        self._draw_tiger_arms(painter, center_x, center_y + 18 * scale, scale,
                             limb_spread, walking_phase, waving_arm, wave_angle, arms_raised, raise_angle)
        
        # Draw small legs
        self._draw_tiger_legs(painter, center_x, center_y + 25 * scale, scale,
                             limb_spread, walking_phase)
        
        # Draw star on head
        if star_visible:
            self._draw_star(painter, center_x + 18 * scale, center_y - 25 * scale, 4 * scale)
        
        # Draw cute tail with walking animation
        self._draw_tiger_tail(painter, center_x - 20 * scale, center_y + 20 * scale, scale, walking_phase)
    
    def _draw_tiger_body(self, painter, x, y, scale):
        """Draw the tiger body - pear shape (narrower top, wider bottom)"""
        body_color = QColor(COLOR_TIGER_ORANGE)
        painter.setBrush(QBrush(body_color))
        painter.setPen(Qt.NoPen)
        
        # Pear-shaped body using path
        body_path = QPainterPath()
        # Start from top center
        body_path.moveTo(x, y - 8 * scale)
        # Left side - curves outward then in
        body_path.quadTo(x - 20 * scale, y - 4 * scale, x - 18 * scale, y + 6 * scale)
        body_path.quadTo(x - 18 * scale, y + 14 * scale, x - 12 * scale, y + 18 * scale)
        # Bottom curve
        body_path.quadTo(x, y + 20 * scale, x + 12 * scale, y + 18 * scale)
        # Right side - curves inward then out
        body_path.quadTo(x + 18 * scale, y + 14 * scale, x + 18 * scale, y + 6 * scale)
        body_path.quadTo(x + 20 * scale, y - 4 * scale, x, y - 8 * scale)
        body_path.closeSubpath()
        painter.drawPath(body_path)
        
        # White belly patch (also pear-shaped)
        belly_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(belly_color))
        belly_path = QPainterPath()
        belly_path.moveTo(x, y - 4 * scale)
        belly_path.quadTo(x - 12 * scale, y, x - 10 * scale, y + 6 * scale)
        belly_path.quadTo(x - 10 * scale, y + 12 * scale, x - 6 * scale, y + 14 * scale)
        belly_path.quadTo(x, y + 16 * scale, x + 6 * scale, y + 14 * scale)
        belly_path.quadTo(x + 10 * scale, y + 12 * scale, x + 10 * scale, y + 6 * scale)
        belly_path.quadTo(x + 12 * scale, y, x, y - 4 * scale)
        belly_path.closeSubpath()
        painter.drawPath(belly_path)
        
        # Star on belly
        self._draw_star(painter, x, y + 6 * scale, 3 * scale)
        
        # Body stripes on sides - thinner and more rounded
        stripe_color = QColor(COLOR_TIGER_STRIPE)
        painter.setBrush(QBrush(stripe_color))
        painter.setPen(Qt.NoPen)
        
        # Left side stripes - 3 horizontal stripes (thinner)
        left_stripe1 = QRectF(x - 18 * scale, y + 0 * scale, 3 * scale, 2 * scale)
        painter.drawEllipse(left_stripe1)
        left_stripe2 = QRectF(x - 19 * scale, y + 6 * scale, 3 * scale, 2 * scale)
        painter.drawEllipse(left_stripe2)
        left_stripe3 = QRectF(x - 18 * scale, y + 12 * scale, 3 * scale, 2 * scale)
        painter.drawEllipse(left_stripe3)
        
        # Right side stripes - 3 horizontal stripes (thinner)
        right_stripe1 = QRectF(x + 13 * scale, y + 0 * scale, 3 * scale, 2 * scale)
        painter.drawEllipse(right_stripe1)
        right_stripe2 = QRectF(x + 14 * scale, y + 6 * scale, 3 * scale, 2 * scale)
        painter.drawEllipse(right_stripe2)
        right_stripe3 = QRectF(x + 13 * scale, y + 12 * scale, 3 * scale, 2 * scale)
        painter.drawEllipse(right_stripe3)
    
    def _draw_tiger_head(self, painter, x, y, scale):
        """Draw the big cute tiger head - more tiger-like"""
        # Main head (round and cute)
        head_color = QColor(COLOR_TIGER_ORANGE)
        painter.setBrush(QBrush(head_color))
        painter.setPen(Qt.NoPen)
        
        # Round head (cute shape)
        head_rect = QRectF(x - 32 * scale, y - 32 * scale, 64 * scale, 60 * scale)
        painter.drawEllipse(head_rect)
        
        # White cheek pads (puffy cheeks - key tiger feature)
        face_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(face_color))
        # Left cheek - puffy
        left_cheek = QRectF(x - 30 * scale, y + 2 * scale, 16 * scale, 18 * scale)
        painter.drawEllipse(left_cheek)
        # Right cheek - puffy
        right_cheek = QRectF(x + 14 * scale, y + 2 * scale, 16 * scale, 18 * scale)
        painter.drawEllipse(right_cheek)
        # Chin
        chin_rect = QRectF(x - 10 * scale, y + 16 * scale, 20 * scale, 12 * scale)
        painter.drawEllipse(chin_rect)
        
        # Draw "王" character on forehead - thicker and darker
        self._draw_wang_character(painter, x, y - 24 * scale, scale)
        
        # Tiger ears - larger, wider, flatter, more separated
        ear_color = QColor(COLOR_TIGER_ORANGE)
        painter.setBrush(QBrush(ear_color))
        painter.setPen(Qt.NoPen)
        
        # Left ear - round
        left_ear_rect = QRectF(x - 36 * scale, y - 36 * scale, 18 * scale, 18 * scale)
        painter.drawEllipse(left_ear_rect)
        
        # Right ear - round
        right_ear_rect = QRectF(x + 18 * scale, y - 36 * scale, 18 * scale, 18 * scale)
        painter.drawEllipse(right_ear_rect)
        
        # Ear inner - white (not pink)
        ear_inner_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(ear_inner_color))
        
        left_ear_inner = QRectF(x - 32 * scale, y - 32 * scale, 10 * scale, 10 * scale)
        painter.drawEllipse(left_ear_inner)
        
        right_ear_inner = QRectF(x + 22 * scale, y - 32 * scale, 10 * scale, 10 * scale)
        painter.drawEllipse(right_ear_inner)
        
        # Ear back patch - dark brown circle inside ear edge
        ear_back_color = QColor(COLOR_TIGER_STRIPE)
        painter.setBrush(QBrush(ear_back_color))
        
        left_ear_back = QRectF(x - 35 * scale, y - 34 * scale, 4 * scale, 4 * scale)
        painter.drawEllipse(left_ear_back)
        
        right_ear_back = QRectF(x + 30 * scale, y - 34 * scale, 4 * scale, 4 * scale)
        painter.drawEllipse(right_ear_back)
    
    def _draw_wang_character(self, painter, x, y, scale):
        """Draw the 王 character on tiger's forehead - cute style with rounded caps"""
        wang_color = QColor(COLOR_TIGER_STRIPE)  # Back to brown, not black
        # Thicker pen with rounded caps for cuteness
        painter.setPen(QPen(wang_color, 2.5 * scale, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        
        # Draw 王 character - smaller, more spacing between strokes
        # Top horizontal (long)
        painter.drawLine(int(x - 8 * scale), int(y), int(x + 8 * scale), int(y))
        # Middle horizontal (short)
        painter.drawLine(int(x - 3.5 * scale), int(y + 4 * scale), int(x + 3.5 * scale), int(y + 4 * scale))
        # Bottom horizontal (long)
        painter.drawLine(int(x - 8 * scale), int(y + 8 * scale), int(x + 8 * scale), int(y + 8 * scale))
        # Vertical line (centered, connects all three)
        painter.drawLine(int(x), int(y), int(x), int(y + 8 * scale))
        
        painter.setPen(Qt.NoPen)
    
    def _draw_tiger_face(self, painter, x, y, scale, surprised, eyes_closed, mouth_open, serious, happy_eyes=False):
        """Draw the cute tiger face with animal-like features"""
        # Draw big cute animal eyes
        eye_color = QColor(COLOR_TIGER_EYE)
        eye_highlight = QColor(COLOR_TIGER_EYE_HIGHLIGHT)
        
        if happy_eyes:
            # Happy eyes (^^) - curved upward
            painter.setPen(QPen(eye_color, 2.5 * scale))
            painter.setBrush(Qt.NoBrush)
            # Left eye (happy curve)
            painter.drawArc(QRectF(x - 14 * scale, y - 4 * scale, 12 * scale, 8 * scale), 180 * 16, 360 * 16)
            # Right eye (happy curve)
            painter.drawArc(QRectF(x + 2 * scale, y - 4 * scale, 12 * scale, 8 * scale), 180 * 16, 360 * 16)
            painter.setPen(Qt.NoPen)
        elif eyes_closed:
            # Closed eyes (downward curved lines ⌒ ⌒)
            painter.setPen(QPen(eye_color, 2.5 * scale, Qt.SolidLine, Qt.RoundCap))
            painter.setBrush(Qt.NoBrush)
            # Left eye (downward curve)
            painter.drawArc(QRectF(x - 14 * scale, y - 4 * scale, 12 * scale, 8 * scale), 180 * 16, 180 * 16)
            # Right eye (downward curve)
            painter.drawArc(QRectF(x + 2 * scale, y - 4 * scale, 12 * scale, 8 * scale), 180 * 16, 180 * 16)
            painter.setPen(Qt.NoPen)
        else:
            # Big round animal eyes (larger for cuteness)
            if surprised:
                eye_width = 16 * scale
                eye_height = 18 * scale
            else:
                eye_width = 14 * scale
                eye_height = 16 * scale
            
            # Left eye
            painter.setBrush(QBrush(eye_color))
            left_eye_rect = QRectF(x - 16 * scale, y - 9 * scale, eye_width, eye_height)
            painter.drawEllipse(left_eye_rect)
            
            # Right eye
            right_eye_rect = QRectF(x + 2 * scale, y - 9 * scale, eye_width, eye_height)
            painter.drawEllipse(right_eye_rect)
            
            # Big white highlights (making eyes cute and shiny)
            painter.setBrush(QBrush(eye_highlight))
            # Main highlight
            left_highlight = QRectF(x - 13 * scale, y - 6 * scale, 5 * scale, 5 * scale)
            painter.drawEllipse(left_highlight)
            right_highlight = QRectF(x + 5 * scale, y - 6 * scale, 5 * scale, 5 * scale)
            painter.drawEllipse(right_highlight)
            
            # Small secondary highlights
            small_highlight = QRectF(x - 9 * scale, y - 2 * scale, 2.5 * scale, 2.5 * scale)
            painter.drawEllipse(small_highlight)
            small_highlight2 = QRectF(x + 9 * scale, y - 2 * scale, 2.5 * scale, 2.5 * scale)
            painter.drawEllipse(small_highlight2)
        
        # Draw cute round pink nose (small and cute)
        nose_color = QColor(COLOR_TIGER_NOSE)
        painter.setBrush(QBrush(nose_color))
        painter.setPen(Qt.NoPen)
        # Small round/oval nose
        nose_rect = QRectF(x - 3 * scale, y + 4 * scale, 6 * scale, 5 * scale)
        painter.drawEllipse(nose_rect)
        
        # Draw cute ω-shaped mouth (cute smile)
        mouth_color = QColor(COLOR_TIGER_STRIPE)
        painter.setPen(QPen(mouth_color, 2 * scale, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        
        if surprised:
            # O-shaped mouth
            painter.setBrush(QBrush(mouth_color))
            mouth_rect = QRectF(x - 3 * scale, y + 10 * scale, 6 * scale, 6 * scale)
            painter.drawEllipse(mouth_rect)
            painter.setBrush(Qt.NoBrush)
        elif mouth_open:
            # Open happy mouth (ω shape)
            mouth_path = QPainterPath()
            mouth_path.moveTo(x - 4 * scale, y + 9 * scale)
            mouth_path.quadTo(x - 4 * scale, y + 13 * scale, x, y + 11 * scale)
            mouth_path.quadTo(x + 4 * scale, y + 13 * scale, x + 4 * scale, y + 9 * scale)
            painter.drawPath(mouth_path)
        else:
            # Cute ω smile (animal-style)
            mouth_path = QPainterPath()
            mouth_path.moveTo(x - 5 * scale, y + 9 * scale)
            mouth_path.quadTo(x - 5 * scale, y + 12 * scale, x, y + 10 * scale)
            mouth_path.quadTo(x + 5 * scale, y + 12 * scale, x + 5 * scale, y + 9 * scale)
            painter.drawPath(mouth_path)
        
        painter.setPen(Qt.NoPen)
        
        # Draw cute pink blush
        blush_color = QColor(COLOR_TIGER_BLUSH)
        painter.setBrush(QBrush(blush_color))
        painter.setPen(Qt.NoPen)
        
        left_blush_rect = QRectF(x - 22 * scale, y + 2 * scale, 10 * scale, 6 * scale)
        painter.drawEllipse(left_blush_rect)
        right_blush_rect = QRectF(x + 12 * scale, y + 2 * scale, 10 * scale, 6 * scale)
        painter.drawEllipse(right_blush_rect)
        
        # Draw whiskers (animal feature)
        whisker_color = QColor(COLOR_TIGER_WHISKER)
        painter.setPen(QPen(whisker_color, 1.5 * scale))
        painter.setBrush(Qt.NoBrush)
        
        # Left whiskers
        painter.drawLine(int(x - 18 * scale), int(y + 6 * scale), int(x - 28 * scale), int(y + 4 * scale))
        painter.drawLine(int(x - 18 * scale), int(y + 8 * scale), int(x - 30 * scale), int(y + 8 * scale))
        painter.drawLine(int(x - 18 * scale), int(y + 10 * scale), int(x - 28 * scale), int(y + 12 * scale))
        
        # Right whiskers
        painter.drawLine(int(x + 18 * scale), int(y + 6 * scale), int(x + 28 * scale), int(y + 4 * scale))
        painter.drawLine(int(x + 18 * scale), int(y + 8 * scale), int(x + 30 * scale), int(y + 8 * scale))
        painter.drawLine(int(x + 18 * scale), int(y + 10 * scale), int(x + 28 * scale), int(y + 12 * scale))
        painter.setPen(Qt.NoPen)
    
    def _draw_tiger_arms(self, painter, x, y, scale, limb_spread, walking_phase,
                         waving_arm, wave_angle, arms_raised, raise_angle):
        """Draw the small cute arms as ellipses (old cute style)"""
        arm_color = QColor(COLOR_TIGER_ORANGE)
        painter.setBrush(QBrush(arm_color))
        painter.setPen(Qt.NoPen)
        
        # Calculate arm positions based on state
        if arms_raised:
            left_arm_y = y - 10 * scale
            right_arm_y = y - 10 * scale
        elif waving_arm:
            left_arm_y = y
            right_arm_y = y - 5 * scale
        elif limb_spread > 0:
            left_arm_y = y - 8 * scale * limb_spread
            right_arm_y = y - 8 * scale * limb_spread
        else:
            left_arm_y = y
            right_arm_y = y
        
        # Left arm (small ellipse - cute style)
        left_arm_rect = QRectF(x - 22 * scale, left_arm_y - 2 * scale, 10 * scale, 6 * scale)
        painter.drawEllipse(left_arm_rect)
        
        # Right arm (small ellipse - cute style)
        right_arm_rect = QRectF(x + 12 * scale, right_arm_y - 2 * scale, 10 * scale, 6 * scale)
        painter.drawEllipse(right_arm_rect)
        
        # White paw pads
        pad_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(pad_color))
        
        # Left paw pad
        left_pad_rect = QRectF(x - 20 * scale, left_arm_y, 4 * scale, 3 * scale)
        painter.drawEllipse(left_pad_rect)
        
        # Right paw pad
        right_pad_rect = QRectF(x + 18 * scale, right_arm_y, 4 * scale, 3 * scale)
        painter.drawEllipse(right_pad_rect)
    
    def _draw_arms(self, painter, x, y, scale, limb_spread, walking_phase,
                  waving_arm, wave_angle, arms_raised, raise_angle):
        """Draw the arms"""
        arm_color = QColor(COLOR_TIGER_ORANGE)
        painter.setBrush(QBrush(arm_color))
        painter.setPen(Qt.NoPen)
        
        # Calculate arm positions based on state
        if arms_raised:
            # Arms raised overhead
            left_arm_angle = -raise_angle
            right_arm_angle = raise_angle
            left_arm_y = y - 15 * scale
            right_arm_y = y - 15 * scale
        elif waving_arm:
            # One arm waving
            left_arm_angle = 0
            right_arm_angle = wave_angle
            left_arm_y = y
            right_arm_y = y - 5 * scale
        elif limb_spread > 0:
            # Arms spread
            left_arm_angle = -30 * limb_spread
            right_arm_angle = 30 * limb_spread
            left_arm_y = y - 10 * scale * limb_spread
            right_arm_y = y - 10 * scale * limb_spread
        else:
            # Normal arms
            left_arm_angle = -15 + (walking_phase * 5)
            right_arm_angle = 15 - (walking_phase * 5)
            left_arm_y = y
            right_arm_y = y
        
        # Left arm
        left_arm_rect = QRectF(x - 30 * scale, left_arm_y - 3 * scale, 12 * scale, 8 * scale)
        painter.drawEllipse(left_arm_rect)
        
        # Right arm
        right_arm_rect = QRectF(x + 18 * scale, right_arm_y - 3 * scale, 12 * scale, 8 * scale)
        painter.drawEllipse(right_arm_rect)
        
        # Draw paw pads
        pad_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(pad_color))
        
        # Left paw pad
        left_pad_rect = QRectF(x - 28 * scale, left_arm_y - 1 * scale, 4 * scale, 3 * scale)
        painter.drawEllipse(left_pad_rect)
        
        # Right paw pad
        right_pad_rect = QRectF(x + 26 * scale, right_arm_y - 1 * scale, 4 * scale, 3 * scale)
        painter.drawEllipse(right_pad_rect)
    
    def _draw_tiger_legs(self, painter, x, y, scale, limb_spread, walking_phase):
        """Draw the tiger legs as rounded rectangles with walking animation"""
        leg_color = QColor(COLOR_TIGER_ORANGE)
        painter.setBrush(QBrush(leg_color))
        painter.setPen(Qt.NoPen)
        
        # Calculate leg positions
        if limb_spread > 0:
            spread = 10 * scale * limb_spread
            left_leg_x = x - spread
            right_leg_x = x + spread
            left_leg_y = y
            right_leg_y = y
        else:
            # Walking animation with more pronounced movement
            left_leg_x = x - 14 * scale
            right_leg_x = x + 6 * scale
            
            if walking_phase == 0:
                left_leg_y = y
                right_leg_y = y - 4 * scale
            elif walking_phase == 1:
                left_leg_y = y - 4 * scale
                right_leg_y = y
            elif walking_phase == 2:
                left_leg_y = y
                right_leg_y = y + 4 * scale
            else:
                left_leg_y = y + 4 * scale
                right_leg_y = y
        
        # Left leg (rounded rectangle)
        painter.save()
        painter.translate(left_leg_x, left_leg_y)
        # Slight rotation for walking
        if walking_phase > 0:
            rotation = (walking_phase - 1.5) * 8
            painter.rotate(rotation)
        left_leg_rect = QRectF(-6 * scale, 0, 12 * scale, 10 * scale)
        painter.drawRoundedRect(left_leg_rect, 4 * scale, 4 * scale)
        # White paw pad
        pad_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(pad_color))
        pad_rect = QRectF(-3 * scale, 6 * scale, 5 * scale, 3 * scale)
        painter.drawRoundedRect(pad_rect, 2 * scale, 2 * scale)
        painter.restore()
        
        # Right leg (rounded rectangle)
        painter.save()
        painter.translate(right_leg_x, right_leg_y)
        # Slight rotation for walking
        if walking_phase > 0:
            rotation = -(walking_phase - 1.5) * 8
            painter.rotate(rotation)
        right_leg_rect = QRectF(-6 * scale, 0, 12 * scale, 10 * scale)
        painter.drawRoundedRect(right_leg_rect, 4 * scale, 4 * scale)
        # White paw pad
        pad_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(pad_color))
        pad_rect = QRectF(-3 * scale, 6 * scale, 5 * scale, 3 * scale)
        painter.drawRoundedRect(pad_rect, 2 * scale, 2 * scale)
        painter.restore()
    
    def _draw_tiger_tail(self, painter, x, y, scale, walking_phase=0):
        """Draw a longer tiger tail with black rings and walking animation"""
        tail_color = QColor(COLOR_TIGER_ORANGE)
        painter.setBrush(QBrush(tail_color))
        painter.setPen(Qt.NoPen)
        
        # Calculate tail sway based on walking phase
        if walking_phase > 0:
            sway_offset = (walking_phase - 1.5) * 4 * scale
        else:
            # Idle state - slight gentle sway
            sway_offset = 0
        
        # Tail base
        tail_base = QRectF(x - 8 * scale, y - 3 * scale, 12 * scale, 6 * scale)
        painter.drawEllipse(tail_base)
        
        # Tail body (longer, curved with sway)
        painter.save()
        painter.translate(x, y)
        if sway_offset != 0:
            painter.rotate(sway_offset)
        
        tail_path = QPainterPath()
        tail_path.moveTo(0, 0)
        tail_path.quadTo(-15 * scale, -5 * scale, -18 * scale, -12 * scale)
        tail_path.quadTo(-12 * scale, -18 * scale, -8 * scale, -15 * scale)
        tail_path.quadTo(-5 * scale, -10 * scale, -2 * scale, -8 * scale)
        painter.drawPath(tail_path)
        
        # Tail tip (white)
        tip_color = QColor(COLOR_TIGER_WHITE)
        painter.setBrush(QBrush(tip_color))
        tail_tip = QRectF(-10 * scale, -18 * scale, 6 * scale, 6 * scale)
        painter.drawEllipse(tail_tip)
        
        # Simple rings on tail (2 rings, not too many)
        ring_color = QColor(COLOR_TIGER_STRIPE)
        painter.setBrush(QBrush(ring_color))
        painter.setPen(Qt.NoPen)
        
        # Ring 1
        tail_ring1 = QRectF(-12 * scale, -10 * scale, 3 * scale, 3 * scale)
        painter.drawEllipse(tail_ring1)
        # Ring 2
        tail_ring2 = QRectF(-10 * scale, -16 * scale, 3 * scale, 3 * scale)
        painter.drawEllipse(tail_ring2)
        
        painter.restore()
    
    def _draw_star(self, painter, x, y, size):
        """Draw a star shape"""
        path = QPainterPath()
        points = 5
        angle = -90  # Start from top
        
        for i in range(points * 2):
            radius = size if i % 2 == 0 else size / 2
            angle_deg = angle + (i * 180 / points)
            angle_rad = angle_deg * 3.14159 / 180
            
            px = x + radius * (angle_rad if i == 0 else 1)  # Simplified
            py = y + radius * (1 if i == 0 else 0)  # Simplified
            
            if i == 0:
                path.moveTo(px, py)
            else:
                # Calculate actual star points
                star_x = x + radius * (1 if i % 2 == 0 else 0.5) * (1 if i % 4 < 2 else -1)
                star_y = y + radius * (0 if i % 2 == 0 else 0.866) * (-1 if (i // 2) % 2 == 0 else 1)
                path.lineTo(star_x, star_y)
        
        # Simplified star drawing
        path = QPainterPath()
        star_points = [
            (x, y - size),           # Top
            (x + size * 0.3, y - size * 0.3),  # Upper right
            (x + size, y - size * 0.3),        # Right
            (x + size * 0.4, y + size * 0.2),  # Lower right
            (x + size * 0.5, y + size),        # Bottom
            (x, y + size * 0.5),               # Bottom center
            (x - size * 0.5, y + size),        # Bottom left
            (x - size * 0.4, y + size * 0.2),  # Lower left
            (x - size, y - size * 0.3),        # Left
            (x - size * 0.3, y - size * 0.3),  # Upper left
        ]
        
        path.moveTo(star_points[0][0], star_points[0][1])
        for point in star_points[1:]:
            path.lineTo(point[0], point[1])
        path.closeSubpath()
        
        painter.drawPath(path)
    
    def _draw_zzz(self, painter, offset):
        """Draw Zzz sleep effect - positioned above head, different sizes"""
        z_color = QColor(COLOR_TIGER_STRIPE)
        painter.setPen(QPen(z_color, 2))
        
        scale = self.current_size / SPRITE_SIZE
        center_x = self.current_size // 2
        center_y = self.current_size // 2
        
        # Position Zzz to the right and above the head
        base_x = center_x + 35 * scale
        base_y = center_y - 40 * scale - offset
        
        # Draw three Z's with decreasing sizes
        # First Z (largest)
        painter.setFont(QFont("Arial", int(16 * scale)))
        painter.drawText(int(base_x), int(base_y), "Z")
        
        # Second z (medium)
        painter.setFont(QFont("Arial", int(12 * scale)))
        painter.drawText(int(base_x + 10 * scale), int(base_y - 8 * scale), "z")
        
        # Third z (smallest)
        painter.setFont(QFont("Arial", int(9 * scale)))
        painter.drawText(int(base_x + 18 * scale), int(base_y - 15 * scale), "z")
    
    def _draw_heart(self, painter, x, y):
        """Draw a small heart"""
        heart_color = QColor(COLOR_TIGER_EAR_INNER)
        painter.setBrush(QBrush(heart_color))
        painter.setPen(Qt.NoPen)
        
        # Simple heart shape
        path = QPainterPath()
        path.moveTo(x, y + 5)
        path.cubicTo(x - 5, y, x - 5, y - 5, x, y - 5)
        path.cubicTo(x + 5, y - 5, x + 5, y, x, y + 5)
        painter.drawPath(path)