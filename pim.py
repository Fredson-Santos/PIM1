import customtkinter as ctk
from tkinter import messagebox
import json, os, statistics, webbrowser, re, urllib.request, io, requests
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ARQUIVO_USUARIOS = "usuarios.json"

#função para carregar e salvar usuários
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

#verifica se o email é válido
def email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def campos_preenchidos(campos):
    return all(campo.strip() for campo in campos)

def calcular_porcentagem_genero(usuarios):
    total = len(usuarios)
    if total == 0:
        return {"Masculino": 0, "Feminino": 0}
    
    contagem = {"Masculino": 0, "Feminino": 0}
    for u in usuarios:
        sexo = u.get("sexo", "").capitalize()
        if sexo in contagem:
            contagem[sexo] += 1
    
    return {
        "Masculino": round((contagem["Masculino"] / total) * 100, 2),
        "Feminino": round((contagem["Feminino"] / total) * 100, 2)
    }


#janela de login e cadastro
class App:
    def __init__(self):
        self.usuarios = carregar_usuarios()
        self.usuario_atual = None
        self.janela_login()

    def janela_login(self):
        self.root = ctk.CTk()
        self.root.geometry("720x480")
        self.root.title("Login")

        ctk.CTkLabel(self.root, text="Login", font=("Arial", 24)).pack(pady=10)

        self.email_entry = ctk.CTkEntry(self.root, placeholder_text="E-mail")
        self.senha_entry = ctk.CTkEntry(self.root, placeholder_text="Senha", show="*")
        self.email_entry.pack(pady=5)
        self.senha_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Entrar", command=self.login).pack(pady=10)
        ctk.CTkButton(self.root, text="Cadastrar", command=self.tela_cadastro).pack()

        self.root.mainloop()

    def tela_cadastro(self):
        self.root.destroy()
        self.root = ctk.CTk()
        self.root.geometry("720x480")
        self.root.title("Cadastro de Usuário")

        ctk.CTkLabel(self.root, text="Cadastro de Usuário", font=("Arial", 20)).pack(pady=10)

        self.nome_entry = ctk.CTkEntry(self.root, placeholder_text="Nome")
        self.email_entry = ctk.CTkEntry(self.root, placeholder_text="E-mail")
        self.senha_entry = ctk.CTkEntry(self.root, placeholder_text="Senha", show="*")
        self.idade_entry = ctk.CTkEntry(self.root, placeholder_text="Idade")
        self.sexo_var = ctk.StringVar(value="Selecione o sexo")
        self.sexo_menu = ctk.CTkOptionMenu(self.root, variable=self.sexo_var, values=["Feminino", "Masculino"])

        for widget in [self.nome_entry, self.email_entry, self.senha_entry, self.idade_entry, self.sexo_menu]:
            widget.pack(pady=5)

        ctk.CTkButton(self.root, text="Cadastrar Usuário", command=self.cadastrar_usuario).pack(pady=10)
        ctk.CTkButton(self.root, text="Voltar ao Login", command=self.voltar_login).pack(pady=5)

        self.root.mainloop()

    def voltar_login(self):
        self.root.destroy()
        self.janela_login()

    def cadastrar_usuario(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        idade = self.idade_entry.get()
        sexo = self.sexo_var.get()

        if sexo not in ["Feminino", "Masculino"]:
            messagebox.showerror("Erro", "Selecione um sexo válido.")
            return

        if not campos_preenchidos([nome, email, senha, idade, sexo]):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        if not email_valido(email):
            messagebox.showerror("Erro", "E-mail inválido!")
            return

        usuario = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "idade": int(idade),
            "sexo": sexo,
            "tipo": "admin" if "@admin" in email else "user"
        }

        self.usuarios.append(usuario)
        salvar_usuarios(self.usuarios)
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.voltar_login()

    def login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        for user in self.usuarios:
            if user["email"] == email and user["senha"] == senha:
                self.usuario_atual = user
                self.root.destroy()
                self.tela_conteudo()
                return

        messagebox.showerror("Erro", "E-mail ou senha incorretos!")

    def logoff(self):
        self.usuario_atual = None
        self.root.destroy()
        self.janela_login()

    def carregar_imagem_url(self, url, tamanho=(200, 120)):
        try:
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            img = Image.open(io.BytesIO(raw_data))
            img = img.resize(tamanho)
            return ImageTk.PhotoImage(img)
        except:
            return None


    #carrefa imagem a partir de uma URL
    def carregar_imagem_url(self, url, tamanho=(320, 213)):
        try:
            resposta = requests.get(url)
            imagem = Image.open(io.BytesIO(resposta.content))
            imagem = imagem.resize(tamanho)
            return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)
        except:
            return None

    def tela_conteudo(self):
        self.root = ctk.CTk()
        self.root.geometry("1080x720")
        self.root.title("Plataforma TechParaTodos")

        ctk.CTkLabel(self.root, text="\nConteúdos Disponiveis \n", font=("Arial", 24)).pack(pady=10)

        self.opcao = ctk.StringVar(value="")

        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(pady=20)

        #listas de conteúdos (para alterar e so mudar os links)
        opcoes = [
            ("Lógica de Programação", "https://youtube.com/playlist?list=PLHz_AreHm4dmSj0MHol_aoNYCSGFqvfXV&si=imsDUOFbDJLvo_jO", 
             "https://raw.githubusercontent.com/Fredson-Santos/images/refs/heads/main/Log%20de%20Programa%C3%A7%C3%A3o.png?token=GHSAT0AAAAAADEH5KKFKPSKNYEPXWYN6OCU2B3HLVA"),
            ("Introdução a Python", "https://youtube.com/playlist?list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6&si=7GAyD93_b9P0hlEF", 
             "https://raw.githubusercontent.com/Fredson-Santos/images/refs/heads/main/Int%20Python.png?token=GHSAT0AAAAAADEH5KKEQ4IS6IKGYYVXP7NA2B3HLEA"),
            ("Segurança da Informação", "https://www.youtube.com/playlist?list=PLHz_AreHm4dlaTyjolzCFC6IjLzO8O0XV", 
             "https://raw.githubusercontent.com/Fredson-Santos/images/refs/heads/main/INFO.png?token=GHSAT0AAAAAADEH5KKEOYATXMJTEZSKL7VE2B3HIBA")
        ]

        for titulo, link, img_url in opcoes:
            img = self.carregar_imagem_url(img_url, tamanho=(320, 213)) 

            bloco = ctk.CTkFrame(frame)
            bloco.pack(side="left", padx=15)
            
            if img:
                img_label = ctk.CTkLabel(bloco, image=img, text="")
                img_label.pack(pady=5)

            ctk.CTkRadioButton(bloco, text=titulo, variable=self.opcao, value=link).pack()

        #botões de ação
        ctk.CTkButton(self.root, text="Acessar Conteúdo", command=self.abrir_conteudo).pack(pady=10)

        if self.usuario_atual["tipo"] == "admin":
            ctk.CTkButton(self.root, text="Relatório de Usuários", command=self.gerar_relatorio).pack(pady=5)

        ctk.CTkButton(self.root, text="Sair", command=self.logoff).pack(pady=10)

        self.root.mainloop()

    #funcao pra abrir o conteudo escolhido
    def abrir_conteudo(self):
        link = self.opcao.get()
        if link:
            webbrowser.open(link)
        else:
            messagebox.showwarning("Aviso", "Selecione um conteúdo!")


    #gerar relatorio com media, mediana e moda das idades e porcentagem de cada sexo
    def gerar_relatorio(self):
        idades = [u["idade"] for u in self.usuarios if isinstance(u.get("idade"), int)]
        total = len(self.usuarios)

        if not idades or total == 0:
            messagebox.showerror("Erro", "Não há dados suficientes para gerar o relatório.")
            return

        media = round(statistics.mean(idades), 2)
        mediana = statistics.median(idades)
        try:
            moda = statistics.mode(idades)
        except statistics.StatisticsError:
            moda = "Sem moda única"

        #calcula a porcentagen de sexo
        masculino = sum(1 for u in self.usuarios if u.get("sexo") == "Masculino")
        feminino = sum(1 for u in self.usuarios if u.get("sexo") == "Feminino")

        porcentagem_masculino = round((masculino / total) * 100, 1)
        porcentagem_feminino = round((feminino / total) * 100, 1)

        texto = (
            f"Total de usuários: {total}\n"
            f"Idade média: {media}\n"
            f"Idade mais comum: {moda}\n"
            f"Mediana das idades: {mediana}\n"
            f"Homens: {porcentagem_masculino}%\n"
            f"Mulheres: {porcentagem_feminino}%\n\n"
            "Deseja salvar o relatório?"
        )

        resposta = messagebox.askyesno("Relatório de Usuários", texto, icon='question')

        if resposta:
            relatorio = {
                "total_usuarios": total,
                "media_idade": media,
                "mediana_idade": mediana,
                "moda_idade": moda,
                "porcentagem_masculino": porcentagem_masculino,
                "porcentagem_feminino": porcentagem_feminino,
                "usuarios": [
                    {
                        "nome": u.get("nome", "Desconhecido"),
                        "email": u.get("email", "sem@email.com"),
                        "idade": u.get("idade", 0),
                        "sexo": u.get("sexo", "Não informado")
                    }
                    for u in self.usuarios
                ]
            }

            with open("relatorio.json", "w") as f:
                json.dump(relatorio, f, indent=4)

            messagebox.showinfo("Relatório Salvo", "O relatório foi salvo como relatorio.json.")

            #abrir o arquivo JSON gerado            
            try:
                os.startfile("relatorio.json")  #só funciona no Windows
            except Exception as e:
                print(f"Erro ao abrir o arquivo: {e}")





App()
