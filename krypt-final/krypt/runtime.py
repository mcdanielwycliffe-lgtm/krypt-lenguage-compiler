import sys, pathlib, math as pymath

class ReturnSignal(Exception):
    def __init__(self,value): self.value=value

class KryptShape:
    def __init__(self, canvas, item, kind, coords):
        self.canvas, self.item, self.kind, self.coords = canvas, item, kind, list(coords)
    def set_position(self, x, y):
        dx, dy = float(x)-self.coords[0], float(y)-self.coords[1]
        self.move(dx, dy); return self
    def move(self, dx, dy):
        self.canvas.move(self.item, float(dx), float(dy))
        if self.kind == 'segment':
            self.coords[0]+=dx; self.coords[1]+=dy; self.coords[2]+=dx; self.coords[3]+=dy
        else:
            for i in range(0,len(self.coords),2): self.coords[i]+=dx; self.coords[i+1]+=dy
        return self
    def set_color(self, color):
        options={'fill':str(color)}
        if self.kind != 'text': options['outline']=str(color)
        self.canvas.itemconfigure(self.item, **options); return self
    def set_width(self, width):
        self.canvas.itemconfigure(self.item, width=float(width)); return self
    def set_size(self, width, height):
        if self.kind in ('segment','text'): return self
        x,y=self.coords[0],self.coords[1]
        self.coords[2],self.coords[3]=x+float(width),y+float(height)
        self.canvas.coords(self.item,*self.coords); return self
    def set_font_size(self, size):
        if self.kind == 'text': self.canvas.itemconfigure(self.item, font=('Arial',int(size)))
        return self
    def hide(self): self.canvas.itemconfigure(self.item, state='hidden'); return self
    def show(self): self.canvas.itemconfigure(self.item, state='normal'); return self
    def remove(self): self.canvas.delete(self.item); return None

class KryptFunction:
    def __init__(self,params,body,vm): self.params,self.body,self.vm=params,body,vm
    def __call__(self,*args):
        old=self.vm.env; self.vm.env=dict(old)
        for i,p in enumerate(self.params): self.vm.env[p]=args[i] if i<len(args) else None
        try: self.vm.exec_block(self.body)
        except ReturnSignal as r: result=r.value
        else: result=None
        self.vm.env=old; return result

class WindowLib:
    def __init__(self,vm): self.vm=vm; self.root=None
    def create(self,title='Krypt',width=640,height=480):
        import tkinter as tk
        self.root=tk.Tk(); self.root.title(str(title)); self.root.geometry(f'{int(width)}x{int(height)}')
        self.canvas=tk.Canvas(self.root,width=int(width),height=int(height),highlightthickness=0)
        self.canvas.pack(fill='both',expand=True)
        self.vm.env['window_handle']=self.root; return self.root
    def set_background(self,color):
        if self.root:
            self.root.configure(bg=str(color)); self.canvas.configure(bg=str(color))
    def text(self,value,x=20,y=20,size=18,color='white'):
        if not self.root: raise RuntimeError('window.create deve ser chamado antes')
        item=self.canvas.create_text(int(x),int(y),text=str(value),anchor='nw',font=('Arial',int(size)),fill=str(color)); return KryptShape(self.canvas,item,'text',[x,y])
    def input_box(self,prompt='Valor',kind='text',default=''):
        import tkinter.simpledialog as dialog
        self._ready(); kind=str(kind).lower()
        if kind in ('integer','int','inteiro'): return dialog.askinteger('Krypt',str(prompt),initialvalue=int(default or 0),parent=self.root)
        if kind in ('decimal','float','real'): return dialog.askfloat('Krypt',str(prompt),initialvalue=float(default or 0),parent=self.root)
        if kind in ('boolean','bool','logico','lógico'):
            import tkinter.messagebox as messagebox
            return messagebox.askyesno('Krypt',str(prompt),parent=self.root)
        return dialog.askstring('Krypt',str(prompt),initialvalue=str(default),parent=self.root)
    def segment(self,x1,y1,x2,y2,color='white',width=2):
        self._ready(); item=self.canvas.create_line(x1,y1,x2,y2,fill=str(color),width=float(width)); return KryptShape(self.canvas,item,'segment',[x1,y1,x2,y2])
    def panel(self,x,y,width,height,color='white',outline=None,stroke=2):
        self._ready(); outline=str(outline if outline is not None else color)
        item=self.canvas.create_rectangle(x,y,float(x)+float(width),float(y)+float(height),fill=str(color),outline=outline,width=float(stroke)); return KryptShape(self.canvas,item,'panel',[x,y,float(x)+float(width),float(y)+float(height)])
    def ellipse(self,x,y,width,height,color='white',outline=None,stroke=2):
        self._ready(); outline=str(outline if outline is not None else color)
        item=self.canvas.create_oval(x,y,float(x)+float(width),float(y)+float(height),fill=str(color),outline=outline,width=float(stroke)); return KryptShape(self.canvas,item,'ellipse',[x,y,float(x)+float(width),float(y)+float(height)])
    def _ready(self):
        if not self.root: raise RuntimeError('window.create deve ser chamado antes')
    def show(self):
        if not self.root: raise RuntimeError('window.create deve ser chamado antes')
        self.root.mainloop()
    def close(self):
        if self.root: self.root.destroy()

class IOLib:
    def __init__(self,vm): self.vm=vm
    def on_key(self,key,callback):
        root=self.vm.env.get('window_handle')
        if not root: raise RuntimeError('window.create deve ser chamado antes de iolib.on_key')
        root.bind(f'<KeyPress-{key}>',lambda e: (self.vm.keys_down.__setitem__(str(key),True), callback(key))); return None
    def track_key(self,key):
        root=self.vm.env.get('window_handle')
        if not root: raise RuntimeError('window.create deve ser chamado antes de iolib.track_key')
        root.bind(f'<KeyPress-{key}>',lambda e: self.vm.keys_down.__setitem__(str(key),True))
        root.bind(f'<KeyRelease-{key}>',lambda e: self.vm.keys_down.__setitem__(str(key),False)); return None
    def on_click(self,callback):
        root=self.vm.env.get('window_handle')
        if not root: raise RuntimeError('window.create deve ser chamado antes de iolib.on_click')
        root.bind('<Button-1>',lambda e: callback(e.x,e.y)); return None
    def key(self,key):
        return self.vm.keys_down.get(str(key),False)
    def input(self,prompt=''): return input(str(prompt))

class MathLib:
    def __init__(self,vm): self.vm=vm
    pi=pymath.pi; e=pymath.e
    sin=staticmethod(pymath.sin); cos=staticmethod(pymath.cos); tan=staticmethod(pymath.tan)
    sqrt=staticmethod(pymath.sqrt); pow=staticmethod(pow); abs=staticmethod(abs)
    floor=staticmethod(pymath.floor); ceil=staticmethod(pymath.ceil)
    log=staticmethod(pymath.log); min=staticmethod(min); max=staticmethod(max)
    def radians(self,x): return pymath.radians(x)
    def degrees(self,x): return pymath.degrees(x)

class GatesLib:
    def __init__(self,vm):
        self.vm=vm; setattr(self,'and',self.and_); setattr(self,'or',self.or_); setattr(self,'not',self.not_)
    def add(self,a,b): return a+b
    def sub(self,a,b): return a-b
    def mul(self,a,b): return a*b
    def div(self,a,b): return a/b
    def and_(self,a,b): return bool(a) and bool(b)
    def or_(self,a,b): return bool(a) or bool(b)
    def xor(self,a,b): return bool(a) != bool(b)
    def xnor(self,a,b): return bool(a) == bool(b)
    def not_(self,a): return not bool(a)
    def nand(self,a,b): return not (bool(a) and bool(b))
    def nor(self,a,b): return not (bool(a) or bool(b))

class PsicsLib:
    def __init__(self,vm): self.vm=vm
    def gravity(self,velocity,acceleration,time): return velocity + acceleration*time
    def position(self,position,velocity,acceleration,time): return position + velocity*time + 0.5*acceleration*time*time
    def force(self,mass,acceleration): return mass*acceleration
    def momentum(self,mass,velocity): return mass*velocity
    def kinetic_energy(self,mass,velocity): return 0.5*mass*velocity*velocity
    def distance(self,x1,y1,x2,y2): return ((x2-x1)**2+(y2-y1)**2)**0.5
    def clamp(self,value,low,high): return max(low,min(high,value))

class VM:
    def __init__(self):
        self.env={'print':lambda *x: print(*x),'len':len,'str':str,'int':int,'float':float,'keys_down':{}}; self.keys_down={}
    def import_lib(self,name):
        if name=='window': self.env['window']=WindowLib(self)
        elif name=='iolib': self.env['iolib']=IOLib(self)
        elif name=='math': self.env['math']=MathLib(self)
        elif name=='gates': self.env['gates']=GatesLib(self)
        elif name=='psics': self.env['psics']=PsicsLib(self)
        else: raise RuntimeError(f'Biblioteca Krypt desconhecida: {name}')
    def run(self,program,base_dir=None):
        self.base_dir=pathlib.Path(base_dir or getattr(self,'base_dir',pathlib.Path.cwd()))
        for s in program.statements: self.exec(s)
    def exec_block(self,b):
        for s in b.statements: self.exec(s)
    def exec(self,n):
        from .parser import Block,Import,ImportFile,Var,Assign,ExprStmt,If,While,Fun,Return
        if isinstance(n,Import): self.import_lib(n.name)
        elif isinstance(n,ImportFile):
            target=(self.base_dir / n.path).resolve()
            if not target.is_file(): raise RuntimeError(f'Arquivo Krypt não encontrado: {target}')
            from .parser import Parser
            old=self.base_dir; self.base_dir=target.parent
            self.run(Parser(target.read_text(encoding='utf-8')).parse(),target.parent)
            self.base_dir=old
        elif isinstance(n,Block): self.exec_block(n)
        elif isinstance(n,Var): self.env[n.name]=self.eval(n.expr)
        elif isinstance(n,Assign): self.env[n.name]=self.eval(n.expr)
        elif isinstance(n,ExprStmt): self.eval(n.expr)
        elif isinstance(n,If):
            condition=self.eval(n.cond)
            if condition: self.exec(n.then)
            elif n.otherwise: self.exec(n.otherwise)
        elif isinstance(n,While):
            while self.eval(n.cond): self.exec(n.body)
        elif isinstance(n,Fun): self.env[n.name]=KryptFunction(n.params,n.body,self)
        elif isinstance(n,Return): raise ReturnSignal(self.eval(n.expr))
    def eval(self,n):
        from .parser import Literal,Name,Unary,Binary,Call,Member,ListExpr
        if isinstance(n,Literal): return n.value
        if isinstance(n,Name):
            if n.value not in self.env: raise RuntimeError(f'Nome não definido: {n.value}')
            return self.env[n.value]
        if isinstance(n,Member): return getattr(self.eval(n.obj),n.name)
        if isinstance(n,ListExpr): return [self.eval(x) for x in n.items]
        if isinstance(n,Unary):
            v=self.eval(n.expr); return (not v) if n.op in ('!','not') else -v
        if isinstance(n,Binary):
            a=self.eval(n.left); b=self.eval(n.right)
            return {'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b,'/':lambda:a/b,'%':lambda:a%b,'==':lambda:a==b,'!=':lambda:a!=b,'<':lambda:a<b,'>':lambda:a>b,'<=':lambda:a<=b,'>=':lambda:a>=b,'and':lambda:a and b,'&&':lambda:a and b,'or':lambda:a or b,'||':lambda:a or b}[n.op]()
        if isinstance(n,Call): return self.eval(n.callee)(*[self.eval(x) for x in n.args])
        raise RuntimeError('Nó inválido')

def run_source(source, base_dir=None):
    from .parser import Parser
    vm=VM(); vm.run(Parser(source).parse(),base_dir or pathlib.Path.cwd()); return vm
