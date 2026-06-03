"""
💕 will_you_be_mine.py — A Special Question for Terry
=====================================================
HOW TO RUN:
  1. Make sure Python 3 is installed (Tkinter comes built-in).
  2. In your terminal run:
       python will_you_be_mine.py
  3. That's it — just be prepared for a "Yes"! 🎉
"""

import tkinter as tk
from tkinter import messagebox
import random
import math

# ── Palette ───────────────────────────────────────────────────────────────────
BG          = "#fff0f5"          # lavender blush
ACCENT      = "#ff6b9d"          # hot pink
ACCENT2     = "#c44b8a"          # deeper rose
TEXT_MAIN   = "#4a1942"          # dark plum
TEXT_SUB    = "#9b4f7e"          # muted mauve
YES_BG      = "#ff6b9d"
YES_HOV     = "#ff4080"
NO_BG       = "#d6d6e8"
NO_HOV      = "#b0b0cc"
CONFETTI_COLORS = [
    "#ff6b9d","#ff9ecd","#ffd6e8","#c44b8a",
    "#ffb347","#ffe066","#a8edea","#9b59b6",
    "#f9ca24","#6ab04c","#eb4d4b","#30336b",
]

# ── Main App ──────────────────────────────────────────────────────────────────
class GirlfriendApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("A Special Question <3")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._center(600, 480)

        # Confetti / particle state
        self.confetti_items: list[dict] = []
        self.sparkle_items:  list[int]  = []
        self.floating_hearts: list[dict] = []
        self.animating = False

        # No-button run-away state
        self._no_escaped = 0          # how many times it ran
        self._no_timeout_id = None

        self._build_question_screen()

    # ── Layout helpers ────────────────────────────────────────────────────────
    def _center(self, w: int, h: int):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _clear(self):
        """Destroy every widget in the root."""
        if self._no_timeout_id:
            self.root.after_cancel(self._no_timeout_id)
        for w in self.root.winfo_children():
            w.destroy()

    # ── Question screen ───────────────────────────────────────────────────────
    def _build_question_screen(self):
        self._clear()
        self.animating = False

        # Floating hearts in the background (canvas layer)
        self.bg_canvas = tk.Canvas(
            self.root, width=600, height=480,
            bg=BG, highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0)
        self.floating_hearts = []
        for _ in range(18):
            self._spawn_bg_heart()
        self._animate_bg_hearts()

        # ── Top decorative hearts ──────────────────────────────────────────
        deco = tk.Label(self.root, text="💗  💕  💗  💕  💗",
                        font=("Georgia", 16), bg=BG, fg=ACCENT)
        deco.place(relx=0.5, rely=0.06, anchor="center")

        # ── Main question ─────────────────────────────────────────────────
        lbl = tk.Label(
            self.root,
            text="Terry, will you be\nmy girlfriend?",
            font=("Georgia", 28, "bold"),
            bg=BG, fg=TEXT_MAIN,
            justify="center",
            wraplength=520,
        )
        lbl.place(relx=0.5, rely=0.38, anchor="center")

        sub = tk.Label(
            self.root,
            text="(think very carefully before answering 😉)",
            font=("Georgia", 11, "italic"),
            bg=BG, fg=TEXT_SUB,
        )
        sub.place(relx=0.5, rely=0.57, anchor="center")

        # ── Buttons ───────────────────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.place(relx=0.5, rely=0.72, anchor="center")

        self.yes_btn = self._make_btn(
            btn_frame, "Yes  💖", YES_BG, YES_HOV, "white",
            self._on_yes
        )
        self.yes_btn.grid(row=0, column=0, padx=24)

        self.no_btn = self._make_btn(
            btn_frame, "No", NO_BG, NO_HOV, TEXT_MAIN,
            lambda: None   # real action bound via motion
        )
        self.no_btn.grid(row=0, column=1, padx=24)
        # Bind mouse-enter so the button runs away
        self.no_btn.bind("<Enter>", self._no_run_away)

        # ── Bottom hearts ─────────────────────────────────────────────────
        tk.Label(self.root, text="✨  💝  ✨",
                 font=("Georgia", 14), bg=BG, fg=ACCENT
                 ).place(relx=0.5, rely=0.90, anchor="center")

    def _make_btn(self, parent, text, bg, hover_bg, fg, cmd):
        btn = tk.Button(
            parent, text=text, command=cmd,
            font=("Georgia", 14, "bold"),
            bg=bg, fg=fg, activebackground=hover_bg,
            relief="flat", cursor="hand2",
            padx=26, pady=10, bd=0,
            highlightthickness=2, highlightbackground=ACCENT,
        )
        btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.configure(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg:       b.configure(bg=c))
        return btn

    # ── No button runs away ───────────────────────────────────────────────────
    def _no_run_away(self, event=None):
        """Teleport the No button to a random safe position on screen."""
        self._no_escaped += 1
        # keep it within the window
        max_x = 580 - self.no_btn.winfo_width()
        max_y = 460 - self.no_btn.winfo_height()
        nx = random.randint(10, max(10, max_x))
        ny = random.randint(10, max(10, max_y))
        self.no_btn.place_forget()
        self.no_btn.grid_forget()
        self.no_btn.place(x=nx, y=ny)

        # After enough escapes, show a cheeky message
        if self._no_escaped in (3, 6, 10):
            msgs = [
                "Nope, that button doesn't work here 😄",
                "Still trying to say no? Bold strategy 😂",
                "The answer is Yes. You just haven't accepted it yet 💕",
            ]
            idx = [3,6,10].index(self._no_escaped)
            self._flash_message(msgs[idx])

    def _flash_message(self, text: str):
        """Show a temporary floating label that fades away."""
        lbl = tk.Label(
            self.root, text=text,
            font=("Georgia", 11, "italic"),
            bg="#ffe0ee", fg=ACCENT2,
            padx=10, pady=6,
            relief="flat",
        )
        lbl.place(relx=0.5, rely=0.82, anchor="center")
        self.root.after(2200, lbl.destroy)

    # ── Background floating hearts ────────────────────────────────────────────
    def _spawn_bg_heart(self):
        x = random.randint(20, 580)
        y = random.randint(-50, 480)
        size = random.choice([12, 16, 20, 24])
        alpha_char = random.choice(["💗","💕","💓","🩷","❤️"])
        item_id = self.bg_canvas.create_text(
            x, y, text=alpha_char,
            font=("Arial", size), fill=ACCENT,
        )
        speed = random.uniform(0.4, 1.1)
        drift = random.uniform(-0.4, 0.4)
        self.floating_hearts.append({"id": item_id, "speed": speed, "drift": drift})

    def _animate_bg_hearts(self):
        if not hasattr(self, 'bg_canvas') or not self.bg_canvas.winfo_exists():
            return
        to_reset = []
        for h in self.floating_hearts:
            self.bg_canvas.move(h["id"], h["drift"], h["speed"])
            x, y = self.bg_canvas.coords(h["id"])
            if y > 500:
                to_reset.append(h)
        for h in to_reset:
            self.bg_canvas.coords(h["id"], random.randint(20,580), -20)
        self.root.after(30, self._animate_bg_hearts)

    # ── Yes! ──────────────────────────────────────────────────────────────────
    def _on_yes(self):
        self._clear()
        self.animating = True
        self.confetti_items = []
        self.sparkle_items  = []

        # Full-screen canvas for celebration effects
        self.canvas = tk.Canvas(
            self.root, width=600, height=480,
            bg=BG, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # ── "Thank you" label ────────────────────────────────────────────
        self.canvas.create_text(
            300, 160,
            text="Thank you!  ❤️",
            font=("Georgia", 36, "bold"),
            fill=ACCENT2,
            tags="thanks",
        )
        self.canvas.create_text(
            300, 215,
            text="You've made me the happiest person alive 🥹",
            font=("Georgia", 13, "italic"),
            fill=TEXT_SUB,
            tags="sub",
        )

        # Seed confetti
        for _ in range(70):
            self._spawn_confetti()
        # Seed sparkles
        for _ in range(20):
            self._spawn_sparkle()

        self._animate_celebration()

    # ── Confetti ──────────────────────────────────────────────────────────────
    def _spawn_confetti(self, y_start: int = None):
        x = random.randint(0, 600)
        y = y_start if y_start is not None else random.randint(-480, 0)
        w = random.randint(6, 14)
        h = random.randint(6, 14)
        color = random.choice(CONFETTI_COLORS)
        shape = random.choice(["rect", "oval"])
        if shape == "rect":
            item = self.canvas.create_rectangle(
                x, y, x+w, y+h, fill=color, outline=""
            )
        else:
            item = self.canvas.create_oval(
                x, y, x+w, y+h, fill=color, outline=""
            )
        speed  = random.uniform(2.0, 5.0)
        drift  = random.uniform(-1.2, 1.2)
        wiggle = random.uniform(0, math.pi * 2)
        self.confetti_items.append({
            "id": item, "speed": speed, "drift": drift,
            "wiggle": wiggle, "age": 0,
        })

    # ── Sparkles ──────────────────────────────────────────────────────────────
    def _spawn_sparkle(self):
        x = random.randint(20, 580)
        y = random.randint(20, 460)
        chars = ["✨","💖","🌸","⭐","💫","🩷","❣️"]
        item = self.canvas.create_text(
            x, y, text=random.choice(chars),
            font=("Arial", random.randint(14, 26)),
        )
        life = random.randint(20, 60)
        self.sparkle_items.append({"id": item, "life": life})

    # ── Main celebration animation loop ──────────────────────────────────────
    def _animate_celebration(self):
        if not self.animating:
            return

        # Move confetti
        to_respawn = []
        for c in self.confetti_items:
            c["wiggle"] += 0.08
            dx = c["drift"] + 0.6 * math.sin(c["wiggle"])
            self.canvas.move(c["id"], dx, c["speed"])
            coords = self.canvas.coords(c["id"])
            if not coords:
                continue
            y = coords[1] if len(coords) >= 2 else 0
            if y > 500:
                to_respawn.append(c)

        for c in to_respawn:
            self.canvas.delete(c["id"])
            self.confetti_items.remove(c)
            self._spawn_confetti(y_start=random.randint(-40, -5))

        # Fade / cycle sparkles
        dead = []
        for s in self.sparkle_items:
            s["life"] -= 1
            if s["life"] <= 0:
                dead.append(s)
        for s in dead:
            self.canvas.delete(s["id"])
            self.sparkle_items.remove(s)
        # Replenish sparkles
        while len(self.sparkle_items) < 20:
            self._spawn_sparkle()

        # Pulse the "Thank you" text gently
        t = self.root.tk.call("clock", "milliseconds")
        scale = 1 + 0.04 * math.sin(int(t) / 400)
        size = int(36 * scale)
        self.canvas.itemconfigure(
            "thanks",
            font=("Georgia", max(28, size), "bold"),
        )

        self.root.after(28, self._animate_celebration)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = GirlfriendApp(root)
    root.mainloop()
