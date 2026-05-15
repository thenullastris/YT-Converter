#!/usr/bin/env python3
import customtkinter as ctk
import yt_dlp
import threading
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DOWNLOAD_DIR = os.path.expanduser("~/Downloads")

class YTConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YT Converter")
        self.geometry("520x500")
        self.resizable(True, True)

        # Title
        ctk.CTkLabel(self, text="YouTube Converter", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="Made by TheNullAstris", text_color="#c084fc",
             font=ctk.CTkFont(size=20)).pack(pady=(4, 0))
        ctk.CTkLabel(self, text="Download videos or audio from YouTube", text_color="gray").pack()

        # URL input
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste YouTube URL here...", width=420, height=40)
        self.url_entry.pack(pady=20)

        # Format frame
        fmt_frame = ctk.CTkFrame(self, fg_color="transparent")
        fmt_frame.pack()
        ctk.CTkLabel(fmt_frame, text="Format:").pack(side="left", padx=(0, 12))
        self.format_var = ctk.StringVar(value="mp3")
        ctk.CTkRadioButton(fmt_frame, text="MP3 (Audio)", variable=self.format_var, value="mp3").pack(side="left", padx=8)
        ctk.CTkRadioButton(fmt_frame, text="MP4 (Video)", variable=self.format_var, value="mp4").pack(side="left", padx=8)

        # Quality frame
        qual_frame = ctk.CTkFrame(self, fg_color="transparent")
        qual_frame.pack(pady=8)
        ctk.CTkLabel(qual_frame, text="Quality:").pack(side="left", padx=(0, 12))
        self.quality_var = ctk.StringVar(value="best")
        ctk.CTkRadioButton(qual_frame, text="Best", variable=self.quality_var, value="best").pack(side="left", padx=8)
        ctk.CTkRadioButton(qual_frame, text="720p", variable=self.quality_var, value="720").pack(side="left", padx=8)
        ctk.CTkRadioButton(qual_frame, text="480p", variable=self.quality_var, value="480").pack(side="left", padx=8)

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=420)
        self.progress.pack(pady=16)
        self.progress.set(0)

        # Status
        self.status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status.pack()

        # Button
        self.btn = ctk.CTkButton(self, text="⬇  Convert & Download", width=220, height=44,
                                  font=ctk.CTkFont(size=14, weight="bold"), command=self.start_download)
        self.btn.pack(pady=10)

        # Output folder label
        ctk.CTkLabel(self, text=f"Saves to: {DOWNLOAD_DIR}", text_color="gray",
                     font=ctk.CTkFont(size=11)).pack()


    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status.configure(text="⚠️  Please enter a URL", text_color="orange")
            return
        self.btn.configure(state="disabled", text="Downloading...")
        self.progress.set(0)
        self.status.configure(text="Starting...", text_color="gray")
        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def download(self, url):
        fmt = self.format_var.get()
        quality = self.quality_var.get()

        def progress_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    pct = downloaded / total
                    self.progress.set(pct)
                    self.status.configure(text=f"Downloading... {int(pct*100)}%", text_color="gray")
            elif d['status'] == 'finished':
                self.status.configure(text="Processing...", text_color="gray")

        if fmt == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            }
        else:
            fmt_str = 'bestvideo+bestaudio/best' if quality == 'best' else f'bestvideo[height<={quality}]+bestaudio/best'
            ydl_opts = {
                'format': fmt_str,
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'merge_output_format': 'mp4',
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.progress.set(1)
            self.status.configure(text="✅ Done! File saved to ~/Downloads", text_color="#4CAF50")
        except Exception as e:
            self.status.configure(text=f"❌ Error: {str(e)[:60]}", text_color="#f44336")
        finally:
            self.btn.configure(state="normal", text="⬇  Convert & Download")

if __name__ == "__main__":
    app = YTConverterApp()
    app.mainloop()