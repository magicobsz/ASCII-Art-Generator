from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import random

class AAG:
    def __init__(self, master):
        self.m = master
        self.m.title("ASCII Art Generator")
        self.m.geometry("800x600")
        
        self.ac = list("@#S%?*+;:,")  # 让白色区域没有字符
        random.shuffle(self.ac)
        
        self.font_size = 5
        self.contrast = 1.0
        self.white_threshold = 200  #阈值，高于此值不显示字符
        
        self.cw()
        
    def cw(self):
        tf = tk.Frame(self.m)
        tf.pack(pady=10)
        
        self.sb = tk.Button(tf, text="选择图片", command=self.si, bg="#4CAF50", fg="white", font=("Arial", 10))
        self.sb.pack(side=tk.LEFT, padx=3)
        
        self.gb = tk.Button(tf, text="生成", command=self.ga, bg="#2196F3", fg="white", font=("Arial", 10), state=tk.DISABLED)
        self.gb.pack(side=tk.LEFT, padx=3)
        
        self.eb = tk.Button(tf, text="导出", command=self.ea, bg="#FF9800", fg="white", font=("Arial", 10), state=tk.DISABLED)
        self.eb.pack(side=tk.LEFT, padx=3)
        
        self.cb = tk.Button(tf, text="清空", command=self.ca, bg="#f44336", fg="white", font=("Arial", 10))
        self.cb.pack(side=tk.LEFT, padx=3)
        
        tk.Label(tf, text="宽:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(15, 2))
        self.wv = tk.StringVar(value="120")
        self.we = tk.Entry(tf, textvariable=self.wv, width=4, font=("Arial", 9))
        self.we.pack(side=tk.LEFT, padx=2)
        
        tk.Label(tf, text="字体:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(10, 2))
        self.fv = tk.StringVar(value="5")
        self.fe = tk.Entry(tf, textvariable=self.fv, width=3, font=("Arial", 9))
        self.fe.pack(side=tk.LEFT, padx=2)
        
        tk.Label(tf, text="对比:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(10, 2))
        self.cv = tk.StringVar(value="1.0")
        self.ce = tk.Entry(tf, textvariable=self.cv, width=4, font=("Arial", 9))
        self.ce.pack(side=tk.LEFT, padx=2)
        
        tk.Label(tf, text="白阈:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(10, 2))
        self.wtv = tk.StringVar(value="200")
        self.wte = tk.Entry(tf, textvariable=self.wtv, width=4, font=("Arial", 9))
        self.wte.pack(side=tk.LEFT, padx=2)
        
        mf = tk.Frame(self.m)
        mf.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        lf = tk.Frame(mf)
        lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(lf, text="预览", font=("Arial", 10, "bold")).pack()
        
        self.il = tk.Label(lf, text="无图片", bg="#f0f0f0", relief=tk.SUNKEN, width=40, height=15)
        self.il.pack(fill=tk.BOTH, expand=True, pady=3)
        
        self.infol = tk.Label(lf, text="", font=("Arial", 8), fg="gray")
        self.infol.pack()
        
        rf = tk.Frame(mf)
        rf.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(rf, text="ASCII艺术", font=("Arial", 10, "bold")).pack()
        
        self.at = scrolledtext.ScrolledText(rf, wrap=tk.NONE, font=("Courier New", self.font_size), bg="black", fg="white")
        self.at.pack(fill=tk.BOTH, expand=True, pady=3)
        
        self.sv = tk.StringVar(value="准备就绪")
        sb = tk.Label(self.m, textvariable=self.sv, relief=tk.SUNKEN, anchor=tk.W)
        sb.pack(side=tk.BOTTOM, fill=tk.X)
    
    def si(self):
        ft = [("图片", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"), ("所有", "*.*")]
        fn = filedialog.askopenfilename(title="选择图片", filetypes=ft)
        
        if fn:
            try:
                self.oi = Image.open(fn)
                ps = (300, 300)
                ip = self.oi.copy()
                ip.thumbnail(ps, Image.Resampling.LANCZOS)
                self.tki = ImageTk.PhotoImage(ip)
                self.il.configure(image=self.tki, text="")
                it = f"尺寸: {self.oi.size[0]} x {self.oi.size[1]}"
                self.infol.configure(text=it)
                self.gb.configure(state=tk.NORMAL)
                self.sv.set(f"已选择: {fn.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("错误", f"无法打开: {str(e)}")
                self.sv.set("错误")
    
    def ga(self):
        if not hasattr(self, 'oi'):
            messagebox.showwarning("警告", "请先选择图片")
            return
        
        try:
            w = int(self.wv.get())
            if w <= 0 or w > 400:
                messagebox.showwarning("警告", "宽度1-400")
                return
                
            self.font_size = int(self.fv.get())
            if self.font_size < 1 or self.font_size > 20:
                messagebox.showwarning("警告", "字体大小1-20")
                return
                
            self.contrast = float(self.cv.get())
            if self.contrast < 0.1 or self.contrast > 5.0:
                messagebox.showwarning("警告", "对比度0.1-5.0")
                return
                
            self.white_threshold = int(self.wtv.get())
            if self.white_threshold < 0 or self.white_threshold > 255:
                messagebox.showwarning("警告", "白阈0-255")
                return
                
            self.sv.set("生成中...")
            self.m.update()
            
            img = self.oi.copy()
            wp = w / float(img.size[0])
            h = int(float(img.size[1]) * float(wp * 0.55))
            
            img = img.resize((w, h), Image.Resampling.NEAREST)
            img = img.convert("L")
            
            # 应用
            if self.contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(self.contrast)
                
            p = img.load()
            
            r = ""
            for i in range(h):
                for j in range(w):
                    g = p[j, i]
                    # 使用空格
                    if g >= self.white_threshold:
                        r += " "
                    else:
                        # 调整映射范围
                        idx = int(g / (self.white_threshold / len(self.ac)))
                        if idx >= len(self.ac):
                            idx = len(self.ac) - 1
                        r += self.ac[idx]
                r += "\n"
            
            self.at.delete(1.0, tk.END)
            self.at.insert(1.0, r)
            self.at.configure(font=("Courier New", self.font_size))
            
            self.eb.configure(state=tk.NORMAL)
            self.sv.set(f"完成 - 尺寸: {w} x {h}")
            
        except ValueError as ve:
            messagebox.showerror("错误", f"数值错误: {str(ve)}")
        except Exception as e:
            messagebox.showerror("错误", f"生成失败: {str(e)}")
            self.sv.set("错误")
    
    def ea(self):
        if not self.at.get(1.0, tk.END).strip():
            messagebox.showwarning("警告", "无内容可导出")
            return
            
        fn = filedialog.asksaveasfilename(
            title="导出ASCII艺术",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if fn:
            try:
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(self.at.get(1.0, tk.END))
                messagebox.showinfo("成功", f"已导出到: {fn}")
                self.sv.set("导出成功")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
                self.sv.set("导出错误")
    
    def ca(self):
        self.at.delete(1.0, tk.END)
        self.il.configure(image="", text="无图片")
        self.infol.configure(text="")
        self.gb.configure(state=tk.DISABLED)
        self.eb.configure(state=tk.DISABLED)
        self.sv.set("已清空")
        
        if hasattr(self, 'oi'):
            del self.oi
        if hasattr(self, 'tki'):
            del self.tki

if __name__ == "__main__":
    r = tk.Tk()
    a = AAG(r)
    r.mainloop()