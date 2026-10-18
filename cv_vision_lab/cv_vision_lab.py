
import cv2
import numpy as np
import customtkinter as ctk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import os


#  CustomTkinter Theme Setup


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


#  Colors & Constants


BG        = "#0d0d0f"
PANEL     = "#13131a"
BORDER    = "#1e1e2e"
ACCENT    = "#00e5ff"
IDLE_BTN  = "#1a1a2e"
TEXT      = "#dde0ff"
DIM       = "#4a4a6a"
RED       = "#ff3355"
GREEN     = "#00ffaa"
FONT_MONO = "Courier New"

MIN_W     = 900
MIN_H     = 600


#  Global State


cap               = None
raw_frame         = None
current_filter    = "Original"
filter_buttons    = {}
cam_buttons       = {}

root              = None
raw_label         = None
proc_label        = None
proc_title_label  = None
status_var        = None
filter_status_var = None
video_frame       = None   # holds the two video panels — used for resize


#  Image Processing Functions


def apply_none(frame):
    return frame

def apply_negative(frame):
    return 255 - frame

def apply_thresholding(frame, threshold_value=125):
    _, thresh = cv2.threshold(frame, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh

def apply_contrast_stretching(frame):
    r_min, r_max = np.min(frame), np.max(frame)
    if r_max == r_min:
        return frame
    return ((frame - r_min) / (r_max - r_min) * 255).astype(np.uint8)

def apply_laplacian(frame):
    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    return cv2.filter2D(frame, -1, kernel)

def apply_laplacian_composite(frame):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(frame, -1, kernel)

def apply_noise(frame, probability=0.02):
    noisy = frame.copy()
    mask = np.random.random(noisy.shape) < probability
    noisy[mask] = 255
    return noisy

def apply_equalize_histogram(frame):
    return cv2.equalizeHist(frame)

def apply_flip_add(frame):
    return cv2.add(frame, cv2.flip(frame, 0))

FILTERS = {
    "Original":            apply_none,
    "Negative":            apply_negative,
    "Thresholding":        apply_thresholding,
    "Contrast Stretch":    apply_contrast_stretching,
    "Laplacian":           apply_laplacian,
    "Laplacian Composite": apply_laplacian_composite,
    "Noise":               apply_noise,
    "Equalize Histogram":  apply_equalize_histogram,
    "Flip Add":            apply_flip_add,
}


#  Camera Functions


def open_camera(index):
    global cap
    if cap:
        cap.release()
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        status_var.set(f"✕  CAM {index} NOT FOUND")
    else:
        status_var.set("●  LIVE")

def switch_camera(index):
    open_camera(index)
    highlight_cam_btn(index)

def highlight_cam_btn(active_idx):
    for idx, btn in cam_buttons.items():
        if idx == active_idx:
            btn.configure(fg_color=ACCENT, text_color=BG)
        else:
            btn.configure(fg_color=IDLE_BTN, text_color=TEXT)


#  Filter Functions


def set_filter(name):
    global current_filter
    current_filter = name
    for n, btn in filter_buttons.items():
        if n == name:
            btn.configure(fg_color=ACCENT, text_color=BG,
                          hover_color=ACCENT)
        else:
            btn.configure(fg_color=IDLE_BTN, text_color=TEXT,
                          hover_color="#2a2a4e")
    proc_title_label.configure(text=f"  {name.upper()}  ")
    filter_status_var.set(f"Filter: {name}")


#  Capture


def capture():
    global raw_frame
    if raw_frame is None:
        messagebox.showerror("No Frame", "No frame captured yet.")
        return
    name = simpledialog.askstring(
        "Save Capture",
        "Enter filename (without extension):",
        parent=root
    )
    if not name:
        return
    name = name.strip().replace(" ", "_")
    if not name:
        messagebox.showerror("Invalid Name", "Filename cannot be empty.")
        return

    raw_path  = f"{name}_raw.png"
    proc_path = f"{name}_processed.png"

    gray = cv2.flip(cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY), 1)
    processed = FILTERS[current_filter](gray)

    cv2.imwrite(proc_path, processed)
    messagebox.showinfo(
        "Saved",
        f"Saved to current directory:\n  {os.path.abspath(raw_path)}\n  {os.path.abspath(proc_path)}"
    )


#  Video Update Loop  (resize-aware)


def update_loop():
    global raw_frame
    if cap and cap.isOpened():
        ret, bgr = cap.read()
        if ret:
            raw_frame = bgr.copy()

            # Calculate each panel size from current widget dimensions
            panel_w = max(raw_label.winfo_width(),  320)
            panel_h = max(raw_label.winfo_height(), 240)

            # ── Raw feed (colour, mirrored) ──
            raw_rgb = cv2.cvtColor(cv2.flip(bgr, 1), cv2.COLOR_BGR2RGB)
            raw_rgb = cv2.resize(raw_rgb, (panel_w, panel_h))
            raw_img = ImageTk.PhotoImage(Image.fromarray(raw_rgb))
            raw_label.configure(image=raw_img)
            raw_label.image = raw_img

            # ── Processed feed ──
            gray = cv2.flip(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), 1)
            processed = FILTERS[current_filter](gray)
            if len(processed.shape) == 2:
                proc_rgb = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
            else:
                proc_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
            proc_rgb = cv2.resize(proc_rgb, (panel_w, panel_h))
            proc_img = ImageTk.PhotoImage(Image.fromarray(proc_rgb))
            proc_label.configure(image=proc_img)
            proc_label.image = proc_img

    root.after(15, update_loop)


#  On Close


def on_close():
    global cap
    if cap:
        cap.release()
    root.destroy()


#  UI Builder


def build_ui():
    global root, raw_label, proc_label, proc_title_label
    global status_var, filter_status_var, video_frame

    root = ctk.CTk()
    root.title("CV Vision Lab")
    root.configure(fg_color=BG)
    root.geometry("1360x820")
    root.minsize(MIN_W, MIN_H)
    # Resizable in both directions
    root.resizable(True, True)

    # ── Make rows/cols stretch on resize ─────
    root.grid_rowconfigure(2, weight=1)   # video row expands
    root.grid_columnconfigure(0, weight=1)

    # ── Top bar ──────────────────────────────
    topbar = ctk.CTkFrame(root, fg_color=PANEL, corner_radius=0, height=48)
    topbar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
    topbar.grid_columnconfigure(1, weight=1)
    topbar.grid_propagate(False)

    ctk.CTkLabel(
        topbar, text="  ⬡  CV VISION LAB",
        font=(FONT_MONO, 14, "bold"),
        text_color=ACCENT
    ).grid(row=0, column=0, sticky="w", padx=12, pady=10)

    cam_bar = ctk.CTkFrame(topbar, fg_color="transparent")
    cam_bar.grid(row=0, column=2, sticky="e", padx=12)

    ctk.CTkLabel(
        cam_bar, text="CAMERA ",
        font=(FONT_MONO, 18, "bold"),
        text_color=DIM
    ).pack(side="left", padx=(0, 4))

    for idx, label in [(0, "Primary"), (1, "Secondary"), (2, "Tertiary")]:
        btn = ctk.CTkButton(
            cam_bar, text=label, width=80, height=28,
            font=(FONT_MONO, 18, "bold"),
            fg_color=IDLE_BTN, text_color=TEXT,
            hover_color="#2a2a4e",
            corner_radius=4,
            command=lambda i=idx: switch_camera(i)
        )
        btn.pack(side="left", padx=3)
        cam_buttons[idx] = btn

    highlight_cam_btn(0)

    # ── Thin accent line ──────────────────────
    ctk.CTkFrame(root, fg_color=ACCENT, height=2, corner_radius=0).grid(
        row=1, column=0, sticky="ew"
    )

    # ── Video area ────────────────────────────
    video_frame = ctk.CTkFrame(root, fg_color=BG)
    video_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=10)
    video_frame.grid_columnconfigure(0, weight=1)
    video_frame.grid_columnconfigure(1, weight=1)
    video_frame.grid_rowconfigure(1, weight=1)

    # Left panel header
    ctk.CTkLabel(
        video_frame, text="  RAW FEED",
        font=(FONT_MONO, 15, "bold"),
        text_color=DIM, fg_color=PANEL,
        anchor="w", corner_radius=4
    ).grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 2))

    # Right panel header (dynamic name)
    proc_title_label = ctk.CTkLabel(
        video_frame, text="  ORIGINAL",
        font=(FONT_MONO, 15, "bold"),
        text_color=ACCENT, fg_color=PANEL,
        anchor="w", corner_radius=4
    )

    proc_title_label.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 2))

    # Raw video label
    raw_label = ctk.CTkLabel(video_frame, text="", fg_color="#000000", corner_radius=6)
    raw_label.grid(row=1, column=0, sticky="nsew", padx=(0, 6))

    # Processed video label
    proc_label = ctk.CTkLabel(video_frame, text="", fg_color="#000000", corner_radius=6)
    proc_label.grid(row=1, column=1, sticky="nsew", padx=(6, 0))

    # ── Accent separator ─────────────────────
    ctk.CTkFrame(root, fg_color=BORDER, height=1, corner_radius=0).grid(
        row=3, column=0, sticky="ew", padx=12, pady=(0, 4)
    )

    # ── Filter panel ─────────────────────────
    filter_panel = ctk.CTkFrame(root, fg_color=PANEL, corner_radius=8)
    filter_panel.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 6))

    ctk.CTkLabel(
        filter_panel, text="FILTERS",
        font=(FONT_MONO, 8, "bold"),
        text_color=DIM
    ).grid(row=0, column=0, sticky="w", padx=14, pady=(8, 4))

    btn_grid = ctk.CTkFrame(filter_panel, fg_color="transparent")
    btn_grid.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))

    for i, name in enumerate(FILTERS):
        btn = ctk.CTkButton(
            btn_grid, text=name,
            width=130, height=32,
            font=(FONT_MONO, 11, "bold"),
            fg_color=IDLE_BTN, text_color=TEXT,
            hover_color="#2a2a4e",
            corner_radius=6,
            command=lambda n=name: set_filter(n)
        )
        btn.grid(row=i // 5, column=i % 5, padx=4, pady=4)
        filter_buttons[name] = btn

    # ── Bottom status bar ─────────────────────
    bot = ctk.CTkFrame(root, fg_color=PANEL, corner_radius=0, height=44)
    bot.grid(row=5, column=0, sticky="ew")
    bot.grid_propagate(False)
    bot.grid_columnconfigure(1, weight=1)

    status_var = ctk.StringVar(value="●  LIVE")
    ctk.CTkLabel(
        bot, textvariable=status_var,
        font=(FONT_MONO, 9, "bold"),
        text_color=GREEN
    ).grid(row=0, column=0, sticky="w", padx=16, pady=10)

    filter_status_var = ctk.StringVar(value="Filter: Original")
    ctk.CTkLabel(
        bot, textvariable=filter_status_var,
        font=(FONT_MONO, 9),
        text_color=DIM
    ).grid(row=0, column=1, sticky="w", padx=8)

    ctk.CTkButton(
        bot, text="  ⬡  CAPTURE  ",
        width=130, height=32,
        font=(FONT_MONO, 10, "bold"),
        fg_color=RED, text_color="#ffffff",
        hover_color="#cc2244",
        corner_radius=6,
        command=capture
    ).grid(row=0, column=2, sticky="e", padx=16, pady=6)

    set_filter("Original")


#  Run


build_ui()
open_camera(0)
update_loop()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
