"""
ai_verification.py — Production-Grade OMR Bubble Classifier
============================================================
Architecture:
BubbleNormalizer → ResNet-style CNN → 5-class Softmax + Confidence Score

Classes:
0: empty        — فارغة (حلقة مطبوعة فقط)
1: filled       — مظللة كاملة
2: half_filled  — نصف تظليل / متردد
3: erased       — ممسوحة بالممحاة
4: crossed      — مشطوبة بـ X

Key Feature — Confidence Calibration:
Every prediction returns a confidence score.
If confidence < REVIEW_THRESHOLD, the bubble is flagged for human review.
"""

import os
import logging
import threading
import numpy as np
import cv2
from typing import Dict, List, Optional, Tuple, Any

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from .bubble_normalizer import BubbleNormalizer

logger = logging.getLogger("omr.ai")

# ─── Configuration ────────────────────────────────────────────────────────────
INPUT_SIZE       = 48          # pixels — must match BubbleNormalizer.output_size
NUM_CLASSES      = 5
CLASS_NAMES      = ["empty", "filled", "half_filled", "erased", "crossed"]
REVIEW_THRESHOLD = 0.75        # confidence below this → flag for human review
MODEL_PATH       = os.path.join(os.path.dirname(__file__), "omr_bubble_cnn_v2.pt")

TRAIN_SAMPLES_PER_CLASS = 2000   # 10,000 total
TRAIN_EPOCHS             = 25
BATCH_SIZE               = 64
LEARNING_RATE            = 1e-3


# ─── Model ────────────────────────────────────────────────────────────────────

class ResidualBlock(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(channels, channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(channels),
        )
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(x + self.block(x))


class BubbleClassifierCNN(nn.Module):
    """
    ResNet-style CNN for 5-class OMR bubble classification.
    Input:  (B, 1, 48, 48)  float32  [0, 1]
    Output: (B, 5)          logits
    """

    def __init__(self, num_classes: int = NUM_CLASSES):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1: 48→24
            nn.Conv2d(1, 32, 3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            # Block 2: 24→12
            nn.Conv2d(32, 64, 3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            # Block 3: 12→6
            nn.Conv2d(64, 128, 3, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            # Residual block (maintains 6×6×128)
            ResidualBlock(128),
        )
        # Global average pooling → 128-d vector
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.gap(x)
        return self.classifier(x)


# ─── Realistic Training Data Generator ────────────────────────────────────────

REAL_EMPTY_CROPS_PATH = os.path.join(os.path.dirname(__file__), "real_empty_crops.npy")


class RealisticBubbleDataGenerator:
    """
    Hybrid data generator for OMR bubble classification.

    STRATEGY:
    - 'empty' class: uses REAL crops extracted from the actual blank OMR sheet
    (zero domain gap — the model sees exactly what a real scanner produces)
    - Other classes: draws marks ON TOP of real empty crops, then applies
    scanner degradation artifacts.

    This approach eliminates the synthetic-to-real domain gap.
    """

    SIZE = INPUT_SIZE   # 48 × 48

    def __init__(self):
        # Load real empty crops if available
        if os.path.exists(REAL_EMPTY_CROPS_PATH):
            self._real_empty = np.load(REAL_EMPTY_CROPS_PATH)
            print(f"[AI] Loaded {len(self._real_empty)} real empty bubble crops for training")
        else:
            self._real_empty = None
            print("[AI] No real empty crops found — using synthetic data only")

    def _get_real_base(self) -> np.ndarray:
        """Return a real empty crop as the base (or synthetic if unavailable)."""
        if self._real_empty is not None and len(self._real_empty) > 0:
            idx = np.random.randint(0, len(self._real_empty))
            return self._real_empty[idx].copy()
        return self._make_base_bubble()

    # ── class generators ─────────────────────────────────────────────────────

    def _make_base_bubble(self) -> np.ndarray:
        """
        White background with a printed circle ring (the template).
        Real OMR sheets have a THICK printed ring — measuring ~18-20% dark pixels
        in a 38×38 crop. We model that accurately here.
        """
        img = np.ones((self.SIZE, self.SIZE), dtype=np.float32)
        cx, cy = self.SIZE // 2, self.SIZE // 2
        r = self.SIZE // 2 - 4
        # Real printer ring: 3-5px thick, with anti-aliasing blur
        thickness = np.random.randint(3, 6)
        cv2.circle(img, (cx, cy), r, 0.0, thickness)
        # Slight blur to simulate print quality
        img = cv2.GaussianBlur(img, (3, 3), 0.5)
        return img

    def _gen_empty(self) -> np.ndarray:
        """
        Empty bubble — uses REAL crop from the actual OMR sheet.
        Just adds augmentation to increase variety.
        """
        img = self._get_real_base()   # <-- Real scan data!
        # Mild augmentation: brightness/contrast shift
        scale = np.random.uniform(0.9, 1.1)
        shift = np.random.uniform(-0.03, 0.03)
        img = img * scale + shift
        # Scanner noise
        noise_sigma = np.random.uniform(0.005, 0.03)
        img += np.random.normal(0, noise_sigma, img.shape).astype(np.float32)
        return np.clip(img, 0, 1)

    def _gen_filled(self) -> np.ndarray:
        """Filled bubble — dark pencil/pen fill ON TOP of a real empty crop."""
        img = self._get_real_base()   # <-- Real scan base
        cx, cy = self.SIZE // 2, self.SIZE // 2
        r = self.SIZE // 2 - 5
        # Darkness varies: 0.0 (black/2B pencil) to 0.30 (light HB)
        darkness  = np.random.uniform(0.0, 0.25)
        fill_radius = int(r * np.random.uniform(0.75, 0.95))
        cv2.circle(img, (cx, cy), fill_radius, darkness, -1)
        # Add pencil/pen texture
        noise = np.random.normal(0, np.random.uniform(0.02, 0.08), img.shape)
        img += noise.astype(np.float32)
        return np.clip(img, 0, 1)

    def _gen_half_filled(self) -> np.ndarray:
        """Half/partial fill ON TOP of a real empty crop."""
        img = self._get_real_base()   # <-- Real scan base
        cx, cy = self.SIZE // 2, self.SIZE // 2
        r = self.SIZE // 2 - 5
        style = np.random.randint(0, 3)
        if style == 0:
            rect = np.zeros_like(img)
            cv2.ellipse(rect, (cx, cy), (r, r), 0, 180, 360, 1, -1)
            darkness = np.random.uniform(0.05, 0.3)
            img = np.where(rect > 0, darkness, img)
        elif style == 1:
            rect = np.zeros_like(img)
            cv2.ellipse(rect, (cx, cy), (r, r), 0, 90, 270, 1, -1)
            darkness = np.random.uniform(0.05, 0.3)
            img = np.where(rect > 0, darkness, img)
        else:
            fill_radius = int(r * np.random.uniform(0.45, 0.70))
            cv2.circle(img, (cx, cy), fill_radius, np.random.uniform(0.05, 0.35), -1)
        noise = np.random.normal(0, 0.04, img.shape)
        return np.clip(img + noise, 0, 1)

    def _gen_erased(self) -> np.ndarray:
        """
        Erased bubble: light gray smudge residue on a real empty base.
        Real stats: mean≈0.78, dark%≈12%, std≈0.21
        
        Real erased = pencil filled → eraser applied → faint gray smudge remains.
        Result: slightly darker than empty (0.845) but FEWER very-dark pixels
        because the gray is uniform (no sharp ring contrast).
        """
        img = self._get_real_base()  # Start from real empty
        cx, cy = self.SIZE // 2, self.SIZE // 2
        r = self.SIZE // 2 - 5

        # Apply light gray smudge fill over interior (residue after erasing)
        smudge_val = np.random.uniform(0.68, 0.82)   # lighter than empty mean
        mask = np.zeros_like(img)
        fill_r = int(r * np.random.uniform(0.75, 0.95))
        cv2.circle(mask, (cx, cy), fill_r, 1.0, -1)
        img = np.where(mask > 0, smudge_val, img)

        # Eraser direction streaks (slightly lighter/white bands)
        n_strokes = np.random.randint(2, 6)
        for _ in range(n_strokes):
            y_s = int(cy + np.random.uniform(-r * 0.9, r * 0.9))
            sw  = np.random.randint(1, 4)
            angle = np.random.uniform(-20, 20)
            dx = int(r * np.cos(np.radians(angle)))
            dy = int(r * np.sin(np.radians(angle)))
            bright = np.random.uniform(0.85, 1.0)
            cv2.line(img, (cx - dx, y_s - dy), (cx + dx, y_s + dy), bright, sw)

        # Slight texture noise (pencil grain residue)
        img += np.random.normal(0, 0.025, img.shape).astype(np.float32)
        return np.clip(img, 0, 1)

    def _gen_crossed(self) -> np.ndarray:
        """
        Crossed bubble: ALWAYS filled first then X marks drawn on top.
        Real stats: mean≈0.36, dark%≈79%, std≈0.28
        
        Real crossed = student fills completely → then draws X to cancel.
        Result: darker than filled (0.44, 73%) because X adds more dark ink.
        """
        img = self._gen_filled()   # ALWAYS start from a filled bubble
        cx, cy = self.SIZE // 2, self.SIZE // 2
        r = int((self.SIZE // 2 - 5) * 0.90)  # Slightly larger reach

        # Heavy X strokes — thick, very dark ink (pen, not pencil)
        thickness = np.random.randint(2, 4)
        color     = np.random.uniform(0.0, 0.10)   # near-black (pen stroke)
        offset_x  = np.random.randint(-2, 3)
        offset_y  = np.random.randint(-2, 3)
        cv2.line(img,
                (cx - r + offset_x, cy - r + offset_y),
                (cx + r + offset_x, cy + r + offset_y),
                color, thickness)
        cv2.line(img,
                (cx + r + offset_x, cy - r + offset_y),
                (cx - r + offset_x, cy + r + offset_y),
                color, thickness)
        # Sometimes a second pass (student pressing hard)
        if np.random.random() < 0.4:
            cv2.line(img, (cx-r, cy-r+2), (cx+r, cy+r+2), color, max(1, thickness-1))
            cv2.line(img, (cx+r, cy-r+2), (cx-r, cy+r+2), color, max(1, thickness-1))

        noise = np.random.normal(0, 0.03, img.shape)
        return np.clip(img + noise, 0, 1)

    # ── scanner/camera degradation ────────────────────────────────────────────

    @staticmethod
    def _apply_scanner_artifacts(img: np.ndarray) -> np.ndarray:
        """Apply real-world scanning degradation effects."""

        # 1. Gaussian noise (sensor noise)
        if np.random.random() < 0.7:
            sigma = np.random.uniform(0.01, 0.06)
            img = img + np.random.normal(0, sigma, img.shape).astype(np.float32)

        # 2. Gaussian blur (scanner focus / phone shake)
        if np.random.random() < 0.5:
            k = np.random.choice([3, 5])
            s = np.random.uniform(0.5, 1.5)
            img_u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
            img_u8 = cv2.GaussianBlur(img_u8, (k, k), s)
            img = img_u8.astype(np.float32) / 255.0

        # 3. Brightness shift (uneven illumination)
        if np.random.random() < 0.6:
            shift = np.random.uniform(-0.12, 0.12)
            img = img + shift

        # 4. JPEG compression artifacts
        if np.random.random() < 0.4:
            quality = np.random.randint(50, 90)
            img_u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
            _, buf = cv2.imencode('.jpg', img_u8, [cv2.IMWRITE_JPEG_QUALITY, quality])
            img = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0

        # 5. Slight rotation
        if np.random.random() < 0.5:
            angle = np.random.uniform(-15, 15)
            M = cv2.getRotationMatrix2D(
                (INPUT_SIZE // 2, INPUT_SIZE // 2), angle, 1.0)
            img_u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
            img_u8 = cv2.warpAffine(img_u8, M, (INPUT_SIZE, INPUT_SIZE),
                                    borderValue=255)
            img = img_u8.astype(np.float32) / 255.0

        # 6. Perspective distortion (phone photos)
        if np.random.random() < 0.3:
            s = INPUT_SIZE
            dx = np.random.randint(0, 4)
            dy = np.random.randint(0, 4)
            src = np.float32([[0, 0], [s, 0], [s, s], [0, s]])
            dst = np.float32([[dx, dy], [s - dx, dy],
                            [s - dx, s - dy], [dx, s - dy]])
            M = cv2.getPerspectiveTransform(src, dst)
            img_u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
            img_u8 = cv2.warpPerspective(img_u8, M, (s, s), borderValue=255)
            img = img_u8.astype(np.float32) / 255.0

        return np.clip(img, 0, 1)

    # ── public API ────────────────────────────────────────────────────────────

    _GENERATORS = [
        '_gen_empty', '_gen_filled', '_gen_half_filled',
        '_gen_erased', '_gen_crossed',
    ]

    def generate_dataset(
        self,
        n_per_class: int = TRAIN_SAMPLES_PER_CLASS,
        apply_artifacts: bool = True,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns X: (N, 1, 48, 48) float32, y: (N,) int64

        CRITICAL: Each generated image is passed through BubbleNormalizer
        (CLAHE + circle centering + resize) — the SAME pipeline used during
        inference. This eliminates the training/inference preprocessing mismatch.
        """
        from .bubble_normalizer import BubbleNormalizer
        normalizer = BubbleNormalizer()

        X_list, y_list = [], []
        for class_idx, gen_name in enumerate(self._GENERATORS):
            gen_fn = getattr(self, gen_name)
            logger.info(f"  Generating {n_per_class} samples for class: {CLASS_NAMES[class_idx]}")
            for _ in range(n_per_class):
                img = gen_fn()
                if apply_artifacts:
                    img = self._apply_scanner_artifacts(img)
                # Convert to uint8 (same format as real camera/scanner input)
                img_u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
                # Apply EXACT same preprocessing as inference (CLAHE + centering + resize)
                normalized = normalizer.normalize(img_u8)
                X_list.append(normalized)
                y_list.append(class_idx)

        X = np.array(X_list, dtype=np.float32)[:, np.newaxis, :, :]  # (N,1,H,W)
        y = np.array(y_list, dtype=np.int64)

        # Shuffle
        perm = np.random.permutation(len(y))
        return X[perm], y[perm]


# ─── Trainer ──────────────────────────────────────────────────────────────────

def train_model(
    model: BubbleClassifierCNN,
    X: np.ndarray,
    y: np.ndarray,
    epochs: int = TRAIN_EPOCHS,
    lr: float = LEARNING_RATE,
) -> BubbleClassifierCNN:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.train()

    X_t = torch.tensor(X, dtype=torch.float32)
    y_t = torch.tensor(y, dtype=torch.long)

    # 90/10 train/val split
    n_val = max(1, int(len(y_t) * 0.10))
    perm = torch.randperm(len(y_t))
    val_idx, train_idx = perm[:n_val], perm[n_val:]

    train_ds = TensorDataset(X_t[train_idx], y_t[train_idx])
    val_ds   = TensorDataset(X_t[val_idx],   y_t[val_idx])
    train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_dl   = DataLoader(val_ds,   batch_size=BATCH_SIZE)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    best_val_acc = 0.0

    for epoch in range(1, epochs + 1):
        # ── train ──
        model.train()
        total_loss, correct, total = 0.0, 0, 0
        for xb, yb in train_dl:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(yb)
            correct += (logits.argmax(1) == yb).sum().item()
            total += len(yb)
        train_acc = correct / total

        # ── validate ──
        model.eval()
        v_correct, v_total = 0, 0
        with torch.no_grad():
            for xb, yb in val_dl:
                xb, yb = xb.to(device), yb.to(device)
                preds = model(xb).argmax(1)
                v_correct += (preds == yb).sum().item()
                v_total += len(yb)
        val_acc = v_correct / v_total

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            # Atomic save to prevent corrupted/half-written files
            tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pt", dir=os.path.dirname(MODEL_PATH))
            os.close(tmp_fd)
            torch.save(model.state_dict(), tmp_path)
            os.replace(tmp_path, MODEL_PATH)

        scheduler.step()

        if epoch % 5 == 0 or epoch == 1:
            logger.info(
                f"  Epoch {epoch:3d}/{epochs} | "
                f"Loss: {total_loss/total:.4f} | "
                f"Train: {train_acc:.3f} | "
                f"Val: {val_acc:.3f} | "
                f"Best: {best_val_acc:.3f}"
            )
        # Also print for console visibility
        if epoch % 5 == 0 or epoch == 1:
            print(
                f"  Epoch {epoch:3d}/{epochs} | "
                f"loss={total_loss/total:.4f} | "
                f"train_acc={train_acc:.1%} | "
                f"val_acc={val_acc:.1%} | "
                f"best={best_val_acc:.1%}"
            )

    # Reload best weights
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    print(f"\n✅ Training complete. Best val accuracy: {best_val_acc:.1%}")
    print(f"   Model saved to: {MODEL_PATH}")
    return model


# ─── AIBubbleVerifier — the main interface ────────────────────────────────────

_GLOBAL_AI_VERIFIER: Optional["AIBubbleVerifier"] = None
_GLOBAL_VERIFIER_LOCK = threading.Lock()

def get_ai_verifier(model_path: str = MODEL_PATH) -> "AIBubbleVerifier":
    """Returns a pre-warmed, process-wide cached singleton of AIBubbleVerifier."""
    global _GLOBAL_AI_VERIFIER
    if _GLOBAL_AI_VERIFIER is None:
        with _GLOBAL_VERIFIER_LOCK:
            if _GLOBAL_AI_VERIFIER is None:
                _GLOBAL_AI_VERIFIER = AIBubbleVerifier(model_path=model_path)
    return _GLOBAL_AI_VERIFIER


class AIBubbleVerifier:
    """
    Production-grade bubble classifier.

    Usage:
        verifier = AIBubbleVerifier()
        result   = verifier.predict(bubble_crop_bgr_or_gray)
        # result = {
        #   "label": "filled",
        #   "confidence": 0.987,
        #   "distribution": {"empty": 0.003, "filled": 0.987, ...},
        #   "needs_review": False
        # }
    """

    def __init__(self, model_path: str = MODEL_PATH, auto_train: bool = False):
        self.normalizer = BubbleNormalizer()
        self.device     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model      = BubbleClassifierCNN().to(self.device)
        self.model.eval()

        self.is_yolo_ready = False
        self.is_cnn_ready  = False
        
        # ── 1. Primary Engine: Master Unified YOLOv8 Verifier ──
        self.yolo_verifier = None
        try:
            from .master_yolo_verifier import get_master_yolo_verifier
            yolo_path = os.path.join(os.path.dirname(__file__), "master_omr_yolo.pt")
            if os.path.exists(yolo_path):
                self.yolo_verifier = get_master_yolo_verifier(model_path=yolo_path)
                if self.yolo_verifier.model is not None:
                    self.is_yolo_ready = True
                    print(f"✅ [AI Verification] Master Unified YOLOv8 Verifier Active: {yolo_path}")
        except Exception as e:
            logger.warning(f"Could not initialize Master YOLO verifier: {e}")
            self.yolo_verifier = None

        # ── 2. Auxiliary Engine: Certified ResNet CNN Verifier ──
        # Always attempt to load the certified CNN weights so that fallbacks, Grad-CAM,
        # and embedding extraction never operate on random untrained weights!
        if os.path.exists(model_path):
            try:
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                self.is_cnn_ready = True
                logger.info(f"AI CNN model loaded from {model_path}")
                print(f"✅ [AI Verification] Certified CNN Auxiliary Verifier Active: {model_path}")
            except Exception as e:
                logger.warning(f"Could not load CNN model: {e}")
                self.is_cnn_ready = False
                if auto_train:
                    self._auto_train()
        elif auto_train:
            print(f"[AI] No model found at {model_path}. Training now...")
            self._auto_train()
        else:
            logger.warning(f"⚠️ [AI Verification] CNN weights not found at {model_path}. Auxiliary CNN disabled.")

    def _auto_train(self):
        """Generate data and train the model from scratch (offline only)."""
        print("[AI] Generating realistic training dataset (10,000 samples)...")
        gen = RealisticBubbleDataGenerator()
        X, y = gen.generate_dataset(n_per_class=TRAIN_SAMPLES_PER_CLASS)
        print(f"[AI] Dataset ready: {X.shape} | Training for {TRAIN_EPOCHS} epochs...")
        self.model = train_model(self.model, X, y)
        self.model.eval()
        self.is_cnn_ready = True

    # ── inference ─────────────────────────────────────────────────────────────

    def predict(self, crop: np.ndarray) -> Dict:
        """
        Classify a single raw bubble crop with hybrid YOLOv8 -> CNN fallback.
        """
        results = self.predict_batch([crop])
        return results[0] if results else {
            "status": "error",
            "detection_succeeded": False,
            "label": "unclassified",
            "confidence": 0.0,
            "distribution": {c: 0.0 for c in CLASS_NAMES},
            "decision_reason": "EMPTY_OR_FAILED_INFERENCE",
            "needs_review": True
        }

    def _predict_batch_cnn(self, crops: List[np.ndarray]) -> List[Dict]:
        """Classify a batch of bubble crops using the certified ResNet CNN."""
        if not crops:
            return []
        if not self.is_cnn_ready:
            raise RuntimeError("CNN verifier weights are not loaded.")

        normed = self.normalizer.normalize_batch(crops)     # (N, 48, 48)
        tensor = torch.tensor(normed, dtype=torch.float32).unsqueeze(1).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs  = torch.softmax(logits, dim=1).cpu().numpy()  # (N, 5)

        results = []
        for idx, row in enumerate(probs):
            raw_idx        = int(row.argmax())
            raw_label      = CLASS_NAMES[raw_idx]
            raw_confidence = float(row[raw_idx])

            final_label      = raw_label
            final_confidence = raw_confidence
            decision_reason  = "CNN_RAW_OUTPUT"
            
            # Hybrid Thresholding Policy
            if raw_label in ['erased', 'crossed'] and raw_confidence < 0.85:
                empty_idx = CLASS_NAMES.index('empty')
                filled_idx = CLASS_NAMES.index('filled')
                if row[empty_idx] > row[filled_idx]:
                    final_label = 'empty'
                    final_confidence = float(row[empty_idx])
                    decision_reason = "POLICY_FALLBACK_LOW_CONF_ERASED_CROSSED_TO_EMPTY"
                else:
                    final_label = 'filled'
                    final_confidence = float(row[filled_idx])
                    decision_reason = "POLICY_FALLBACK_LOW_CONF_ERASED_CROSSED_TO_FILLED"
                
            entropy      = float(-np.sum(row * np.log2(row + 1e-9)))   # H(P)
            norm_entropy = float(entropy / np.log2(len(CLASS_NAMES)))
            review_reasons = []
            if final_confidence < REVIEW_THRESHOLD:
                review_reasons.append(f"LOW_CONFIDENCE: {final_confidence:.2%}")
            if decision_reason != "CNN_RAW_OUTPUT":
                review_reasons.append(f"POLICY_RULE: {decision_reason}")
            if norm_entropy > 0.65:
                review_reasons.append(f"HIGH_ENTROPY: {norm_entropy:.2f}")

            results.append({
                "status":             "success",
                "detection_succeeded": True,
                "crop_index":         idx,
                "label":              final_label,
                "confidence":         round(final_confidence, 4),
                "distribution":       {n: round(float(p), 4) for n, p in zip(CLASS_NAMES, row)},
                "entropy":            round(entropy, 4),
                "normalized_entropy": round(norm_entropy, 4),
                "raw_prediction":     raw_label,
                "raw_confidence":     round(raw_confidence, 4),
                "decision_reason":    decision_reason,
                "needs_review":       len(review_reasons) > 0,
                "review_reasons":     review_reasons,
                "model_name":         "ResNet_CNN_v4",
                "model_version":      "4.0",
            })
        return results

    def predict_batch(self, crops: List[np.ndarray]) -> List[Dict]:
        """Classify a batch of bubble crops with automatic auxiliary CNN fallback."""
        if not crops:
            return []
            
        yolo_results = None
        if self.is_yolo_ready and self.yolo_verifier is not None:
            try:
                yolo_results = self.yolo_verifier.predict_batch(crops)
            except Exception as e:
                logger.warning(f"Master YOLO batch prediction failed: {e}")
                yolo_results = None

        if yolo_results is not None:
            # Check for any crops where YOLO failed to detect a box or returned unknown/low-confidence
            failed_indices = [
                i for i, r in enumerate(yolo_results)
                if not r.get("detection_succeeded", True) or r.get("label") in ["unknown", "unclassified"] or r.get("confidence", 0.0) < 0.20
            ]
            if failed_indices and self.is_cnn_ready:
                failed_crops = [crops[i] for i in failed_indices]
                cnn_fallback_results = self._predict_batch_cnn(failed_crops)
                for orig_idx, cnn_res in zip(failed_indices, cnn_fallback_results):
                    cnn_res["decision_reason"] = f"CNN_FALLBACK_AFTER_YOLO_MISS: {cnn_res.get('decision_reason', '')}"
                    cnn_res["crop_index"] = orig_idx
                    yolo_results[orig_idx] = cnn_res
            return yolo_results

        if not self.is_cnn_ready:
            raise RuntimeError(
                "Neither YOLOv8 nor CNN verifier weights are loaded. Cannot perform batch inference."
            )

        return self._predict_batch_cnn(crops)

    # ── Grad-CAM ─────────────────────────────────────────────────────────────

    def gradcam(self, crop: np.ndarray, target_class: Optional[int] = None) -> np.ndarray:
        """
        Grad-CAM visual explanation for the auxiliary ResNet CNN.
        Explains feature activations inside the ResidualBlock.
        Note: When YOLOv8 is the primary verifier, Grad-CAM explains the CNN's feature representation.
        Returns a (48, 48) float32 heatmap in [0, 1].
        """
        if not self.is_cnn_ready:
            raise RuntimeError(
                "Cannot generate Grad-CAM: Certified CNN weights are not loaded. "
                "Grad-CAM requires a trained model to compute true gradient activations."
            )

        normalized = self.normalizer.normalize(crop)
        tensor = torch.tensor(normalized, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(self.device)
        tensor.requires_grad_(True)

        self.model.eval()
        feature_maps: list = []
        gradients:    list = []

        # Hook on the last conv layer (ResidualBlock inside features[-1])
        def fwd_hook(m, inp, out):
            feature_maps.append(out.detach())

        def bwd_hook(m, grad_in, grad_out):
            gradients.append(grad_out[0])

        # Register on ResidualBlock's second Conv2d (block[-2] in Conv-BN-ReLU-Conv-BN)
        last_conv = self.model.features[-1].block[-2]
        h_fwd = last_conv.register_forward_hook(fwd_hook)
        h_bwd = last_conv.register_full_backward_hook(bwd_hook)

        try:
            logits = self.model(tensor)
            probs  = torch.softmax(logits, dim=1).squeeze(0)

            if target_class is None:
                target_class = int(probs.argmax())

            # Backprop for target class
            self.model.zero_grad()
            logits[0, target_class].backward()

            # Pool gradients across spatial dims
            grad  = gradients[0].squeeze(0)          # (C, H, W)
            fmaps = feature_maps[0].squeeze(0)       # (C, H, W)
            weights = grad.mean(dim=(1, 2))           # (C,)

            cam = torch.zeros(fmaps.shape[1:], device=self.device)
            for i, w in enumerate(weights):
                cam += w * fmaps[i]

            cam = torch.relu(cam).cpu().numpy()
            cam = cam - cam.min()
            if cam.max() > 0:
                cam = cam / cam.max()
            cam = cv2.resize(cam, (INPUT_SIZE, INPUT_SIZE), interpolation=cv2.INTER_LINEAR)
            return cam.astype(np.float32)
        finally:
            h_fwd.remove()
            h_bwd.remove()
            self.model.zero_grad()

    def gradcam_overlay(self, crop: np.ndarray, target_class: Optional[int] = None) -> np.ndarray:
        """Returns a BGR image (48×48) with Grad-CAM heatmap overlaid on the bubble."""
        cam   = self.gradcam(crop, target_class)
        norm  = self.normalizer.normalize(crop)

        # Convert grayscale to BGR
        base  = (np.clip(norm * 255, 0, 255)).astype(np.uint8)
        base_bgr = cv2.cvtColor(base, cv2.COLOR_GRAY2BGR)

        # Apply colormap
        heatmap   = cv2.applyColorMap((cam * 255).astype(np.uint8), cv2.COLORMAP_JET)
        overlay   = cv2.addWeighted(base_bgr, 0.45, heatmap, 0.55, 0)
        return overlay

    # ── Embedding (128-d latent vector) ──────────────────────────────────────

    def get_embedding(self, crop: np.ndarray) -> np.ndarray:
        """Return 128-d feature vector before the final classifier layer."""
        normalized = self.normalizer.normalize(crop)
        tensor = torch.tensor(normalized, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(self.device)
        with torch.no_grad():
            feats = self.model.features(tensor)     # (1, 128, H, W)
            emb   = self.model.gap(feats).squeeze() # (128,)
        return emb.cpu().numpy()

    def get_embedding_batch(self, crops: List[np.ndarray]) -> np.ndarray:
        """Return (N, 128) embedding matrix for a batch of crops."""
        normed = self.normalizer.normalize_batch(crops)
        tensor = torch.tensor(normed, dtype=torch.float32).unsqueeze(1).to(self.device)
        with torch.no_grad():
            feats = self.model.features(tensor)
            emb   = self.model.gap(feats).squeeze(dim=(2, 3))
        return emb.cpu().numpy()

    # ── Entropy helper ───────────────────────────────────────────────────────

    @staticmethod
    def prediction_entropy(probs_dict: Dict[str, float]) -> float:
        """H(P) = -Σ p·log2(p) — higher means more uncertain (0 = certain, 2.32 = max for 5 classes)."""
        p = np.array(list(probs_dict.values()), dtype=np.float64)
        return float(-np.sum(p * np.log2(p + 1e-9)))


    def verify_ambiguous_bubbles(
        self,
        bubble_crops: Dict[str, np.ndarray],
        classical_results: Optional[Dict[str, str]] = None,
        darkness_values: Optional[Dict[str, float]] = None,
        confidence_threshold: float = 0.80,
    ) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
        """
        Production Hybrid Verification & Conflict Arbitration Engine.
        Compares Classical OpenCV pixel measurements with AI Model Predictions.
        Flags discrepancies, low-confidence bubbles, and ambiguous ink artifacts.

        Parameters
        ----------
        bubble_crops : Dict[str, np.ndarray]
            Map of choice identifier -> raw cropped bubble image.
        classical_results : Optional[Dict[str, str]]
            Map of choice identifier -> classical label ('filled', 'empty', etc.).
        darkness_values : Optional[Dict[str, float]]
            Map of choice identifier -> calculated dark pixel ratio (0.0 to 1.0).
        confidence_threshold : float
            Threshold below which bubbles are marked for human review.

        Returns
        -------
        Tuple[Dict[str, Dict[str, Any]], List[str]]
            - ai_results: Normalized Unified Prediction Contract for every bubble.
            - flagged_keys: List of bubble IDs requiring human review.
        """
        if not bubble_crops:
            return {}, []

        all_keys = list(bubble_crops.keys())
        all_crops = [bubble_crops[k] for k in all_keys]
        predictions = self.predict_batch(all_crops)

        if len(predictions) != len(all_keys):
            raise RuntimeError(
                f"Batch prediction synchronization error: submitted {len(all_keys)} crops, "
                f"but received {len(predictions)} predictions."
            )

        ai_results = {}
        flagged_keys = []

        for key, pred in zip(all_keys, predictions):
            review_reasons = list(pred.get("review_reasons", []))
            pred_label = pred.get("label", "empty")
            pred_conf = pred.get("confidence", 0.0)

            # ── Check 1: Classical vs AI Conflict Arbitration ──
            if classical_results is not None and key in classical_results:
                class_label = classical_results[key]
                if class_label != pred_label:
                    pred["needs_review"] = True
                    reason_msg = f"CLASSICAL_AI_DISAGREEMENT: classical='{class_label}' vs ai='{pred_label}'"
                    if reason_msg not in review_reasons:
                        review_reasons.append(reason_msg)
                    if pred.get("decision_reason") in ("MODEL_RAW_OUTPUT", "YOLO_OBJECT_DETECTION"):
                        pred["decision_reason"] = "HYBRID_CONFLICT_ARBITRATION"

            # ── Check 2: Low Model Confidence ──
            if pred_conf < confidence_threshold:
                pred["needs_review"] = True
                conf_msg = f"LOW_CONFIDENCE: {pred_conf:.2%}"
                if conf_msg not in review_reasons:
                    review_reasons.append(conf_msg)

            # ── Check 3: Extreme Darkness Discrepancy (Physical Ink Sanity) ──
            if darkness_values is not None and key in darkness_values:
                d_val = darkness_values[key]
                if d_val >= 0.40 and pred_label == "empty":
                    pred["needs_review"] = True
                    review_reasons.append(f"PHYSICAL_INK_OVERRIDE: darkness={d_val:.2f} but AI said empty")
                elif d_val <= 0.05 and pred_label in ("filled", "crossed"):
                    pred["needs_review"] = True
                    review_reasons.append(f"PHYSICAL_EMPTY_OVERRIDE: darkness={d_val:.2f} but AI said {pred_label}")

            # ── Check 4: High Prediction Entropy (Ambiguity) ──
            if pred.get("entropy", 0.0) > 1.25:
                pred["needs_review"] = True
                ent_msg = f"HIGH_ENTROPY: {pred.get('entropy'):.2f}"
                if ent_msg not in review_reasons:
                    review_reasons.append(ent_msg)

            pred["review_reasons"] = review_reasons
            ai_results[key] = pred

            if pred.get("needs_review", False):
                flagged_keys.append(key)
                logger.debug(
                    f"  [REVIEW_FLAG] {key}: {pred_label} (Conf: {pred_conf:.1%}) | Reasons: {review_reasons}"
                )

        return ai_results, flagged_keys


# ─── Convenience: re-train from CLI ───────────────────────────────────────────
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("OMR Bubble CNN v2 — Training")
    print("=" * 60)

    force = "--force" in sys.argv
    if force and os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)
        print(f"Removed old model: {MODEL_PATH}")

    verifier = AIBubbleVerifier(auto_train=True)
    print("\nDone. Model is ready for production use.")
