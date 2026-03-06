#!/usr/bin/env python3
import os, random, string
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black

W, H = 8.5*inch, 11*inch
M = 0.6*inch

class InteractiveWorkbook:
    def __init__(self, title="Ultimate Kids Interactive Learning Workbook"):
        self.title = title
        self.page = 0
        self.out_dir = "interactive_books/output"
        os.makedirs(self.out_dir, exist_ok=True)
        self.path = f"{self.out_dir}/{self.title.replace(' ','_')}.pdf"
        self.c = canvas.Canvas(self.path, pagesize=(W,H))

    def np(self):
        if self.page: self.c.showPage()
        self.page += 1
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(HexColor("#999999"))
        self.c.drawRightString(W-M, 0.35*inch, str(self.page))

    def header(self, t, s=""):
        self.c.setFillColor(HexColor("#2E86DE"))
        self.c.rect(0, H-1.1*inch, W, 1.1*inch, fill=1, stroke=0)
        self.c.setFillColor(HexColor("#ffffff"))
        self.c.setFont("Helvetica-Bold", 20)
        self.c.drawString(M, H-0.68*inch, t)
        if s:
            self.c.setFont("Helvetica", 11)
            self.c.drawString(M, H-0.95*inch, s)

    def cover(self):
        self.np()
        self.c.setFillColor(HexColor("#2E86DE"))
        self.c.rect(0, H-2.5*inch, W, 2.5*inch, fill=1, stroke=0)
        self.c.setFillColor(HexColor("#fff"))
        self.c.setFont("Helvetica-Bold", 30)
        self.c.drawString(M, H-1.45*inch, "Ultimate Kids")
        self.c.drawString(M, H-1.95*inch, "Interactive Workbook")
        self.c.setFillColor(HexColor("#333"))
        self.c.setFont("Helvetica", 14)
        self.c.drawString(M, H-3.1*inch, "Real Mazes • Word Search • Find-Me • Tracing • Logic")
        self.c.drawString(M, H-3.45*inch, "Ages 5-9 | Print & Use")

    def tracing_page(self, letter):
        self.np(); self.header(f"Trace Letter: {letter}", "Trace first, then write on blank lines")
        y = H-2.2*inch
        for row in range(5):
            self.c.setStrokeColor(HexColor("#d9d9d9")); self.c.setLineWidth(1)
            self.c.line(M, y+0.35*inch, W-M, y+0.35*inch)
            self.c.setDash(3,3); self.c.line(M, y, W-M, y); self.c.setDash()
            self.c.line(M, y-0.35*inch, W-M, y-0.35*inch)
            self.c.setFont("Helvetica-Bold", 54); self.c.setFillColor(HexColor("#b0b0b0"))
            for i in range(4):
                x = M+0.2*inch+i*1.9*inch
                if row < 3 or i < 2:
                    self.c.drawString(x, y-0.18*inch, letter)
            y -= 1.6*inch

    def number_tracing(self, n):
        self.np(); self.header(f"Trace Number: {n}", "Count objects, then trace and write")
        self.c.setFont("Helvetica", 28)
        for i in range(n):
            col=i%6; row=i//6
            self.c.drawString(M+0.2*inch+col*1.2*inch, H-2.2*inch-row*0.9*inch, "⭐")
        y = H-5.3*inch
        for r in range(4):
            self.c.setStrokeColor(HexColor("#d9d9d9")); self.c.line(M,y, W-M,y)
            self.c.setFont("Helvetica-Bold", 64); self.c.setFillColor(HexColor("#b0b0b0"))
            for i in range(5):
                x = M+0.2*inch+i*1.5*inch
                if r<3 or i<2: self.c.drawString(x, y-0.55*inch, str(n))
            y -= 1.1*inch

    def gen_maze(self, w=12,h=12):
        # DFS maze
        dirs=[(1,0),(-1,0),(0,1),(0,-1)]
        vis=[[False]*h for _ in range(w)]
        walls={(x,y):set(dirs) for x in range(w) for y in range(h)}
        stack=[(0,0)]; vis[0][0]=True
        while stack:
            x,y=stack[-1]
            n=[]
            for dx,dy in dirs:
                nx,ny=x+dx,y+dy
                if 0<=nx<w and 0<=ny<h and not vis[nx][ny]: n.append((nx,ny,dx,dy))
            if not n: stack.pop(); continue
            nx,ny,dx,dy=random.choice(n)
            walls[(x,y)].discard((dx,dy)); walls[(nx,ny)].discard((-dx,-dy))
            vis[nx][ny]=True; stack.append((nx,ny))
        return walls,w,h

    def maze_page(self, idx):
        self.np(); self.header(f"Maze Challenge #{idx}", "Start at 🚀 and reach 🏁")
        walls,w,h=self.gen_maze(14,14)
        x0,y0=M+0.4*inch, M+1.4*inch
        cell=0.5*inch
        self.c.setStrokeColor(black); self.c.setLineWidth(2)
        # draw walls
        for x in range(w):
            for y in range(h):
                cx=x0+x*cell; cy=y0+y*cell
                if (-1,0) in walls[(x,y)] and x==0: self.c.line(cx,cy,cx,cy+cell)
                if (1,0) in walls[(x,y)]: self.c.line(cx+cell,cy,cx+cell,cy+cell)
                if (0,-1) in walls[(x,y)] and y==0: self.c.line(cx,cy,cx+cell,cy)
                if (0,1) in walls[(x,y)]: self.c.line(cx,cy+cell,cx+cell,cy+cell)
        self.c.setFont("Helvetica", 18)
        self.c.drawString(x0-0.35*inch, y0+0.05*inch, "🚀")
        self.c.drawString(x0+w*cell+0.05*inch, y0+h*cell-0.25*inch, "🏁")

    def word_search_page(self, words, idx):
        self.np(); self.header(f"Word Search #{idx}", "Find all words in the grid")
        size=12; grid=[[None]*size for _ in range(size)]
        dirs=[(1,0),(0,1),(1,1),(-1,1)]
        for word in words:
            placed=False
            for _ in range(300):
                dx,dy=random.choice(dirs)
                x=random.randrange(size); y=random.randrange(size)
                ex=x+dx*(len(word)-1); ey=y+dy*(len(word)-1)
                if not (0<=ex<size and 0<=ey<size): continue
                ok=True
                for i,ch in enumerate(word):
                    xx=x+dx*i; yy=y+dy*i
                    if grid[yy][xx] not in (None,ch): ok=False; break
                if not ok: continue
                for i,ch in enumerate(word):
                    xx=x+dx*i; yy=y+dy*i; grid[yy][xx]=ch
                placed=True; break
            if not placed: pass
        for r in range(size):
            for c in range(size):
                if grid[r][c] is None: grid[r][c]=random.choice(string.ascii_uppercase)
        gx,gy=M+0.6*inch, H-7.8*inch; cs=0.42*inch
        self.c.setStrokeColor(HexColor("#888")); self.c.setLineWidth(1)
        self.c.setFont("Helvetica-Bold", 12); self.c.setFillColor(HexColor("#222"))
        for r in range(size):
            for c in range(size):
                x=gx+c*cs; y=gy-r*cs
                self.c.rect(x,y,cs,cs, fill=0, stroke=1)
                self.c.drawString(x+0.15*inch, y+0.14*inch, grid[r][c])
        self.c.setFont("Helvetica", 12)
        self.c.drawString(M, M+0.7*inch, "Words: " + ", ".join(words))

    def find_me_page(self, idx):
        self.np(); self.header(f"Find-Me Puzzle #{idx}", "Find and circle all targets")
        targets=["⭐","🍎","🚗","🐟"]
        pool=targets + ["🍌","⚽","🐶","🌙","🎈","🧩"]
        cols,rows=10,12
        gx,gy=M+0.2*inch, H-2.2*inch
        self.c.setFont("Helvetica", 20)
        target_counts={t:0 for t in targets}
        for r in range(rows):
            for c in range(cols):
                ch=random.choice(pool)
                if random.random()<0.18:
                    ch=random.choice(targets); target_counts[ch]+=1
                x=gx+c*0.75*inch; y=gy-r*0.65*inch
                self.c.drawString(x,y,ch)
        self.c.setFont("Helvetica-Bold", 12); self.c.setFillColor(HexColor("#222"))
        self.c.drawString(M, M+0.6*inch, "Targets: " + "  ".join([f"{t} x ?" for t in targets]))

    def logic_page(self, idx):
        self.np(); self.header(f"Logic Puzzle #{idx}", "Complete the pattern")
        patterns=[
            ["🔺","🔵","🔺","🔵","?"],
            ["1","2","3","1","2","?"],
            ["⭐","⭐","🌙","⭐","⭐","?"],
            ["A","C","E","G","?"],
        ]
        self.c.setFont("Helvetica", 28)
        y=H-2.5*inch
        for p in patterns:
            x=M+0.4*inch
            for item in p:
                self.c.drawString(x,y,item)
                x+=0.9*inch
            y-=1.2*inch
        self.c.setFont("Helvetica", 12)
        self.c.drawString(M, M+0.5*inch, "Write your answers on a separate page.")

    def cert(self):
        self.np();
        self.c.setStrokeColor(HexColor("#2E86DE")); self.c.setLineWidth(4)
        self.c.rect(M,M,W-2*M,H-2*M, fill=0, stroke=1)
        self.c.setFont("Helvetica-Bold", 32); self.c.setFillColor(HexColor("#2E86DE"))
        t="Certificate of Completion"; self.c.drawCentredString(W/2, H-2*inch, t)
        self.c.setFont("Helvetica", 16); self.c.setFillColor(HexColor("#333"))
        self.c.drawCentredString(W/2, H-3*inch, "This certifies that")
        self.c.line(M+1*inch, H-4*inch, W-M-1*inch, H-4*inch)
        self.c.drawCentredString(W/2, H-5*inch, "completed the Interactive Learning Workbook")

    def build(self):
        self.cover()
        self.tracing_page("A"); self.tracing_page("B")
        self.number_tracing(3); self.number_tracing(7)
        for i in range(1,7): self.maze_page(i)
        self.word_search_page(["CAT","DOG","SUN","MOON","BOOK"],1)
        self.word_search_page(["APPLE","FISH","CAR","STAR","TREE"],2)
        self.find_me_page(1); self.find_me_page(2)
        self.logic_page(1); self.logic_page(2)
        self.cert()
        self.c.save()
        return self.path, self.page

if __name__ == "__main__":
    wb=InteractiveWorkbook("Ultimate Kids Interactive Learning Workbook")
    p,n=wb.build()
    print(f"✅ Built: {p}")
    print(f"Pages: {n}")
