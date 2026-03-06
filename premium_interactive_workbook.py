#!/usr/bin/env python3
import os, random, string, json
from collections import deque
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black

W, H, M = 8.5*inch, 11*inch, 0.6*inch

class PremiumWorkbook:
    def __init__(self, seed=42):
        random.seed(seed)
        self.seed = seed
        self.out_dir = "interactive_books/premium"
        os.makedirs(self.out_dir, exist_ok=True)
        self.book_pdf = f"{self.out_dir}/Premium_Interactive_Workbook_V2.pdf"
        self.key_pdf = f"{self.out_dir}/Premium_Interactive_Workbook_V2_Answer_Key.pdf"
        self.report_json = f"{self.out_dir}/Premium_Interactive_Workbook_V2_Validation.json"
        self.book = canvas.Canvas(self.book_pdf, pagesize=(W,H))
        self.key = canvas.Canvas(self.key_pdf, pagesize=(W,H))
        self.page = 0
        self.validation = {"mazes": [], "word_searches": [], "find_me": []}

    def np(self, c):
        if c is self.book:
            if self.page: c.showPage()
            self.page += 1
            c.setFont("Helvetica", 9); c.setFillColor(HexColor("#999")); c.drawRightString(W-M, 0.35*inch, str(self.page))
        else:
            c.showPage()

    def header(self, c, t, s=""):
        c.setFillColor(HexColor("#1f6feb")); c.rect(0, H-1.05*inch, W, 1.05*inch, fill=1, stroke=0)
        c.setFillColor(HexColor("#fff")); c.setFont("Helvetica-Bold", 18); c.drawString(M, H-0.68*inch, t)
        if s: c.setFont("Helvetica", 10); c.drawString(M, H-0.9*inch, s)

    def cover(self):
        self.np(self.book)
        self.book.setFillColor(HexColor("#1f6feb")); self.book.rect(0, H-2.2*inch, W, 2.2*inch, fill=1, stroke=0)
        self.book.setFillColor(HexColor("#fff")); self.book.setFont("Helvetica-Bold", 30)
        self.book.drawString(M, H-1.35*inch, "Premium Interactive Workbook V2")
        self.book.setFillColor(HexColor("#222")); self.book.setFont("Helvetica", 13)
        self.book.drawString(M, H-2.65*inch, "Real solvable mazes, validated word searches, counted find-me puzzles")

    def make_maze(self, w=12, h=12):
        dirs=[(1,0),(-1,0),(0,1),(0,-1)]
        walls={(x,y):set(dirs) for x in range(w) for y in range(h)}
        vis=[[False]*h for _ in range(w)]
        stack=[(0,0)]; vis[0][0]=True
        while stack:
            x,y=stack[-1]
            nbr=[]
            for dx,dy in dirs:
                nx,ny=x+dx,y+dy
                if 0<=nx<w and 0<=ny<h and not vis[nx][ny]: nbr.append((nx,ny,dx,dy))
            if not nbr:
                stack.pop(); continue
            nx,ny,dx,dy=random.choice(nbr)
            walls[(x,y)].discard((dx,dy)); walls[(nx,ny)].discard((-dx,-dy))
            vis[nx][ny]=True; stack.append((nx,ny))
        return walls,w,h

    def solve_maze(self, walls, w, h):
        q=deque([(0,0)]); prev={(0,0):None}
        while q:
            x,y=q.popleft()
            if (x,y)==(w-1,h-1):
                path=[]; cur=(x,y)
                while cur is not None: path.append(cur); cur=prev[cur]
                return list(reversed(path))
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                if (dx,dy) in walls[(x,y)]:
                    continue
                nx,ny=x+dx,y+dy
                if 0<=nx<w and 0<=ny<h and (nx,ny) not in prev:
                    prev[(nx,ny)]=(x,y); q.append((nx,ny))
        return []

    def draw_maze(self, idx):
        walls,w,h=self.make_maze(12,12)
        path=self.solve_maze(walls,w,h)
        self.validation["mazes"].append({"index": idx, "solvable": bool(path), "path_len": len(path)})

        self.np(self.book); self.header(self.book, f"Maze {idx}", "Start 🚀 to finish 🏁")
        x0,y0=M+0.5*inch, M+1.8*inch; cell=0.55*inch
        self.book.setStrokeColor(black); self.book.setLineWidth(2)
        for x in range(w):
            for y in range(h):
                cx=x0+x*cell; cy=y0+y*cell
                if (-1,0) in walls[(x,y)] and x==0: self.book.line(cx,cy,cx,cy+cell)
                if (1,0) in walls[(x,y)]: self.book.line(cx+cell,cy,cx+cell,cy+cell)
                if (0,-1) in walls[(x,y)] and y==0: self.book.line(cx,cy,cx+cell,cy)
                if (0,1) in walls[(x,y)]: self.book.line(cx,cy+cell,cx+cell,cy+cell)
        self.book.setFont("Helvetica", 16); self.book.drawString(x0-0.35*inch, y0+0.05*inch, "🚀"); self.book.drawString(x0+w*cell+0.05*inch, y0+h*cell-0.2*inch, "🏁")

        self.np(self.key); self.header(self.key, f"Maze {idx} Answer", "Solution path shown")
        self.key.setStrokeColor(black); self.key.setLineWidth(1.5)
        for x in range(w):
            for y in range(h):
                cx=x0+x*cell; cy=y0+y*cell
                if (-1,0) in walls[(x,y)] and x==0: self.key.line(cx,cy,cx,cy+cell)
                if (1,0) in walls[(x,y)]: self.key.line(cx+cell,cy,cx+cell,cy+cell)
                if (0,-1) in walls[(x,y)] and y==0: self.key.line(cx,cy,cx+cell,cy)
                if (0,1) in walls[(x,y)]: self.key.line(cx,cy+cell,cx+cell,cy+cell)
        if path:
            self.key.setStrokeColor(HexColor("#e53935")); self.key.setLineWidth(3)
            for i in range(len(path)-1):
                x1,y1=path[i]; x2,y2=path[i+1]
                self.key.line(x0+(x1+0.5)*cell, y0+(y1+0.5)*cell, x0+(x2+0.5)*cell, y0+(y2+0.5)*cell)

    def make_word_search(self, words, size=12):
        grid=[[None]*size for _ in range(size)]
        dirs=[(1,0),(0,1),(1,1),(-1,1)]
        placements=[]
        for w in words:
            placed=False
            for _ in range(400):
                dx,dy=random.choice(dirs); x=random.randrange(size); y=random.randrange(size)
                ex=x+dx*(len(w)-1); ey=y+dy*(len(w)-1)
                if not (0<=ex<size and 0<=ey<size): continue
                ok=True
                for i,ch in enumerate(w):
                    xx,yy=x+dx*i,y+dy*i
                    if grid[yy][xx] not in (None,ch): ok=False; break
                if not ok: continue
                for i,ch in enumerate(w):
                    xx,yy=x+dx*i,y+dy*i; grid[yy][xx]=ch
                placements.append({"word":w,"start":[x,y],"dir":[dx,dy]})
                placed=True; break
            if not placed:
                return None, []
        for r in range(size):
            for c in range(size):
                if grid[r][c] is None: grid[r][c]=random.choice(string.ascii_uppercase)
        return grid, placements

    def draw_word_search(self, idx, words):
        grid, placements = self.make_word_search(words, 12)
        ok = len(placements)==len(words)
        self.validation["word_searches"].append({"index":idx, "valid": ok, "words": words})

        self.np(self.book); self.header(self.book, f"Word Search {idx}", "Find all words")
        gx,gy=M+0.6*inch,H-7.8*inch; cs=0.42*inch
        self.book.setStrokeColor(HexColor("#888")); self.book.setLineWidth(1)
        self.book.setFont("Helvetica-Bold",12)
        for r in range(12):
            for c in range(12):
                x=gx+c*cs; y=gy-r*cs
                self.book.rect(x,y,cs,cs,fill=0,stroke=1)
                self.book.drawString(x+0.15*inch,y+0.14*inch,grid[r][c])
        self.book.setFont("Helvetica",12); self.book.drawString(M, M+0.7*inch, "Words: "+", ".join(words))

        self.np(self.key); self.header(self.key, f"Word Search {idx} Answer", "Highlighted placements")
        self.key.setStrokeColor(HexColor("#888")); self.key.setLineWidth(1); self.key.setFont("Helvetica-Bold",12)
        for r in range(12):
            for c in range(12):
                x=gx+c*cs; y=gy-r*cs
                self.key.rect(x,y,cs,cs,fill=0,stroke=1)
                self.key.drawString(x+0.15*inch,y+0.14*inch,grid[r][c])
        self.key.setStrokeColor(HexColor("#e53935")); self.key.setLineWidth(2)
        for p in placements:
            x,y = p["start"]; dx,dy = p["dir"]; L=len(p["word"])
            x1,y1 = gx+(x+0.5)*cs, gy-(y+0.5)*cs
            x2,y2 = gx+(x+dx*(L-1)+0.5)*cs, gy-(y+dy*(L-1)+0.5)*cs
            self.key.line(x1,y1,x2,y2)

    def draw_find_me(self, idx):
        targets=["⭐","🍎","🚗","🐟"]
        pool=targets+["🍌","⚽","🐶","🌙","🎈","🧩","📘"]
        cols,rows=10,12
        grid=[]; counts={t:0 for t in targets}
        for r in range(rows):
            row=[]
            for c in range(cols):
                ch=random.choice(pool)
                if random.random()<0.16:
                    ch=random.choice(targets)
                if ch in counts: counts[ch]+=1
                row.append(ch)
            grid.append(row)
        self.validation["find_me"].append({"index":idx,"counts":counts})

        self.np(self.book); self.header(self.book, f"Find-Me {idx}", "Find and circle all targets")
        gx,gy=M+0.2*inch,H-2.2*inch
        self.book.setFont("Helvetica",20)
        for r in range(rows):
            for c in range(cols):
                self.book.drawString(gx+c*0.75*inch, gy-r*0.65*inch, grid[r][c])
        self.book.setFont("Helvetica-Bold",12)
        self.book.drawString(M, M+0.6*inch, "Targets: " + "  ".join([f"{t} x ?" for t in targets]))

        self.np(self.key); self.header(self.key, f"Find-Me {idx} Answer", "Verified counts")
        self.key.setFont("Helvetica",20)
        for r in range(rows):
            for c in range(cols):
                self.key.drawString(gx+c*0.75*inch, gy-r*0.65*inch, grid[r][c])
        self.key.setFont("Helvetica-Bold",13)
        self.key.drawString(M, M+0.6*inch, "Counts: " + "  ".join([f"{t} x {counts[t]}" for t in targets]))

    def tracing(self):
        for L in ["A","B"]:
            self.np(self.book); self.header(self.book, f"Trace Letter {L}", "Trace then write")
            y=H-2.2*inch
            for row in range(5):
                self.book.setStrokeColor(HexColor("#d9d9d9"))
                self.book.line(M, y+0.35*inch, W-M, y+0.35*inch)
                self.book.setDash(3,3); self.book.line(M, y, W-M, y); self.book.setDash()
                self.book.line(M, y-0.35*inch, W-M, y-0.35*inch)
                self.book.setFont("Helvetica-Bold",54); self.book.setFillColor(HexColor("#b0b0b0"))
                for i in range(4):
                    x=M+0.2*inch+i*1.9*inch
                    if row<3 or i<2: self.book.drawString(x,y-0.18*inch,L)
                y-=1.6*inch

    def build(self):
        # cover
        self.np(self.book)
        self.book.setFillColor(HexColor("#1f6feb")); self.book.rect(0,H-2.2*inch,W,2.2*inch,fill=1,stroke=0)
        self.book.setFillColor(HexColor("#fff")); self.book.setFont("Helvetica-Bold",28)
        self.book.drawString(M,H-1.35*inch,"Premium Interactive Workbook V2")
        self.book.setFillColor(HexColor("#222")); self.book.setFont("Helvetica",12)
        self.book.drawString(M,H-2.55*inch,"Validated puzzles + answer key")

        self.np(self.key); self.header(self.key, "Answer Key", "Premium Interactive Workbook V2")

        self.tracing()
        for i in range(1,5): self.draw_maze(i)
        self.draw_word_search(1,["CAT","DOG","SUN","MOON","BOOK"])
        self.draw_word_search(2,["APPLE","FISH","CAR","STAR","TREE"])
        self.draw_find_me(1); self.draw_find_me(2)

        self.book.save(); self.key.save()

        # validation summary
        all_ok = all(m["solvable"] for m in self.validation["mazes"]) and all(w["valid"] for w in self.validation["word_searches"])
        self.validation["summary"]={"all_ok":all_ok,"seed":self.seed}
        with open(self.report_json,"w") as f: json.dump(self.validation,f,indent=2)

        return self.book_pdf, self.key_pdf, self.report_json

if __name__ == "__main__":
    wb=PremiumWorkbook(seed=42)
    b,k,r=wb.build()
    print("✅ Built premium workbook")
    print(b)
    print(k)
    print(r)
